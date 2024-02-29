import datetime
from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class Tranzactie(Entitate):
    """
    Creeaza o tranzactie
    """
    id_medicament: str
    id_card_client: str
    nr_bucati: str
    data_si_ora: str
