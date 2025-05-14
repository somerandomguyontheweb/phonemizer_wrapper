########################################################################
#                                                                      #
#  tokenization script for tagger preprocessing                        #
#  Original authors: Helmut Schmid, IMS, University of Stuttgart       #
#                    Serge Sharoff, University of Leeds                #
#  Converted to Python with Gemini 2.5 Pro (date: 2025.05.11)          #
#  Description:                                                        #
#  - splits input text into tokens (one token per line)                #
#  - cuts off punctuation, parentheses etc.                            #
#  - disambiguates periods                                             #
#  - preserves SGML markup                                             #
#                                                                      #
########################################################################

import sys
import re

# characters which have to be cut off at the beginning of a word
PChar_literal = '[¿¡{\'\\`"‚„†‡‹‘’“”•–—›»«'
PChar_re = f"[{re.escape(PChar_literal)}]"

# characters which have to be cut off at the end of a word
FChar_literal = ']}\'\`\",;:\!\?؟\%‚„…†‡‰‹‘’“”•–—›»«'
FChar_re = f"[{re.escape(FChar_literal)}]"

# character sequences which have to be cut off at the beginning of a word
PClitic = '' # This is a regex pattern string

# character sequences which have to be cut off at the end of a word
FClitic = '' # This is a regex pattern string

def ttg_tokenize(line):
    output_buffer = []

    # delete optional byte order markers (BOM)
    if line.startswith('\ufeff'):
        line = line[1:] # or line.removeprefix('\ufeff') in Python 3.9+
    # Note:
    # - In the original implementation, \ufeff is removed only in the first line of the input
    # - In the Python rewrite, \ufeff is removed in each line

    # replace newlines and tab characters with blanks
    line = line.replace('\n', ' ').replace('\t', ' ')

    # replace blanks within SGML tags
    sgml_space_placeholder = chr(255) # \377 is chr(255)
    while True:
        new_line = re.sub(r'(<[^<> ]*) ([^<>]*>)', rf'\1{sgml_space_placeholder}\2', line)
        if new_line == line:
            break
        line = new_line

    # replace whitespace with a special character
    segment_separator_placeholder = chr(254) # \376 is chr(254)
    line = line.replace(' ', segment_separator_placeholder)

    # restore SGML tags
    translation_table = str.maketrans(
        sgml_space_placeholder + segment_separator_placeholder,
        ' ' + sgml_space_placeholder
    )
    line = line.translate(translation_table)
    actual_segment_separator = sgml_space_placeholder

    # prepare SGML-Tags for tokenization
    line = re.sub(r'(<[^<>]*>)', rf'{actual_segment_separator}\1{actual_segment_separator}', line)

    if line.startswith(actual_segment_separator):
        line = line[len(actual_segment_separator):]

    if line.endswith(actual_segment_separator):
        line = line[:-len(actual_segment_separator)]

    line = re.sub(rf'{re.escape(actual_segment_separator)}{{2,}}', actual_segment_separator, line)

    S = line.split(actual_segment_separator)

    for current_segment in S:
        if not current_segment and actual_segment_separator == line:
            pass

        if re.fullmatch(r'<.*>', current_segment):
            output_buffer.append(current_segment + '\n')
        else:
            processed_segment = f" {current_segment} "

            # insert missing blanks after punctuation
            processed_segment = re.sub(r'(\.\.\.)', r' \1 ', processed_segment)

            processed_segment = re.sub(r'([;!?])([^ ])', r'\1 \2', processed_segment)

            F_words = processed_segment.split()

            for current_word_from_F in F_words:
                current_word = current_word_from_F
                suffix = ""

                # separate punctuation and parentheses from words
                finished = False
                while not finished:
                    original_word_in_loop = current_word # For complex replacements

                    # preceding parentheses
                    m = re.match(r'^(\()([^\)]*)(.)$', current_word)
                    if m:
                        output_buffer.append(m.group(1) + '\n')
                        current_word = m.group(2) + m.group(3)
                        continue

                    # following preceding parentheses
                    m = re.match(r'^([^(]+)(\))$', current_word)
                    if m:
                        current_word = m.group(1)
                        suffix = m.group(2) + '\n' + suffix
                        continue

                    # cut off preceding punctuation (Perl has two identical blocks here, likely a typo, one is enough)
                    m = re.match(rf'^({PChar_re})(.)', current_word)
                    if m:
                        output_buffer.append(m.group(1) + '\n')
                        current_word = m.group(2) + current_word[len(m.group(0)):]
                        continue

                    # cut off trailing punctuation
                    m = re.search(rf'(.)({FChar_re})$', current_word)
                    if m:
                        suffix = m.group(2) + '\n' + suffix
                        current_word = current_word[:-len(m.group(0))] + m.group(1)
                        continue

                    # cut off trailing periods if punctuation precedes
                    pattern_trailing_period = rf"({FChar_re}|\))\.$"
                    m = re.search(pattern_trailing_period, current_word)
                    if m:
                        char_before_period = m.group(1)
                        current_word = current_word[:m.start()]
                        suffix = ".\n" + suffix

                        if not current_word:
                            current_word = char_before_period
                        else:
                            suffix = char_before_period + "\n" + suffix
                        continue

                    finished = True

                # abbreviations of the form A. or U.S.A.
                if re.fullmatch(r'([A-Za-z-]\.)+$', current_word):
                    output_str_abbr = current_word + '\n'
                    if suffix:
                        output_str_abbr += suffix
                    output_buffer.append(output_str_abbr)
                    continue

                # disambiguate periods
                match_period_disamb = re.fullmatch(r'(..*)\.', current_word)
                # is_numeric_dot = re.fullmatch(r'[0-9]+\.', current_word)

                if match_period_disamb and current_word != "...":
                    current_word = match_period_disamb.group(1)
                    suffix = ".\n" + suffix

                # cut off clitics
                while True:
                    m = re.match(r'^(--)(.)', current_word)
                    if m:
                        output_buffer.append(m.group(1) + '\n')
                        current_word = m.group(2) + current_word[len(m.group(0)):]
                    else:
                        break

                if PClitic:
                    while True:
                        m = re.match(rf'^({PClitic})(.)', current_word, re.IGNORECASE)
                        if m:
                            output_buffer.append(m.group(1) + '\n')
                            current_word = m.group(2) + current_word[len(m.group(0)):]
                        else:
                            break

                while True:
                    m = re.search(r'(.)(--)$', current_word)
                    if m:
                        suffix = m.group(2) + '\n' + suffix
                        current_word = current_word[:-len(m.group(0))] + m.group(1)
                    else:
                        break

                if FClitic:
                    while True:
                        m = re.search(rf'(.)({FClitic})$', current_word, re.IGNORECASE)
                        if m:
                            suffix = m.group(2) + '\n' + suffix
                            current_word = current_word[:-len(m.group(0))] + m.group(1)
                        else:
                            break

                output_str_final = ""
                if current_word or not suffix:
                    output_str_final += current_word + '\n'
                if suffix:
                     output_str_final += suffix

                final_combined_output = current_word + '\n' + suffix
                output_buffer.append(final_combined_output)

    return "".join(output_buffer)

# main loop
if __name__ == "__main__":
    for line_bytes in sys.stdin.buffer:
        line = line_bytes.decode('utf-8')
        sys.stdout.buffer.write(ttg_tokenize(line).encode('utf-8'))
