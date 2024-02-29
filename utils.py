def clear_file(filename):
    with open(filename, "w"):
        pass


def my_sorted(iterable, key=None, reverse: bool = False):
    rez = iterable[:]
    for i in range(len(rez) - 1):
        for j in range(i + 1, len(rez)):
            if key is None:
                if rez[i] > rez[j]:
                    rez[i], rez[j] = rez[j], rez[i]
            else:
                if key(rez[i]) > key(rez[j]):
                    rez[i], rez[j] = rez[j], rez[i]

    if reverse is True:
        return rez[::-1]
    return rez
