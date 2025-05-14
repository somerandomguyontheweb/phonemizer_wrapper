## Overview

This is a wrapper around the [BNKorpus phonemizer](https://github.com/alex73/Software-Korpus/releases/tag/fanetyka_1.0) of Belarusian. It adds two preprocessing steps:
- Expansion of numbers into numerals, abbreviations into full words, etc. A set of rules is applied to handle simpler cases (like *у 1984 г.* → *у тысяча дзевяцьсот восемдзесят чацвёртым годзе*), then the trickier cases that remain are handled with an external LLM.
- Accentuation. Tokens that have only one possible stress position are accentuated according to [GrammarDB](https://github.com/Belarus/GrammarDB), then the remaining tokens (i.e. homographs, like *прыкладаў*, and words missing from GrammarDB, such as proper names and recent loanwords) are handled with an external LLM.

The output – expanded accentuated text – is then fed into the BNKorpus phonemizer.

**Warning:** This is an early-stage prototype, nowhere near production quality. Feel free to edit the source code. Known issues:
- limited scope of the rules in `rule_based_expansion.py`;
- a somewhat outdated model (Gemini 2.0 Flash) and possibly suboptimal accentuation prompt in `gemini_client.py`;
- overly eager accentuation of clitics;
- no handling of errors raised by the BNKorpus phonemizer;
- no implementation of non-Belarusian tokens phonemization (Russian, English, etc.);
- no test coverage.

## Installation
- Make sure you have Python 3.x (`python3 -v`) and Java (`java -version`).
- Download the BNKorpus phonemizer: `wget https://github.com/alex73/Software-Korpus/releases/download/fanetyka_1.0/fanetyka.jar`
- Install dependencies, preferably in a separate virtualenv: `pip install DAWG jpype1`
- Create an API key in [Google AI Studio](https://aistudio.google.com) and save it in the file `gemini_api_key`. Mind the free tier quotas: up to 15 requests per minute, up to 1500 requests per day.
- Make sure you have all of the following files in the working directory:
```
.
├── trie/unambiguous.dawg    # the trie that stores unambiguously accentuated tokens (based on GrammarDB)
├── fanetyka.jar             # phonemizer JAR file
├── gemini_api_key           # API key file
├── ttg_tokenizer.py         # auxiliary module for tokenization
├── belarusian_numerals.py   # auxiliary module for number -> numeral conversion
├── rule_based_expansion.py  # auxiliary module for rule-based text processing
├── gemini_client.py         # auxiliary module for LLM-powered text processing
├── phonemizer_wrapper.py    # main module
└── test_harness.py          # example script
```

## Usage
```
>>> from phonemizer_wrapper import phonemize
>>> s = "У 1918–1991 гг., асабліва ў 2-й пал. XX ст., КП(б)Б надзяляла шмат увагі пытанням ЖКГ."
>>> phonemization = phonemize(s)
>>> phonemization
'ˈu ˈtɨsʲat͡ʂa d͡zʲɛvʲaˈt͡sʲsɔt vasʲamˈnat͡sːatɨm– ˈtɨsʲat͡ʂa d͡zʲɛvʲaˈt͡sʲsɔd͡zʲːɛvʲaˈnɔsta ˈpʲɛrʂɨm ˈɣadax, asaˈblʲiva ˈu druˈɣɔj paˈɫɔvʲɛ dvaˈt͡sːataɣa staˈɣɔd͡zʲːa, kamunʲiˈstɨt͡ʂnaja ˈpartɨja balʲʂavʲiˈkɔu̯ bʲɛɫaˈrusʲi nad͡zʲaˈlʲaɫa ˈʂmat uˈvaɣʲi pɨˈtanʲːam ʐɨlʲːɔvakamuˈnalʲnaj ɣaspaˈdarkʲi.'
```

As the `.jar` file of the BNKorpus phonemizer takes some time to initialize all necessary data structures, expect a longer delay (~10 seconds) on the first call, all subsequent calls are going to be much faster.

More examples:
- To process 5 pre-selected sentences and print the outputs in IPA phonemization: `python3 test_harness.py`
- To debug the expansion rules:
    - Download the Belarusian dataset of [FLORES](https://huggingface.co/datasets/facebook/flores) (~2K short paragraphs from Wikipedia), as described in `./validate/flores/README.md`.
    - In `test_harness.py`, comment out the `sanity_check` call and uncomment the `flores_check` call.
    - Run `python3 test_harness.py` once again and inspect the resulting file `./validate/flores/intermediate.csv`. Repeat this step upon each change in `rule_based_expansion.py`.
