from Domain.Add_Operations import AddOperations
from Domain.Delete_Operations import DeleteOperations
from Domain.Modify_Operations import ModifyOperations
from Domain.Scumpire_Medicamente_Cu_Un_Procentaj\
    import ScumpireMedicamenteCuUnProcentaj
from Domain.medicament import Medicament
from Domain.medicament_Validator import MedicamentValidator

from Repository.repository import Repository
from Service.Undo_Redo_Service import UndoRedoService


class MedicamentService:
    def __init__(self, medicamentRepository: Repository,
                 medicamentValidator: MedicamentValidator,
                 undoRedoService: UndoRedoService):
        self.medicamentRepository = medicamentRepository
        self.medicamentValidator = medicamentValidator
        self.undoRedoService = undoRedoService

    def get_All(self):
        """
        Afiseaza lista de medicamente
        :return: Returneaza lista de medicamente
        """
        return self.medicamentRepository.read()

    def adauga(self, id_medicament: str, nume: str,
               producator: str, pret: str, reteta: str) -> None:
        """
        Adauga un obiect de tip Medicament in lista
        :param id_medicament: id-ul medicamentului
        :param nume: numele medicamentului
        :param producator: producatorul medicamentului
        :param pret: pretul medicamentului
        :param reteta: reteta (Daca necesita reteta sau nu)
        :return: None
        """
        medicament = Medicament(id_medicament, nume, producator,
                                pret, reteta)
        self.medicamentValidator.validator(medicament)
        self.medicamentRepository.adauga(medicament)
        self.undoRedoService.clear_redo()
        self.undoRedoService.Add_Undo_Operations(
            AddOperations(self.medicamentRepository, medicament))

    def sterge(self, id_medicament: str) -> None:
        """
        Sterge un obiect de tip Medicament din lista
        :param id_medicament: id-ul medicamentului
        :return: None
        """
        if self.medicamentRepository.read(id_medicament) is not None:
            medicament = self.medicamentRepository.read(id_medicament)
        self.medicamentRepository.sterge(id_medicament)
        self.undoRedoService.clear_redo()
        self.undoRedoService.Add_Undo_Operations(
            DeleteOperations(self.medicamentRepository, medicament))

    def modifica(self, id_medicament: str, nume: str,
                 producator: str, pret: str, reteta: str) -> None:
        """
        Modifica un obiect de tip Medicament din lista
        :param id_medicament: id-ul medicamentului
        :param nume: numele medicamentului
        :param producator: producatorul medicamentului
        :param pret: pretul medicamentului
        :param reteta: reteta (Daca necesita reteta sau nu)
        :return: None
        """
        if self.medicamentRepository.read(id_medicament) is not None:
            medicament_vechi = self.medicamentRepository.read(id_medicament)
        medicament = Medicament(id_medicament, nume, producator, pret,
                                reteta)
        self.medicamentValidator.validator(medicament)
        self.medicamentRepository.modifica(medicament)
        self.undoRedoService.clear_redo()
        self.undoRedoService.Add_Undo_Operations(
            ModifyOperations(self.medicamentRepository,
                             medicament_vechi, medicament))

    def Scumpirea_Cu_Un_Procentaj(self, procentaj: float, pret_comp: float):
        """
        Aceasta functie scumpeste cu un procentaj toate medicamentele
        care au pretul mai mic decat pret_comp
        :param procentaj: procentajul date de utilizator
        :param pret_comp: pretul cu care se compara pretul medicamentului
        """
        lista = self.medicamentRepository.read()
        for index in lista:
            pret = getattr(index, "pret")
            pret = float(pret)
            if pret < pret_comp:
                pret_final = pret + procentaj / 100 * pret
                medicament = Medicament(getattr(index, "id_entitate"),
                                        getattr(index, "nume"),
                                        getattr(index, "producator"),
                                        str(pret_final),
                                        getattr(index, "reteta"))
                self.medicamentRepository.modifica(medicament)
        lista_noua = self.medicamentRepository.read()

        self.undoRedoService.clear_redo()
        scumpire_cu_un_procentaj = ScumpireMedicamenteCuUnProcentaj(
             self.medicamentRepository,
             lista,
             lista_noua)
        self.undoRedoService.Add_Undo_Operations(scumpire_cu_un_procentaj)
