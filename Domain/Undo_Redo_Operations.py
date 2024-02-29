from abc import ABC


class UndoRedoOperations(ABC):
    def doUndo(self):
        ...

    def doRedo(self):
        ...
