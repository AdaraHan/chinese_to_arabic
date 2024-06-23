CN_NUM = {
    '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
    '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
}

CN_UNIT = {
    '十': 10,
    '百': 100,
    '千': 1000,
    '万': 10000,
    '亿': 100000000,
}


def chinese_to_arabic_direct(cn) -> int:
    if not isinstance(cn, str):
        return cn  # 如果不是字符串，直接返回原值
    cn_str = str(cn)  # 确保cn是字符串
    arabic_list = [CN_NUM.get(char, str(char)) for char in cn_str]
    arabic_str = ''.join(str(i) for i in arabic_list)
    try:
        return int(arabic_str)
    except ValueError:
        return arabic_str  # 如果转换不成功，返回字符串格式


def chinese_to_arabic(cn: str) -> int:
    if not isinstance(cn, str):
        return cn  # 如果不是字符串，直接返回原值

    if cn.startswith("十") or cn.startswith("百"):
        cn = "一" + cn

    unit = 0
    ldig = []

    for cndig in reversed(cn):
        if cndig in CN_UNIT:
            if cndig == '十' and unit == 1:
                ldig.append(unit)
            unit = CN_UNIT.get(cndig)
        else:
            num = CN_NUM.get(cndig)
            if num is None:
                raise ValueError(f"Unrecognized Chinese numeral: {cndig}")
            if unit:
                num *= unit
                unit = 1
            ldig.append(num)
    return sum(ldig)
