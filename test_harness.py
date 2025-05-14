# Imports

import os
import csv
from random import shuffle

from tqdm import tqdm
from sentence_splitter import SentenceSplitter

from phonemizer_wrapper import phonemize, partially_expand, needs_gemini_expansion

# Functions

def process_lines(lines):
    lines_partially_expanded = [partially_expand(line) for line in tqdm(lines)]
    diff_indicators = [int(a != b) for a, b in zip(lines, lines_partially_expanded)]
    gemini_indicators = [int(needs_gemini_expansion(line)) for line in lines_partially_expanded]
    return lines_partially_expanded, diff_indicators, gemini_indicators

def write_output(path, lines, lines_partially_expanded, diff_indicators, gemini_indicators):
    with open(path, "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["line", "line_partially_expanded", "has_diff", "needs_gemini"])
        csv_writer.writerows(zip(lines, lines_partially_expanded, diff_indicators, gemini_indicators))

def sanity_check():
    inputs = [
        "У 1918–1991 гг., асабліва ў 2-й пал. XX ст., КП(б)Б надзяляла шмат увагі пытанням ЖКГ.",
        "Каля 1654 г. і пазней, у 1657 г., без дадатковых 20 тыс. чал. войска армія Рэчы Паспалітай, з яе 3 тыс. конніцы і 5 тыс. пяхоты, не магла эфектыўна супрацьстаяць ворагу.",
        "5-7 пялёсткаў кветкі разгортваюцца на працягу 1-2 дзён да агульнай плошчы ≈20 см².",
        "Ціск 120/80 і сатурацыя 97% – недасяжная мара для 2/3 насельніцтва, бо ўзровень Fe ў крыві значна адхіляецца ад нормы.",
        "У вайсковай школе не хапала вінтовачных прыкладаў для ўжывання ў якасці прыкладаў на занятках, і начальнік школы прыкладаў шмат намаганняў, каб палепшыць сітуацыю."
    ]
    outputs = [phonemize(x) for x in tqdm(inputs)]
    for i, o in zip(inputs, outputs):
        print("Input: ", i)
        print("Output:", o)

def flores_check():
    # Before running this, prepare the data files as described in ./validate/flores/README.md
    lines = []
    assert os.path.exists("./validate/flores/bel_Cyrl.dev")
    with open("./validate/flores/bel_Cyrl.dev") as f:
        lines += [line.strip() for line in f]
    assert os.path.exists("./validate/flores/bel_Cyrl.devtest")
    with open("./validate/flores/bel_Cyrl.devtest") as f:
        lines += [line.strip() for line in f]
    lines_partially_expanded, diff_indicators, gemini_indicators = process_lines(lines)
    _ = write_output("./validate/flores/intermediate.csv", lines, lines_partially_expanded, diff_indicators, gemini_indicators)

# Main loop

if __name__ == "__main__":
    _ = sanity_check()
    # _ = flores_check()
