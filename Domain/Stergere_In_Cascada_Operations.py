

from Domain.Undo_Redo_Operations import UndoRedoOperations
from Domain.entitate import Entitate
from Repository.repository import Repository


class StergereInCascadaOperations(UndoRedoOperations):
    def __init__(self, entitate_repository: Repository,
                 entitati_repository: Repository,
                 entitate_stearsa: Entitate,
                 lista_entitati_sterse: list[Entitate]):
        self.entitate_repository = entitate_repository
        self.entitati_repository = entitati_repository
        self.entitate_stearsa = entitate_stearsa
        self.lista_entitati_sterse = lista_entitati_sterse

    def doUndo(self):
        self.entitate_repository.adauga(self.entitate_stearsa)
        for entitate in self.lista_entitati_sterse:
            self.entitati_repository.adauga(entitate)

    def doRedo(self):
        self.entitate_repository.sterge(self.entitate_stearsa.id_entitate)
        for entitate in self.lista_entitati_sterse:
            self.entitati_repository.sterge(entitate.id_entitate)
