from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class Medicament(Entitate):
    """
    Creeaza un medicament
    """
    nume: str
    producator: str
    pret: str
    reteta: str
