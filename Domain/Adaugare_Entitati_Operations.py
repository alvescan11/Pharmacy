from Domain.Undo_Redo_Operations import UndoRedoOperations
from Domain.entitate import Entitate
from Repository.repository import Repository


class AdaugareEntitatiOperations(UndoRedoOperations):
    def __init__(self, repository: Repository,
                 lista_entitati: list[Entitate]):
        self.repository = repository
        self.lista_entitati = lista_entitati

    def doUndo(self):
        for entity in self.lista_entitati:
            self.repository.sterge(entity.id_entitate)

    def doRedo(self):
        for entity in self.lista_entitati:
            self.repository.adauga(entity)
