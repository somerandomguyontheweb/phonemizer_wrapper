# Constants

CASES = "NGDAIL"
CASE_MAPPING = {c: i for i, c in enumerate(CASES)}  # {"N": 0, "G": 1, ...}

POWER_MAPPING = {
    3: {
        "sg": ["тысяча", "тысячы", "тысячы", "тысячу", "тысячай", "тысячы"],
        "pl": ["тысячы", "тысяч", "тысячам", "тысячы", "тысячамі", "тысячах"],
    },
    6: {
        "sg": ["мільён", "мільёна", "мільёну", "мільён", "мільёнам", "мільёне"],
        "pl": ["мільёны", "мільёнаў", "мільёнам", "мільёны", "мільёнамі", "мільёнах"],
    },
    9: {
        "sg": ["мільярд", "мільярда", "мільярду", "мільярд", "мільярдам", "мільярдзе"],
        "pl": [
            "мільярды",
            "мільярдаў",
            "мільярдам",
            "мільярды",
            "мільярдамі",
            "мільярдах",
        ],
    },
}

NUMBER_MAPPING = {
    0: ["нуль", "нуля", "нулю", "нуль", "нулём", "нулі"],
    1: {
        "m": ["адзін", "аднаго", "аднаму", "адзін", "адным", "адным"],
        "f": ["адна", "адной", "адной", "адну", "адной", "адной"],
    },
    2: {
        "m": ["два", "двух", "двум", "два", "двума", "двух"],
        "f": ["дзве", "дзвюх", "дзвюм", "дзве", "дзвюма", "дзвюх"],
    },
    3: ["тры", "трох", "тром", "тры", "трыма", "трох"],
    4: ["чатыры", "чатырох", "чатыром", "чатыры", "чатырма", "чатырох"],
    5: ["пяць", "пяці", "пяці", "пяць", "пяццю", "пяці"],
    6: ["шэсць", "шасці", "шасці", "шэсць", "шасцю", "шасці"],
    7: ["сем", "сямі", "сямі", "сем", "сямю", "сямі"],
    8: ["восем", "васьмі", "васьмі", "восем", "васьмю", "васьмі"],
    9: ["дзевяць", "дзевяці", "дзевяці", "дзевяць", "дзевяццю", "дзевяці"],
    10: ["дзесяць", "дзесяці", "дзесяці", "дзесяць", "дзесяццю", "дзесяці"],
    11: [
        "адзінаццаць",
        "адзінаццаці",
        "адзінаццаці",
        "адзінаццаць",
        "адзінаццаццю",
        "адзінаццаці",
    ],
    12: [
        "дванаццаць",
        "дванаццаці",
        "дванаццаці",
        "дванаццаць",
        "дванаццаццю",
        "дванаццаці",
    ],
    13: [
        "трынаццаць",
        "трынаццаці",
        "трынаццаці",
        "трынаццаць",
        "трынаццаццю",
        "трынаццаці",
    ],
    14: [
        "чатырнаццаць",
        "чатырнаццаці",
        "чатырнаццаці",
        "чатырнаццаць",
        "чатырнаццаццю",
        "чатырнаццаці",
    ],
    15: [
        "пятнаццаць",
        "пятнаццаці",
        "пятнаццаці",
        "пятнаццаць",
        "пятнаццаццю",
        "пятнаццаці",
    ],
    16: [
        "шаснаццаць",
        "шаснаццаці",
        "шаснаццаці",
        "шаснаццаць",
        "шаснаццаццю",
        "шаснаццаці",
    ],
    17: [
        "сямнаццаць",
        "сямнаццаці",
        "сямнаццаці",
        "сямнаццаць",
        "сямнаццаццю",
        "сямнаццаці",
    ],
    18: [
        "васямнаццаць",
        "васямнаццаці",
        "васямнаццаці",
        "васямнаццаць",
        "васямнаццаццю",
        "васямнаццаці",
    ],
    19: [
        "дзевятнаццаць",
        "дзевятнаццаці",
        "дзевятнаццаці",
        "дзевятнаццаць",
        "дзевятнаццаццю",
        "дзевятнаццаці",
    ],
    20: ["дваццаць", "дваццаці", "дваццаці", "дваццаць", "дваццаццю", "дваццаці"],
    30: ["трыццаць", "трыццаці", "трыццаці", "трыццаць", "трыццаццю", "трыццаці"],
    40: ["сорак", "сарака", "сарака", "сорак", "сарака", "сарака"],
    50: [
        "пяцьдзясят",
        "пяцідзесяці",
        "пяцідзесяці",
        "пяцьдзясят",
        "пяццюдзесяццю",
        "пяцідзесяці",
    ],
    60: [
        "шэсцьдзясят",
        "шасцідзесяці",
        "шасцідзесяці",
        "шэсцьдзясят",
        "шасцюдзесяццю",
        "шасцідзесяці",
    ],
    70: [
        "семдзесят",
        "сямідзесяці",
        "сямідзесяці",
        "семдзесят",
        "сямюдзесяццю",
        "сямідзесяці",
    ],
    80: [
        "восемдзесят",
        "васьмідзесяці",
        "васьмідзесяці",
        "восемдзесят",
        "васьмюдзесяццю",
        "васьмідзесяці",
    ],
    90: [
        "дзевяноста",
        "дзевяноста",
        "дзевяноста",
        "дзевяноста",
        "дзевяноста",
        "дзевяноста",
    ],
    100: ["сто", "ста", "ста", "сто", "ста", "ста"],
    200: ["дзвесце", "двухсот", "двумстам", "дзвесце", "двумастамі", "двухстах"],
    300: ["трыста", "трохсот", "тромстам", "трыста", "трымастамі", "трохстах"],
    400: [
        "чатырыста",
        "чатырохсот",
        "чатыромстам",
        "чатырыста",
        "чатырмастамі",
        "чатырохстах",
    ],
    500: ["пяцьсот", "пяцісот", "пяцістам", "пяцьсот", "пяццюстамі", "пяцістах"],
    600: ["шэсцьсот", "шасцісот", "шасцістам", "шэсцьсот", "шасцюстамі", "шасцістах"],
    700: ["семсот", "сямісот", "сямістам", "семсот", "сямюстамі", "сямістах"],
    800: [
        "восемсот",
        "васьмісот",
        "васьмістам",
        "восемсот",
        "васьмюстамі",
        "васьмістах",
    ],
    900: [
        "дзевяцьсот",
        "дзевяцісот",
        "дзевяцістам",
        "дзевяцьсот",
        "дзевяцістамі",
        "дзевяцістах",
    ],
}

ORD_GENDER_NUMBER_MAPPING = {"m": 0, "f": 1, "n": 2, "p": 3}

def mk_ord(stem, soft=False, stressed=False):
    v1 = "і" if soft else "ы"
    v2 = "о" if stressed else "я" if soft else "а"
    return [
        [stem+v1, stem+v2+"га", stem+v2+"му", stem+v1, stem+v1+"м", stem+v1+"м"],
        [stem+"ая"[soft and not stressed]+"я", stem+v2+"й", stem+v2+"й", stem+"ую"[soft and not stressed]+"ю", stem+v2+"й", stem+v2+"й"],
        [stem+v2+"е", stem+v2+"га", stem+v2+"му", stem+v2+"е", stem+v1+"м", stem+v1+"м"],
        [stem+v1+"я", stem+v1+"х", stem+v1+"м", stem+v1+"я", stem+v1+"мі", stem+v1+"х"]
    ]

CARD_TO_ORD_MAPPING = {
    "нуль": mk_ord("нуляв", stressed=True),
    "адзін": mk_ord("перш"),
    "два": mk_ord("друг", soft=True, stressed=True),
    "тры": mk_ord("трэц", soft=True),
    "чатыры": mk_ord("чацвёрт"),
    "пяць": mk_ord("пят"),
    "шэсць": mk_ord("шост"),
    "сем": mk_ord("сём"),
    "восем": mk_ord("восьм"),
    "дзевяць": mk_ord("дзявят"),
    "дзесяць": mk_ord("дзясят"),
    "адзінаццаць": mk_ord("адзінаццат"),
    "дванаццаць": mk_ord("дванаццат"),
    "трынаццаць": mk_ord("трынаццат"),
    "чатырнаццаць": mk_ord("чатырнаццат"),
    "пятнаццаць": mk_ord("пятнаццат"),
    "шаснаццаць": mk_ord("шаснаццат"),
    "сямнаццаць": mk_ord("сямнаццат"),
    "васямнаццаць": mk_ord("васямнаццат"),
    "дзевятнаццаць": mk_ord("дзевятнаццат"),
    "дваццаць": mk_ord("дваццат"),
    "трыццаць": mk_ord("трыццат"),
    "сорак": mk_ord("саракав", stressed=True),
    "пяцьдзясят": mk_ord("пяцідзясят"),
    "шэсцьдзясят": mk_ord("шасцідзясят"),
    "семдзесят": mk_ord("сямідзясят"),
    "восемдзесят": mk_ord("васьмідзясят"),
    "дзевяноста": mk_ord("дзевяност"),
    "сто": mk_ord("сот"),
    "дзвесце": mk_ord("двухсот"),
    "трыста": mk_ord("трохсот"),
    "чатырыста": mk_ord("чатырохсот"),
    "пяцьсот": mk_ord("пяцісот"),
    "шэсцьсот": mk_ord("шасцісот"),
    "семсот": mk_ord("сямісот"),
    "восемсот": mk_ord("васьмісот"),
    "дзевяцьсот": mk_ord("дзевяцісот"),
    "тысяча": mk_ord("тысячн"), "тысячы": mk_ord("тысячн"), "тысяч": mk_ord("тысячн"),
    "мільён": mk_ord("мільённ"), "мільёны": mk_ord("мільённ"), "мільёнаў": mk_ord("мільённ"),
    "мільярд": mk_ord("мільярдн"), "мільярды": mk_ord("мільярдн"), "мільярдаў": mk_ord("мільярдн"),
}

MAX_INT = 10 ** 12

# Functions

def to_cardinal(n, case):
    """
    Given integer n (between 0 and 10**12) and case (one of "NGDAIL"),
    produces Belarusian cardinal numeral in the specified case.
    """
    assert case in CASE_MAPPING, "No such case '%s'" % case
    assert type(n) == int and 0 <= n < MAX_INT, (
        "Specify an integer between 0 and %s" % MAX_INT
    )
    if n == 0:
        return NUMBER_MAPPING[n][CASE_MAPPING[case]]
    output = []
    digit_count = len(str(n))
    for power in range(3 * ((digit_count - 1) // 3), 0, -3):
        higher_digits, n = divmod(n, 10 ** power)
        if higher_digits > 0:
            output += small_n_to_cardinal(
                higher_digits, case, power == 3
            )  # needs feminine only with 10**3
            p_number, p_case = get_power_agreement(higher_digits, case)
            output.append(POWER_MAPPING[power][p_number][CASE_MAPPING[p_case]])
    output += small_n_to_cardinal(n, case, False)
    return " ".join(output)

def get_split_representation(n):
    hundreds = 100 * (n // 100)
    tens = 10 * ((n - hundreds) // 10)
    ones = n % 10
    return (
        [hundreds, tens + ones] if tens + ones <= 20 else [hundreds, tens, ones]
    )

def small_n_to_cardinal(n, case, needs_feminine):
    """
    Auxiliary function to produce cardinals between 1 and 999.
    Ensures feminine agreement with the power designation 'тысяча'.
    """
    split_representation = get_split_representation(n)
    output = [
        NUMBER_MAPPING[x][CASE_MAPPING[case]]
        for x in split_representation[:-1]
        if x > 0
    ]
    last_value = split_representation[-1]
    if last_value > 0:
        if last_value in (1, 2):
            gender = "f" if needs_feminine else "m"
            output.append(NUMBER_MAPPING[last_value][gender][CASE_MAPPING[case]])
        else:
            output.append(NUMBER_MAPPING[last_value][CASE_MAPPING[case]])
    return output

def get_power_agreement(n, case):
    """
    Auxiliary function to choose number and case for the power designation.
    """
    ones = n % 10
    dozens = n % 100
    if ones == 1 and dozens != 11:  # "дваццаць адна тысяча" but "адзінаццаць тысяч"
        return "sg", case
    elif case in ("N", "A"):
        return "pl", "N" if (2 <= ones <= 4 and not 12 <= dozens <= 14) else "G"
    else:
        return "pl", case

def get_last_nonzero(n, factor):
    mod_split_representation = get_split_representation((n // factor) % 10**3)
    # 1..19, 21..29, etc.
    if mod_split_representation[-1] != 0:
        return mod_split_representation[-1]
    # 20, 30, 40, etc.
    if len(mod_split_representation) == 3 and mod_split_representation[-2] != 0:
        return mod_split_representation[-2]
    # 100, 200, 300, etc.
    return mod_split_representation[0]

def get_submapping(last_nonzero, factor):
    assert last_nonzero in NUMBER_MAPPING
    if last_nonzero in [1, 2]:
        return NUMBER_MAPPING[last_nonzero]["f" if factor == 10**3 else "m"]
    return NUMBER_MAPPING[last_nonzero]

def fix_round_ordinal(n, ordinal):
    assert n % 10**3 == 0
    factor = 10**9 if n % 10**9 == 0 else 10**6 if n % 10**6 == 0 else 10**3
    root = {10**9: "мільярдн", 10**6: "мільённ", 10**3: "тысячн"}[factor]
    ordinal_words = ordinal.split(" ")
    assert ordinal_words[-1].startswith(root), (n, root, ordinal_words)
    last_nonzero = get_last_nonzero(n, factor)
    submapping = get_submapping(last_nonzero, factor)
    assert ordinal_words[-2] == submapping[CASE_MAPPING["N"]], (n, ordinal_words, submapping[CASE_MAPPING["N"]])
    ordinal_words[-2] = submapping[CASE_MAPPING["G"]] if last_nonzero > 2 else ["адна", "двух"][last_nonzero - 1]
    return " ".join(ordinal_words[:-1]) + ordinal_words[-1]

def to_ordinal(n, case, gn):
    """
    Given integer n (between 0 and 10**12), case (one of "NGDAIL"),
    and gender / number identifier (one of "mfnp"), produces
    Belarusian ordinal numeral in the specified case, gender, and number.
    """
    assert case in CASE_MAPPING, "No such case '%s'" % case
    assert gn in ORD_GENDER_NUMBER_MAPPING, "No such gender / number pair '%s'" % gn
    assert type(n) == int and 0 <= n < MAX_INT, (
        "Specify an integer between 0 and %s" % MAX_INT
    )
    cardinal = to_cardinal(n, "N").split(" ")
    prefix, suffix = " ".join(cardinal[:-1]), cardinal[-1]
    assert suffix in CARD_TO_ORD_MAPPING, (n, suffix)
    result = ((prefix + " ") if prefix else "") + CARD_TO_ORD_MAPPING[suffix][ORD_GENDER_NUMBER_MAPPING[gn]][CASE_MAPPING[case]]
    if result.startswith("адна тысяча "):
        result = result[5:]
    if n > 0 and n % 10**3 == 0:
        result = fix_round_ordinal(n, result)
    return result
