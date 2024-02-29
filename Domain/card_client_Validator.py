from Domain.card_client import CardClient


class CardClientValidatorError(Exception):
    pass


class CardClientValidator:

    def valideaza(self, cardClient: CardClient) -> None:
        """
        Valideaza daca atributele cardului de client sunt bune sau nu
        :param cardClient: un obiect de tipul CardClient
        :return: None
        """
        erori = []
        ok = False
        for i in range(len(cardClient.CNP)):
            if cardClient.CNP[i].isalpha():
                ok = True
        if ok is True:
            erori.append("CNP-ul trebuie sa contina doar cifre")
        if len(erori) > 0:
            raise CardClientValidatorError(erori)
