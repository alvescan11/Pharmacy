from Domain.Undo_Redo_Operations import UndoRedoOperations
from Repository.repository import Repository


class DeleteOperations(UndoRedoOperations):
    def __init__(self, repository: Repository, obiectSters):
        self.repository = repository
        self.obiectSters = obiectSters

    def doUndo(self):
        self.repository.adauga(self.obiectSters)

    def doRedo(self):
        self.repository.sterge(self.obiectSters.id_entitate)
