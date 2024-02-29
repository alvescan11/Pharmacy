
from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class CardClient(Entitate):
    """
    Creeaza un card de client
    """
    nume: str
    prenume: str
    CNP: str
    data_nasterii: str
    data_inregistrare: str
