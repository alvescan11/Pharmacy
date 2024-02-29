class DuplicateIDError(Exception):
    pass


class NoSuchIDError(Exception):
    pass


class DuplicateCNPError(Exception):
    pass


class IncorrectRange(Exception):
    pass


class ModifyTransaction(Exception):
    pass


class AddingTransaction(Exception):
    pass


class IncorrectData(ValueError):
    pass
