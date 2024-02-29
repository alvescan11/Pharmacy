from typing import List

from Domain.Undo_Redo_Operations import UndoRedoOperations


class UndoRedoService:
    def __init__(self):
        self.undo_list: List[UndoRedoOperations] = []
        self.redo_list: List[UndoRedoOperations] = []

    def Add_Undo_Operations(self, undoRedoOperaions: UndoRedoOperations):
        self.undo_list.append(undoRedoOperaions)

    def undo(self):
        if self.undo_list:
            top_operation = self.undo_list.pop()
            top_operation.doUndo()
            self.redo_list.append(top_operation)

    def redo(self):
        if self.redo_list:
            top_operation = self.redo_list.pop()
            top_operation.doRedo()
            self.undo_list.append(top_operation)

    def clear_redo(self):
        self.redo_list.clear()
