The [tries](https://en.wikipedia.org/wiki/Trie) `ambiguous.dawg` and `unambiguous.dawg` store information about Belarusian words that have either more than one accentuation variant (=ambiguous) or exactly one accentuation variant (=unambiguous).

To create or update the tries, extract all wordforms from a release version of [GrammarDB](https://github.com/Belarus/GrammarDB):
```
wget https://github.com/Belarus/GrammarDB/releases/download/RELEASE-202309/RELEASE-20230920.zip
unzip RELEASE-20230920.zip
rm -r spellchecker
cat *.xml | grep Form | sed 's#</Form>##' | cut -d'>' -f2 > wordforms
rm ./*.xml RELEASE-20230920.zip
```
Then run:
```
cat wordforms | python3 find_ambiguous.py - > ambiguous
```

How it works:
- Not all wordforms in GrammarDB are properly accentuated. The file `patterns` is a manually labeled override for such wordforms (or paradigms): each line is a wordform or prefix with the `+` sign after the stressed vowel.
- The script `find_ambiguous.py` reads all GrammarDB wordforms from stdin, reads all overriding patterns from `patterns`, applies patterns to wordforms, then writes the output files:
    - `unambiguous.dawg` is a [`dawg.IntDAWG`](https://dawg.readthedocs.io/en/latest/#intdawg-and-intcompletiondawg) with wordforms as keys and integer-encoded stress positions as values. The encoding is required because there may be more than one primary stress, e.g. in a compound word. For implementation details, see the functions `encode_accents` and `decode_accents`.
    - `ambiguous.dawg` is a [`dawg.DAWG`](https://dawg.readthedocs.io/en/latest/#dawg-and-completiondawg) of homographs, i.e. wordforms that can be stressed in at least two distinct ways (typically because of different lexical meanings or grammatical forms).
    - `ambiguous` is a human-readable listing of homographs, a tab-separated file with wordforms in the first column and all their respective accentuation variants in the second column, pipe-delimited.
    - `unmatched` is a list of non-accentuated GrammarDB wordforms that haven't been covered in the override. Various cases fall into this category, such as typos (*ссыльнапалітымчных*), homographs (*вібрапліты*), multiword entities (*ані аб кім*), clitics with no vowels to stress (*з*), but most are just normal words that should be accentuated.
- To update `patterns`, copy the wordforms you'd wish to accentuate from `unmatched`, label them with `+` signs, and reduce multiple wordforms to their common prefix when they're all accentuated the same (e.g. the prefix `калатнё+` would capture both *калатнёй* and *калатнёю*). Upon each update of `patterns`, you may want to run once again: `cat wordforms | python3 find_ambiguous.py - > ambiguous`
