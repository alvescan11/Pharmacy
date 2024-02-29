from Domain.medicament import Medicament
from Domain.medicament_Validator import MedicamentValidator
from Repository.repository_Json import RepositoryJson
from Service.Undo_Redo_Service import UndoRedoService
from Service.medicament_Service import MedicamentService
from utils import clear_file


def test_medicament_service():
    filename = "test_medicament.json"
    clear_file(filename)
    medicament_validator = MedicamentValidator()
    medicament_repository = RepositoryJson(filename)
    undoRedoService = UndoRedoService()
    medicament_service = MedicamentService(medicament_repository,
                                           medicament_validator,
                                           undoRedoService)
    medicament_service.adauga('1', 'Paracetamol', 'DAWDAWD', '80.8', 'nu')
    assert len(medicament_service.get_All()) == 1
    medicament_service.modifica('1', 'Antibiotic', 'TSEFSEF', '80.8', 'nu')
    for index in medicament_service.get_All():
        id = getattr(index, 'id_entitate')
        if id == '1':
            nume = getattr(index, 'nume')
    assert nume == 'Antibiotic'
    medicament_service.sterge('1')
    assert len(medicament_service.get_All()) == 0


def test_scumpirea_cu_un_procentaj():
    filename = "test_medicament.json"
    clear_file(filename)
    medicament_validator = MedicamentValidator()
    medicament_repository = RepositoryJson(filename)
    undoRedoService = UndoRedoService()
    medicament_service = MedicamentService(medicament_repository,
                                           medicament_validator,
                                           undoRedoService)
    medicament_service.adauga('1', 'Paracetamol', 'DAWDAWD', '100.0', 'nu')
    medicament_service.Scumpirea_Cu_Un_Procentaj(10, 110)
    lista = medicament_service.get_All()
    for med in lista:
        pret = getattr(med, 'pret')
        pret = float(pret)
    assert pret == 110.0
