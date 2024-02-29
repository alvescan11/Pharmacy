from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class CardClientCuReducere(Entitate):
    nume: str
    prenume: str
    CNP: str
    data_nasterii: str
    data_inregistrarii: str
    suma_reducere: float
