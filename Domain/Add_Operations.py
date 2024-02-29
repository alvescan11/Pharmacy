from Domain.Undo_Redo_Operations import UndoRedoOperations
from Domain.entitate import Entitate
from Repository.repository import Repository


class AddOperations(UndoRedoOperations):
    def __init__(self, repository: Repository,
                 obiectAdaugat: Entitate):
        self.repository = repository
        self.obiectAdaugat = obiectAdaugat

    def doUndo(self):
        self.repository.sterge(self.obiectAdaugat.id_entitate)

    def doRedo(self):
        self.repository.adauga(self.obiectAdaugat)
