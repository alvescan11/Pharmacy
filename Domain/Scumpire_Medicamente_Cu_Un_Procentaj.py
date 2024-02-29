from Domain.Undo_Redo_Operations import UndoRedoOperations
from Domain.entitate import Entitate
from Repository.repository import Repository


class ScumpireMedicamenteCuUnProcentaj(UndoRedoOperations):
    def __init__(self, repository: Repository,
                 lista_veche: list[Entitate],
                 lista_noua: list[Entitate]):
        self.repository = repository
        self.lista_veche = lista_veche
        self.lista_noua = lista_noua

    def doUndo(self):
        for entitate in self.lista_veche:
            self.repository.modifica(entitate)

    def doRedo(self):
        for entitate in self.lista_noua:
            self.repository.modifica(entitate)
