from typing import Protocol

from Domain.entitate import Entitate


class Repository(Protocol):
    def read(self, id_entitate=None):
        ...

    def adauga(self, entitate: Entitate) -> None:
        ...

    def sterge(self, id_entitate: str) -> None:
        ...

    def modifica(self, entitate: Entitate) -> None:
        ...
