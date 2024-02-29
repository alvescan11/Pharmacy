from Domain.medicament import Medicament


class MedicamentValidatorError(Exception):
    pass


class MedicamentValidator:

    def validator(self, medicament: Medicament) -> None:
        """
        Valideaza daca atributele medicamentului sunt bune sau nu
        :param medicament: un obiect de tipul Medicament
        :return:
        """
        erori = []
        pret = float(medicament.pret)
        if pret <= 0:
            erori.append("Pretul trebuie sa fie strict pozitiv")
        if medicament.reteta not in ["da", "nu"]:
            erori.append("Reteta medicamet trebuie sa fie 'da' sau 'nu'")
        if len(erori) > 0:
            raise MedicamentValidatorError(erori)
