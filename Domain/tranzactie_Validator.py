from Domain.tranzactie import Tranzactie


class TranzactieValidatorError(Exception):
    pass


class TranzactieValidator:

    def valideaza(self, tranzactie: Tranzactie) -> None:
        """
        Valideaza daca atributele tranzactiei sunt bune sau nu
        :param tranzactie: un obiect de tipul Tranzactie
        :return: None
        """
        erori = []
        nr = float(tranzactie.nr_bucati)
        if nr < 0:
            erori.append("Numarul de bucati trebuie sa fie mai mare decat"
                         " zero!")
        if len(erori) > 0:
            raise TranzactieValidatorError(erori)
