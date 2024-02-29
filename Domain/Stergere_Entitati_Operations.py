from Domain.Undo_Redo_Operations import UndoRedoOperations
from Domain.entitate import Entitate
from Repository.repository import Repository


class StergereEntitatiOperations(UndoRedoOperations):
    def __init__(self, repository: Repository,
                 listaEntitati: list[Entitate]):
        self.repository = repository
        self.listaEntitati = listaEntitati

    def doUndo(self):
        for entitate in self.listaEntitati:
            self.repository.adauga(entitate)

    def doRedo(self):
        for entitate in self.listaEntitati:
            self.repository.sterge(entitate.id_entitate)
