# Imports

from typing import List, Tuple
from functools import lru_cache
from string import digits, punctuation

import dawg
import jpype
import jpype.imports

from ttg_tokenizer import ttg_tokenize
from rule_based_expansion import expand_token, classify_token
from gemini_client import gemini_expand, gemini_accentuate

# Constants

SHIFT = 6
DAWG_UNAMBIGUOUS = dawg.IntDAWG().load("trie/unambiguous.dawg")
# DAWG_AMBIGUOUS = dawg.DAWG().load("trie/ambiguous.dawg")

BEL_FANETYKA_JAR = "./fanetyka.jar"
FINDER = None  # initialized in init_finder

# Functions

def join_back(tokens: List[str], seps: List[str]) -> str:
    assert len(seps) == len(tokens)
    return "".join(t + b for t, b in zip(tokens, seps))

def get_seps(s: str, tokens: List[str]) -> List[str]:
    assert len(tokens) > 0, (s, tokens)
    head, tail = tokens[0], tokens[1:]
    assert s.startswith(head), (s, tokens)
    suffix = s[len(head):]
    seps = []
    for t in tail:
        j = 0
        while not suffix[j:].startswith(t):
            j += 1
        seps.append(suffix[:j])
        suffix = suffix[j+len(t):]
    seps.append("")
    assert join_back(tokens, seps) == s, (join_back(tokens, seps), s)
    return seps

def tokenize(s: str) -> Tuple[List[str], List[str]]:
    tokens = ttg_tokenize(s).splitlines()
    seps = get_seps(s, tokens)
    return tokens, seps

def rule_based_expand(tokens: List[str]) -> List[str]:
    tokens_out = tokens[:]
    while True:
        tokens_in = ["", ""] + tokens_out + [""]
        tokens_out = [
            expand_token(*tokens_in[i:i+4])
            for i in range(len(tokens_in)-3)
        ]
        if tokens_out == tokens_in[2:-1]:
            break
    return tokens_out

def needs_gemini_expansion(s: str) -> bool:
    # tokens, seps = tokenize(s)
    # for t in tokens:
    #     c = classify_token(t)
    #     if t in ["digits", "digits_with_punctuation", "rnumber", "latin", "url", "unknown"]:
    #         return True
    return any(c in digits for c in s)

def grammardb_accentuate(token: str) -> str:
    if token.lower() in DAWG_UNAMBIGUOUS:
        x = DAWG_UNAMBIGUOUS[token.lower()]
        inds = []
        while x > 0:
            inds.append(x % 2**SHIFT)
            x //= 2**SHIFT
        segments = [token[i:j] for i, j in zip([0] + inds, inds + [len(token)])]
        return "́".join(segments)  # not "+" because fanetyka.jar doesn't understand it
    else:
        return token

def needs_gemini_accentuation(s: str) -> bool:
    tokens, seps = tokenize(s)
    for t in tokens:
        c = classify_token(t)
        if t == "lang_be":
            return True
    return False

def init_finder():
    jpype.startJVM(classpath=[BEL_FANETYKA_JAR])
    from org.alex73.korpus.base import GrammarDB2, GrammarFinder
    grammar_db = GrammarDB2.initializeFromJar()
    global FINDER
    FINDER = GrammarFinder(grammar_db)

@lru_cache(maxsize=2**20)
def grammardb_phonemize(s: str) -> str:
    if FINDER is None:
        _ = init_finder()
    from org.alex73.fanetyka.impl import FanetykaText
    return str(FanetykaText(FINDER, s).ipa)  # TODO: add error handling

def adjust_seps(seps: List[str], tokens: List[str]) -> List[str]:
    assert len(seps) == len(tokens)
    return [
        # 3% => 3адсоткі
        " " if (
            s == ""
            and len(t1) > 0
            and len(t2) > 0
            and t1[-1] not in punctuation + "«"
            and t2[0] not in punctuation + "»"
        ) else s
        for s, t1, t2 in zip(seps, tokens, tokens[1:] + [""])
    ]

def partially_expand(s: str) -> str:
    tokens, seps = tokenize(s)
    tokens_partially_expanded = rule_based_expand(tokens)
    seps_adjusted = adjust_seps(seps, tokens_partially_expanded)
    return join_back(tokens_partially_expanded, seps_adjusted)

def partially_accentuate(s_expanded: str) -> str:
    tokens_expanded, seps_expanded = tokenize(s_expanded)
    tokens_partially_accentuated = [grammardb_accentuate(t) for t in tokens_expanded]
    return join_back(tokens_partially_accentuated, seps_expanded)

def phonemize(s: str) -> str:
    s_partially_expanded = partially_expand(s)
    s_expanded = gemini_expand(s_partially_expanded) if needs_gemini_expansion(s_partially_expanded) else s_partially_expanded
    s_partially_accentuated = partially_accentuate(s_expanded)
    s_accentuated = gemini_accentuate(s_partially_accentuated) if needs_gemini_accentuation(s_partially_accentuated) else s_partially_accentuated
    phonemization = grammardb_phonemize(s_accentuated)
    return phonemization
