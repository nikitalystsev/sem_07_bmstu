def check_int(x: str):
    """
    Функция, которая возвращает True, если строка - целое число. Иначе - False
    :param x: потенциальное целое число
    :return: True, если строка - целое число. Иначе - False
    """
    if not x:
        return False

    x = x.replace('_', '')

    if x[0] == '-' or x[0] == '+':
        x = x[1:]

    return x.isdigit()


def check_float(x: str):
    """
    Проверка числа на float. Возвращает True, если число вещественное и
    False, если число нельзя привести к вещественному типу данных
    :param x: потенциальное вещественное число
    :return: True, если строка - вещественное число. Иначе - False
    """
    if not x:
        return False

    if x[0] == '-' or x[0] == '+':
        x = x[1:]

    point_split = x.split('.')

    if len(point_split) == 1:  # Нет точки
        exp_split = x.split('e')
        if len(exp_split) == 1:  # Нет е и нет точки
            return x.isdigit()
        elif len(exp_split) == 2:  # Есть один символ е и нет точки
            return (exp_split[0].isdigit() and (
                    exp_split[1][0] in '+-' and exp_split[1][1:].isdigit() or exp_split[1].isdigit()))
    elif len(point_split) == 2:  # Есть одна точка
        exp_split = point_split[1].split('e')
        if len(exp_split) == 1:  # Есть точка и нет е
            return point_split[0].isdigit() and exp_split[0].isdigit()
        elif len(exp_split) == 2:  # Есть точка и есть е
            return (point_split[0].isdigit() and exp_split[0].isdigit() and (
                    exp_split[1][0] in '+-' and exp_split[1][1:].isdigit() or exp_split[1].isdigit()))

    return False