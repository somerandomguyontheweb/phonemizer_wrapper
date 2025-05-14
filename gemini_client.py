# Imports

import json
from functools import lru_cache

import requests

# Constants

API_KEY = None
URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=%s"

EXPANSION_PROMPT_TEMPLATE = """You will be given a short text in Belarusian, possibly containing numbers, special characters (like %, $, §, etc.), and abbreviations. Your task is to expand all such items into words, as a preprocessing step before grapheme-to-phoneme conversion. All tokens that aren't numbers, special characters, or abbreviations must be copied verbatim from input to output. When expanding abbreviated proper names (like ЕС, ЗША, СССР, etc.), you should prefer phonetic rendering (like еэс, зэшэа, эсэсэсэр, etc.), rather than full-word expansion (like Еўрапейскі саюз, Злучаныя штаты Амерыкі, Саюз савецкіх сацыялістычных рэспублік, etc.). You must ensure correct agreement of inflected forms in case, number, and gender. In cases not envisaged above, act at your own discretion, following one core principle: The output must be readable text in Belarusian, following the input exactly as it would be normally pronounced by a competent speaker of Belarusian, and ready to be plugged into a grapheme-to-phoneme converter.

Here are a few examples.

Input: Я нарадзіўся ў 1992 г., вучыўся ў ПТВ, потым паступіў у БДУ.
Output: Я нарадзіўся ў тысяча дзевяцьсот дзевяноста другім годзе, вучыўся ў пэтэвэ, потым паступіў у бэдэу.

Input: Тэрмін да 10 гадоў зняволення прадугледжаны ч. 2 арт. 130 КК РБ у рэдакцыі ад 08.07.2024.
Output: Тэрмін да дзесяці гадоў зняволення прадугледжаны часткай другой артыкула сто трыццатага кака эрбэ ў рэдакцыі ад восьмага ліпеня дзве тысячы дваццаць чацвёртага.

Input: Пры тэмпературы 20 °C ±0.5 °C вільготнасць паветра можа вар'іравацца ад 1 ‰ да 99 %.
Output: Пры тэмпературы дваццаць градусаў Цэльсія плюс-мінус ноль цэлых пяць дзясятых градуса Цэльсія вільготнасць паветра можа вар'іравацца ад аднаго праміле да дзевяноста дзевяці працэнтаў.
Note: For the character % it is allowed to use any of the words "працэнт" or "адсотак", so that it might as well be "дзевяноста дзевяці адсоткаў" in the above example.

Now the actual instance.

Input: """

ACCENTUATION_PROMPT_TEMPLATE = """You will be given a short text in Belarusian. Some words in it might be already accentuated with the symbol U+0301 (́) after the stressed vowel. Your task is to accentuate the same way all other content words that bear stress. Do not accentuate clitics; if some of the clitics are stressed and you think it is wrong, remove the accents. If none of the words require modifications, just copy the input to output. Otherwise, your output must only differ from the input in U+0301 symbols after the stressed vowels: there may be additional ones, and some may be removed (in the clitics).

Input: """

# Functions

def init_client():
    global API_KEY
    with open("./gemini_api_key") as f:
        API_KEY = f.read().strip()

make_payload = lambda prompt: {"contents": [{"parts": [{"text": prompt}]}]}

def extract_response_text(dct):
    assert "candidates" in dct
    assert len(dct["candidates"]) == 1
    assert "content" in dct["candidates"][0]
    assert "parts" in dct["candidates"][0]["content"]
    assert len(dct["candidates"][0]["content"]["parts"]) == 1
    assert "text" in dct["candidates"][0]["content"]["parts"][0]
    text = dct["candidates"][0]["content"]["parts"][0]["text"].strip()
    if text.startswith("Output: "):
        text = text[8:]
    return text

@lru_cache(maxsize=2**20)
def ask_gemini(prompt):
    if API_KEY is None:
        _ = init_client()
    r = requests.post(
        URL_TEMPLATE % API_KEY,
        headers={"Content-Type": "application/json"},
        data=json.dumps(make_payload(prompt))
    )
    assert r.status_code == 200, r
    return extract_response_text(r.json())

def gemini_expand(s: str) -> str:
    return ask_gemini(EXPANSION_PROMPT_TEMPLATE + s)

def gemini_accentuate(s: str) -> str:
    return ask_gemini(ACCENTUATION_PROMPT_TEMPLATE + s)
