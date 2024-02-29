from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class MedicamentCuNrBucati(Entitate):
    nume: str
    producator: str
    pret: float
    reteta: str
    nr_bucati: int
