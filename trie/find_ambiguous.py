# Imports

from sys import stdin
from collections import defaultdict as dd
import logging

import dawg

# Functions

SHIFT = 6  # any word is shorter than 2**6 characters

def encode_accents(k, v):
    assert "+" in v and v.replace("+", "") == k, (k, v)
    assert len(v) < 2**SHIFT and not v.startswith("+"), (k, v)
    accent_inds = [i for i, c in enumerate(v) if c == "+"]
    for i, _ in enumerate(accent_inds):
        accent_inds[i] = (accent_inds[i] - i) << (i * SHIFT)
    return sum(accent_inds)

def decode_accents(k, x):
    inds = []
    while x > 0:
        inds.append(x % 2**SHIFT)
        x //= 2**SHIFT
    segments = [k[i:j] for i, j in zip([0] + inds, inds + [len(k)])]
    return "+".join(segments)

# Main loop

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("Reading patterns...")
    patterns = {}
    with open("patterns") as f:
        for line in f:
            v = line.strip()
            k = v.replace("+", "")
            assert k not in patterns, k
            patterns[k] = v

    logger.info("Reading input data...")
    data = dd(set)
    for line in stdin:
        line = line.strip().lower()
        if not line:
            continue
        # if "+" not in line:
        #     print(line)
        data[line.replace("+", "")].add(line)

    logger.info("Applying patterns to data...")
    unmatched = []
    for k in sorted(data):
        v = data[k]
        if all("+" not in x for x in v):
            assert len(v) == 1 and list(v)[0] == k
            matches = [p for p in patterns if k.startswith(p)]
            if matches:
                if len(matches) > 1:
                    logger.warning("Multiple patterns: %s => %s", k, matches)
                max_len = max([len(p) for p in matches])
                longest_matches = [p for p in matches if len(p) == max_len]
                assert len(longest_matches) == 1, (k, matches)
                p = longest_matches.pop()
                data[k] = {patterns[p] + k[len(p):]}
            else:
                unmatched.append(k)
                del data[k]
                continue
        elif any("+" not in x for x in v):
            data[k] = {x for x in v if "+" in x}
            assert len(data[k]) > 0
        v = data[k]
        if len(v) == 2 and sorted([x.count("+") for x in v]) == [1, 2]:
            a, b = v
            if a.count("+") == 2:
                a, b = b, a
            stress_inds = [i for i, c in enumerate(b) if c == "+"]
            for i in stress_inds:
                if a == b[:i] + b[i+1:]:
                    data[k] = {b}
                    break

    #     if len({x.lower() for x in v}) > 1:
    #         print(k, "|".join(v), sep="\t")

    logger.info("Writing out unmatched items...")
    with open("unmatched", "w") as f:
        for w in unmatched:
            print(w, file=f)

    logger.info("Writing out ambiguous items...")
    ambiguous = [k for k in data if len(data[k]) > 1]
    for k in sorted(ambiguous, key=lambda x: x[::-1]):
        print(k, "|".join(sorted(data[k])), sep="\t")

    logger.info("Writing out DAWGs...")
    assert all(len(v) > 0 for v in data.values())
    accent_codes = {}
    for k in data:
        if len(data[k]) == 1:
            v = sorted(data[k])[0]
            x = encode_accents(k, v)
            assert decode_accents(k, x) == v, (k, v, x, decode_accents(k, x))
            assert k not in accent_codes
            accent_codes[k] = x
    d_unambiguous = dawg.IntDAWG((k, accent_codes[k]) for k in data if len(data[k]) == 1)
    d_unambiguous.save("unambiguous.dawg")
    d_ambiguous = dawg.DAWG(k for k in data if len(data[k]) > 1)
    d_ambiguous.save("ambiguous.dawg")
