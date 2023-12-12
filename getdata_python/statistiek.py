def mean(lst, totaal=0):
    """
    Bepaal het gemiddelde van een lijst getallen.

    Args:
        lst (list): Een lijst met gehele getallen.

    Returns:
        float: Het gemiddelde van de gegeven getallen.
    """
    return sum(lst) / len(lst)


def rnge(lst):
    """
    Bepaal het bereik van een lijst getallen.

    Args:
        lst (list): Een lijst met gehele getallen.

    Returns:
        int: Het bereik van de gegeven getallen.
    """
    return max(lst) - min(lst)


def median(lst):
    """
    Bepaal de mediaan van een lijst getallen.

    Args:
        lst (list): Een lijst met gehele getallen.

    Returns:
        float: De mediaan van de gegeven getallen.
    """
    lst.sort()
    if len(lst) % 2 == 0:
        indexfirst = (len(lst) / 2) // 1 - 1
        indexlast = indexfirst + 1
        return float((lst[int(indexfirst)] + lst[int(indexlast)]) / 2)

    if len(lst) % 2 == 1:
        index = ((len(lst) / 2) // 1)
        return float(lst[int(index)])


def q1(lst):
    """
    Bepaal het eerste kwartiel Q1 van een lijst getallen.

    Hint: maak gebruik van `median()`

    Args:
        lst (list): Een lijst met gehele getallen.

    Returns:
        float: Het eerste kwartiel Q1 van de gegeven getallen.
    """
    lst.sort()
    index = int(((len(lst) / 2) // 1))
    return float(median(lst[:int(index)]))


def q3(lst):
    """
    Bepaal het derde kwartiel Q3 van een lijst getallen.

    Args:
        lst (list): Een lijst met gehele getallen.

    Returns:
        float: Het derde kwartiel Q3 van de gegeven getallen.
    """
    lst.sort()
    index = 0
    if len(lst) % 2 == 1:
        index = int(((len(lst) / 2) // 1) + 1)
    if len(lst) % 2 == 0:
        index = int((len(lst) / 2))

    return float(median(lst[int(index):]))


def var(lst, tussen=0):
    """
    Bepaal de variantie van een lijst getallen.

    Args:
        lst (list): Een lijst met gehele getallen.

    Returns:
        float: De variantie van de gegeven getallen.
    """
    gemiddelde = mean(lst)
    for instantie in lst:
        tussen += ((instantie - gemiddelde) ** 2)
    return tussen / len(lst)


def std(lst):
    """
    Bepaal de standaardafwijking van een lijst getallen.

    Args:
        lst (list): Een lijst met gehele getallen.

    Returns:
        float: De standaardafwijking van de gegeven getallen.
    """
    return var(lst) ** 0.5


def freq(lst, aantal={}):
    """
    Bepaal de frequenties van alle getallen in een lijst.

    Args:
        lst (list): Een lijst met gehele getallen.

    Returns:
        dict: Een dictionary met als 'key' de waardes die voorkomen in de lijst
            en als 'value' het aantal voorkomens (de frequentie) van die waarde.
    """
    for getal in lst:
        if getal in aantal:
            aantal[getal] += 1
        else:
            aantal[getal] = 1
    return aantal


def modes(lst, modi=[], nieuwdict={}):
    """
    Bepaal alle modi van een lijst getallen.

    Hint: maak gebruik van `freq()`.

    Args:
        lst (list): Een lijst met gehele getallen.

    Returns:
        list: Een gesorteerde lijst van de modi van de gegeven getallen.
    """
    for getal in lst:
        nieuwdict.setdefault(getal, 0)
        nieuwdict[getal] += 1
    maxim = max(nieuwdict.values())
    for getal, aantal in nieuwdict.items():
        if aantal == maxim:
            modi.append(getal)
    return sorted(modi)
