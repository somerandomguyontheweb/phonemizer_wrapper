# Imports

from string import digits, punctuation, ascii_lowercase
import re

from belarusian_numerals import to_cardinal, to_ordinal

# Constants and functions

is_number = lambda w: all(c in digits for c in w)
is_rnumber = lambda w: all(c in "IVXLCDM" for c in w) and re.match("(M{0,3})(C[DM]|D?C{0,3})(X[LC]|L?X{0,3})(I[VX]|V?I{0,3})$", w)
is_timeabbr = lambda w: w in ["г", "ст", "гг", "стст"]
is_ordabbr = lambda w: re.match(r"^[0-9]+\-(ы|га|му?|й|е|х)$", w, re.IGNORECASE)
is_measure = lambda w: re.match(r"^[0-9]+\-(секундн|хвілінн|гадзінн|дзённ|тыднёв|месячн|гадов|метров|кіламетров|градусн)(ы(мі?|[ях])?|а([яйе]|га|му)|ую)$", w, re.IGNORECASE)

is_ukrainian = lambda w: any(c in "їє" for c in w.lower()) or ("і" in w.lower() and "и" in w.lower())
is_polish = lambda w: any(c in "łńśęąó" for c in w.lower())
is_belarusian = lambda w: re.match(r"^[а-зй-шы-яёіў'\- ]+$", w, re.IGNORECASE)

def is_russian(w):
    if not re.match(r"^[а-яё\- ]+$", w, re.IGNORECASE):
        return False
    if not any(c in "аоуэыяёюеи" for c in w.lower()):
        return False
    # if any(c in "ўі" for c in w.lower()):
    #     return False
    if re.findall("[ищъ]|ть?ся$|[дтржшч][ьеёюя]|[бвп]ь|оё", w, re.IGNORECASE):
        return True
    if len(w) > 5 and "-" in w and re.findall("в[бвгджзкмптфхцчш]|фф", w, re.IGNORECASE):
        return True
    if "-" not in w and w.lower().count("о") > 2:
        return True
    return False

def classify_token(w: str) -> str:
    if is_number(w):
        return "digits"
    if all(c in punctuation for c in w):
        return "punctuation"
    if all(c in digits + punctuation + " " for c in w):
        return "digits_with_punctuation"
    if is_rnumber(w):
        return "rnumber"
    if is_polish(w):
        return "lang_pl"
    if all(c in ascii_lowercase + "'- " for c in w.lower()):
        return "latin"
    if is_russian(w):
        return "lang_ru"
    if is_ukrainian(w):
        return "lang_uk"
    if is_belarusian(w):
        return "lang_be"
    if "́" in w and is_belarusian(w.replace("́", "")):
        return "lang_be_accentuated"
    if "i" in w.lower() and is_belarusian(w.lower().replace("i", "і")):
        return "lang_be_sub_i"
    if re.findall(r"\. (by|ru|ua|pl|uk|nl|fr|de|org|net|com|info|gov)$", w, re.IGNORECASE):
        return "url"
    return "unknown"

prep_in = ["у", "ў", "У", "Ў"]
prep_since = ["з", "З", "ад", "Ад"]
prep_until = ["да", "Да"]
prep_until_acc = ["па", "Па"]
prep_since_until = set(prep_since + prep_until)
prep_approx = ["каля", "Каля", "звыш", "Звыш"]
prep_for = ["за", "За"]
prep_at = ["на", "На"]
exact_date_left = {".", ",", "(", ")", ":", ";", "( ;", "»", "[unk]", "на", "і", "а", "але", "аднак", "дзе"}
events = {
    "падзеі", "гісторыя",
    "утвораны", "адкрыты", "ліквідаваны", "скасаваны",
    "нарадзіліся", "памерлі", "нарадзіўся", "памёр", "нарадзілася", "памерла",
    "адбыўся", "адбылася", "адбылося",
}
year_L = ["годзе", "г"]
year_G = ["года", "г"]
year_A = ["год", "г"]
cent_L = ["стагоддзі", "ст"]
cent_G = ["стагоддзя", "ст", "стагоддзяў", "стст"]
year_cent_L = year_L + cent_L
year_cent_G = year_G + cent_G
months_L = [
    "студзені", "лютым", "сакавіку", "красавіку",
    "маі", "траўні", "чэрвені", "ліпені", "жніўні",
    "верасні", "кастрычніку", "лістападзе", "снежні"
]
months_G = [
    "студзеня", "лютага", "сакавіка", "красавіка",
    "мая", "траўня", "чэрвеня", "ліпеня", "жніўня",
    "верасня", "кастрычніка", "лістапада", "снежня"
]
dist_L = [
    "кіламетрах", "км", "метрах", "м",
    "сантыметрах", "см", "міліметрах", "мм",
    "мілях"
]

in_year_cond = lambda left, right: left in prep_in and right in year_cent_L
since_until_year_cond = lambda left, right: left in prep_since_until and right in year_cent_G
since_cond = lambda left, right: left in prep_since and right in prep_until_acc
until_year_acc_cond = lambda left, right: left in prep_until_acc and right in year_A
in_month_cond = lambda left, right: left in months_L and right in year_G
exact_month_cond = lambda left, right: left in months_G and (right in year_G or right in [".", ",", ")", "да", "па"])
exact_or_event_date_cond = lambda left, right: left.lower() in (exact_date_left | events) and right in months_G
since_until_date_cond = lambda left, right: left in prep_since_until and right in months_G
year_cent_mill_date_cond = lambda left, right: right in ["года", "стагоддзя", "тысячагоддзя"]
approx_cond = lambda left, right: left in prep_approx and right not in year_G
parenth_cond = lambda left, right: left == "(" and right == ")"
ic_cond = lambda left, right: left == "IC"
in_dist_cond = lambda left, right: left in prep_in and right in dist_L
since_until_other_cond = lambda left, right: left in prep_since and right in prep_until

ord_loc_masc_sg_rule = lambda x: to_ordinal(int(x), "L", "m")
ord_gen_masc_sg_rule = lambda x: to_ordinal(int(x), "G", "m")
ord_acc_masc_sg_rule = lambda x: to_ordinal(int(x), "A", "m")
card_nom_rule = lambda x: to_cardinal(int(x), "N")
card_gen_rule = lambda x: to_cardinal(int(x), "G")
card_loc_rule = lambda x: to_cardinal(int(x), "L")

rules = [
    (in_year_cond, ord_loc_masc_sg_rule),
    (since_until_year_cond, ord_gen_masc_sg_rule),
    (since_cond, ord_gen_masc_sg_rule),
    (until_year_acc_cond, ord_acc_masc_sg_rule),
    (in_month_cond, ord_gen_masc_sg_rule),
    (exact_month_cond, ord_gen_masc_sg_rule),
    (exact_or_event_date_cond, ord_gen_masc_sg_rule),
    (since_until_date_cond, ord_gen_masc_sg_rule),
    (year_cent_mill_date_cond, ord_gen_masc_sg_rule),
    (approx_cond, card_gen_rule),
    (parenth_cond, card_nom_rule),
    (ic_cond, card_nom_rule),
    (in_dist_cond, card_loc_rule),
    (since_until_other_cond, card_gen_rule),
]

# Borrowed from https://www.tutorialspoint.com/roman-to-integer-in-python
def roman_to_int(s):
    dct = {
        'I': 1, 'V': 5, 'X': 10,
        'L': 50, 'C': 100, 'D': 500, 'M': 1000,
        'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90,
        'CD': 400, 'CM':900
    }
    i = 0
    num = 0
    while i < len(s):
        if i + 1 < len(s) and s[i:i+2] in dct:
            num += dct[s[i:i+2]]
            i += 2
        else:
            assert s[i] in dct
            num += dct[s[i]]
            i += 1
    return num

cent_part_N = ["пачатак", "канец", "сярэдзіна", "палова", "трэць", "чвэрць", "гады"]
cent_part_G = ["канца", "сярэдзіны", "паловы", "гадоў"]
cent_part_L = ["пачатку", "канцы", "сярэдзіне", "палове", "трэці", "чвэрці", "гадах"]
cent_part_NGL = set(cent_part_N + cent_part_G + cent_part_L)
varia_G_n = ["стагоддзя", "стагоддзяў", "склікання", "скліканняў"]
varia_G_f = ["ступені"]
king_N_regular = [
    "Карл", "Генрых", "Людовік", "Фрыдрых",
    "Аляксандр", "Філіп", "Эдуард", "Альфонс",
    "Вільгельм", "Фердынанд", "Альбрэхт", "Жыгімонт", "Клімент"
]
king_N_irregular = ["Пётр", "Мікалай", "Георгій", "Густаў"]
king_N = set(king_N_regular + king_N_irregular)
king_G = set([s + "а" for s in king_N_regular] + ["Пятра", "Мікалая", "Георгія", "Густава"])
king_D = set([s + "у" for s in king_N_regular] + ["Пятру", "Мікалаю", "Георгію", "Густаву"])

in_cent_cond = lambda left, right: left in prep_in and right in cent_L
exact_cent_cond = lambda left, right: type(left) is str and left.lower() in cent_part_NGL and right in cent_G
since_until_cent_cond = lambda left, right: left in prep_since_until and right in cent_G
default_cent_cond = lambda left, right: right == "стагоддзе"
varia_gen_neut_cond = lambda left, right: right in varia_G_n
varia_gen_femn_cond = lambda left, right: right in varia_G_f
king_nom_cond = lambda left, right: left in king_N
king_gen_cond = lambda left, right: left in king_G
king_dat_cond = lambda left, right: left in king_D

r_ord_nom_masc_sg_rule = lambda x: to_ordinal(roman_to_int(x), "N", "m")
r_ord_gen_masc_sg_rule = lambda x: to_ordinal(roman_to_int(x), "G", "m")
r_ord_gen_femn_sg_rule = lambda x: to_ordinal(roman_to_int(x), "G", "f")
r_ord_dat_masc_sg_rule = lambda x: to_ordinal(roman_to_int(x), "N", "m")
r_ord_loc_masc_sg_rule = lambda x: to_ordinal(roman_to_int(x), "L", "m")
r_ord_nom_neut_sg_rule = lambda x: to_ordinal(roman_to_int(x), "N", "n")

rrules = [
    (in_cent_cond, r_ord_loc_masc_sg_rule),
    (exact_cent_cond, r_ord_gen_masc_sg_rule),
    (since_until_cent_cond, r_ord_gen_masc_sg_rule),
    (default_cent_cond, r_ord_nom_neut_sg_rule),
    (varia_gen_neut_cond, r_ord_gen_masc_sg_rule),
    (varia_gen_femn_cond, r_ord_gen_femn_sg_rule),
    (king_nom_cond, r_ord_nom_masc_sg_rule),
    (king_gen_cond, r_ord_gen_masc_sg_rule),
    (king_dat_cond, r_ord_dat_masc_sg_rule),
]

in_year_abbr_cond = lambda leftleft, left: leftleft in prep_in and is_number(left)
since_until_year_abbr_cond = lambda leftleft, left: leftleft in prep_since_until and is_number(left)
in_or_exact_month_abbr_cond = lambda leftleft, left: leftleft in months_L + months_G and is_number(left)
until_year_acc_abbr_cond = lambda leftleft, left: leftleft in prep_until_acc and is_number(left)
in_cent_abbr_cond = lambda leftleft, left: leftleft in prep_in and is_rnumber(left)
exact_cent_abbr_cond = lambda leftleft, left: type(leftleft) is str and leftleft.lower() in cent_part_NGL and is_rnumber(left)
since_until_cent_abbr_cond = lambda leftleft, left: leftleft in prep_since_until and is_rnumber(left)

a_gen_rule = lambda x: {"г": "года", "ст": "стагоддзя", "гг": "гадоў", "стст": "стагоддзяў"}.get(x)
a_acc_rule = lambda x: {"г": "год", "ст": "стагоддзе", "гг": "гады", "стст": "стагоддзі"}.get(x)
a_loc_rule = lambda x: {"г": "годзе", "ст": "стагоддзі", "гг": "гадах", "стст": "стагоддзях"}.get(x)

arules = [
    (in_year_abbr_cond, a_loc_rule),
    (since_until_year_abbr_cond, a_gen_rule),
    (in_or_exact_month_abbr_cond, a_gen_rule),
    (until_year_acc_abbr_cond, a_acc_rule),
    (in_cent_abbr_cond, a_loc_rule),
    (exact_cent_abbr_cond, a_gen_rule),
    (since_until_cent_abbr_cond, a_gen_rule),
]

ordrules = {
    "ы": lambda x: to_ordinal(int(x), "N", "m"),
    "га": lambda x: to_ordinal(int(x), "G", "m"),
    "му": lambda x: to_ordinal(int(x), "D", "m"),
    "м": lambda x: to_ordinal(int(x), "I", "m"),
    "й": lambda x: to_ordinal(int(x), "G", "f"),
    "е": lambda x: to_ordinal(int(x), "N", "n"),
    "х": lambda x: to_ordinal(int(x), "G", "p"),
}

length_measures = {
    "км": "кіламетраў",
    "м": "метраў",
    "см": "сантыметраў",
    "мм": "міліметраў",
}
upper_inds = {
    "²": "квадратных",
    "³": "кубічных"
}
varia = {
    "°": "градусаў",
    "C": "Цэльсія",
    "№": "нумар",
    "%": "адсоткаў",  # TODO
    "‰": "праміле",
    "=": "роўна",
    "нар": "нарадзіўся",  # TODO
    "†": "памёр",
    "інш": "іншае",
    "тыс": "тысяч",
    "000": "тысяч",
    "экз": "экзэмпляраў",
    "рэд": "рэдактар",
    "рэдкал": "рэдкалегія",
    "англ": "англійскае",
    "гг": "гады",
    "стст": "стагоддзі",
    "кг": "кілаграмы",
    "млрд": "мільярды",
    "гадз": "гадзіну",
    "ун-т": "універсітэт",
    "ун - т": "універсітэт",
    "&": "and",
    "×": "на",
    "$": "долараў",
    "£": "фунтаў",
    "€": "еўра",
    "*": "зорачка",
    "→": "стрэлка",
}

def expand_number_token(left, token, right, rules=rules):
    for cond, rule in rules:
        if cond(left, right):
            return rule(token)
    # Default cases - commented out to handle them with Gemini expansion
    # t_int = int(token)
    # if 1900 <= t_int <= 2025:
    #     return to_ordinal(t_int, "N", "m")
    # if t_int < 10**12:
    #     return to_cardinal(t_int, "N")
    return None

def expand_rnumber_token(left, token, right, rrules=rrules):
    for cond, rule in rrules:
        if cond(left, right):
            return rule(token)
    # Default case - commented out to handle them with Gemini expansion
    # return to_ordinal(roman_to_int(token), "N", "m")
    return None

def expand_timeabbr_token(leftleft, left, token, right, arules=arules):
    for cond, rule in arules:
        if cond(leftleft, left):
            return rule(token)
    return None

def expand_ordabbr_token(token, ordrules=ordrules):
    assert token.count("-") == 1
    lhs, rhs = token.split("-")
    assert rhs in ordrules
    return ordrules[rhs](lhs)

def expand_measure_token(token):
    assert token.count("-") == 1
    lhs, rhs = token.split("-")
    assert all(c in digits for c in lhs)
    lhs_numeral = to_cardinal(int(lhs), "G")
    if lhs_numeral.endswith("аднаго"):
        lhs_numeral = lhs_numeral[:-2]
    return lhs_numeral + " " + rhs
    # TODO: тысяча, мільён

def expand_token(leftleft, left, token, right, rules=rules, rrules=rrules):
    if is_number(token):
        t = expand_number_token(left, token, right, rules=rules)
        if t is not None:
            return t
    if is_rnumber(token):
        t = expand_rnumber_token(left, token, right, rrules=rrules)
        if t is not None:
            return t
    if is_timeabbr(token):
        t = expand_timeabbr_token(leftleft, left, token, right)
        if t is not None:
            return t
    if (is_number(leftleft) or is_rnumber(leftleft)) and is_timeabbr(left) and token == ".":
        return ""  # TODO: Avoid if the preceding abbreviation hasn't been expanded
    if is_ordabbr(token):
        return expand_ordabbr_token(token)
    if is_measure(token):
        return expand_measure_token(token)
    if token in length_measures and right in upper_inds:
        return length_measures[token]
    if left in length_measures and token in upper_inds:
        return upper_inds[token]
    if (token == "°" and right == "C") or (left == "°" and token == "C"):
        return varia[token]
    if token == "чал":
        if is_number(left) and left[-1] in "234" and not (len(left) > 1 and left[-2] == "1"):
            return "чалавекі"
        else:
            return "чалавек"
    if token in varia:
        return varia[token]
    return token

# TODO: ад 150 да 200
# TODO: ^25 студзеня
# TODO: у 11:30
# TODO: больш за 5
# TODO: н.э., з.д.
# TODO: ... 000 000
