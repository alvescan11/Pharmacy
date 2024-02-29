from Domain.Undo_Redo_Operations import UndoRedoOperations
from Domain.entitate import Entitate
from Repository.repository import Repository


class ModifyOperations(UndoRedoOperations):
    def __init__(self, repository: Repository, obiectVechi: Entitate,
                 obiectNou: Entitate):
        self.repository = repository
        self.obiectVechi = obiectVechi
        self.obiectNou = obiectNou

    def doUndo(self):
        self.repository.modifica(self.obiectVechi)

    def doRedo(self):
        self.repository.modifica(self.obiectNou)
