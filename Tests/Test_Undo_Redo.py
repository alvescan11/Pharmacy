import datetime

from Domain.Stergere_In_Cascada_Operations import StergereInCascadaOperations
from Domain.card_client_Validator import CardClientValidator
from Domain.medicament import Medicament
from Domain.medicament_Validator import MedicamentValidator
from Domain.tranzactie_Validator import TranzactieValidator
from Repository.repository_Json import RepositoryJson
from Service.card_client_Service import CardClientService
from Service.medicament_Service import MedicamentService
from Service.tranzactie_Service import TranzactieService
from Service.Undo_Redo_Service import UndoRedoService
from utils import clear_file


def test_undo_redo_medicament_service():
    medicament_repository = RepositoryJson('test_undo_redo.json')
    medicament_validator = MedicamentValidator()
    undo_redo_service = UndoRedoService()
    medicament_service = MedicamentService(medicament_repository,
                                           medicament_validator,
                                           undo_redo_service)
    medic1 = Medicament('1', 'Sirop', 'SIROPURI', '123', 'da')
    medic2 = Medicament('2', 'Seren', 'SIROPURI', '123', 'nu')
    clear_file('test_undo_redo.json')
    medicament_service.adauga('1', 'Sirop', 'SIROPURI', '123', 'da')
    medicament_service.adauga('2', 'Seren', 'SIROPURI', '123', 'nu')
    assert len(medicament_service.get_All()) == 2
    medicament_service.undoRedoService.undo()
    assert len(medicament_service.get_All()) == 1
    medicament_service.undoRedoService.redo()
    assert len(medicament_service.get_All()) == 2

    medicament_service.sterge('2')
    assert len(medicament_service.get_All()) == 1
    medicament_service.undoRedoService.undo()
    assert len(medicament_service.get_All()) == 2
    medicament_service.undoRedoService.redo()
    assert len(medicament_service.get_All()) == 1

    medicament_service.modifica('1', 'Teraflu', 'SIROPURI', '123', 'da')
    assert medicament_service.get_All()[0].nume == 'Teraflu'
    medicament_service.undoRedoService.undo()
    assert medicament_service.get_All()[0].nume == 'Sirop'
    medicament_service.undoRedoService.redo()
    assert medicament_service.get_All()[0].nume == 'Teraflu'


def test_undo_redo_card_client_service():
    card_client_repository = RepositoryJson('test_undo_redo.json')
    card_client_validator = CardClientValidator()
    undo_redo_service = UndoRedoService()
    card_client_service = \
        CardClientService(card_client_repository,
                          card_client_validator, undo_redo_service)
    clear_file('test_undo_redo.json')
    card_client_service.adauga('1',
                               'Suciu',
                               'Sergiu',
                               '01234', '11.11.2020', '11.11.2002')
    card_client_service.adauga('2',
                               'Muris',
                               'Flav',
                               '23525', '11.11.2020', '11.11.2002')
    assert len(card_client_service.get_All()) == 2
    card_client_service.undoRedoService.undo()
    assert len(card_client_service.get_All()) == 1
    card_client_service.undoRedoService.redo()
    assert len(card_client_service.get_All()) == 2

    card_client_service.modifica('1',
                                 'Muntean',
                                 'Florina',
                                 '01234', '11.11.2020', '11.11.2002')
    assert card_client_service.get_All()[0].nume == 'Muntean'
    card_client_service.undoRedoService.undo()
    card_client_service.undoRedoService.redo()
    assert card_client_service.get_All()[0].nume == 'Muntean'

    card_client_service.sterge('1')
    assert len(card_client_service.get_All()) == 1
    card_client_service.undoRedoService.undo()
    assert len(card_client_service.get_All()) == 2
    card_client_service.undoRedoService.redo()
    assert len(card_client_service.get_All()) == 1


def test_undo_redo_tranzactie_service():
    medicament_repository = RepositoryJson('test_undo_redo_medicament.json')
    medicament_validator = MedicamentValidator()
    undo_redo_service = UndoRedoService()
    medicament_service = MedicamentService(medicament_repository,
                                           medicament_validator,
                                           undo_redo_service)
    clear_file('test_undo_redo_medicament.json')
    medicament_service.adauga('1', 'Sirop', 'SIROPURI', '123', 'da')
    medicament_service.adauga('2', 'Seren', 'SIROPURI', '123', 'nu')

    card_client_repository = RepositoryJson('test_undo_redo_card.json')
    card_client_validator = CardClientValidator()
    card_client_service = \
        CardClientService(card_client_repository,
                          card_client_validator, undo_redo_service)
    clear_file('test_undo_redo_card.json')
    card_client_service.adauga('1',
                               'Suciu',
                               'Sergiu',
                               '01234',
                               '11.11.2020', '11.11.2002')
    card_client_service.adauga('2',
                               'Muris',
                               'Flav',
                               '23525',
                               '11.11.2020', '11.11.2002')

    tranzactie_repository = RepositoryJson('test_undo_redo.json')
    tranzactie_validator = TranzactieValidator()
    tranzactie_service = TranzactieService(tranzactie_repository,
                                           tranzactie_validator,
                                           medicament_repository,
                                           card_client_repository,
                                           undo_redo_service)
    clear_file('test_undo_redo.json')
    tranzactie_service.adauga('1', '1', '1', '124', '11.11.1111 23:23:23')
    tranzactie_service.adauga('3', '2', '1', '1200', '22.12.2000 23:23:23')
    assert len(tranzactie_service.get_All()) == 2
    tranzactie_service.undoRedoService.undo()
    assert len(tranzactie_service.get_All()) == 1
    tranzactie_service.undoRedoService.redo()
    assert len(tranzactie_service.get_All()) == 2

    tranzactie_service.modifica('1', '1', '1', '12400', '11.11.1111 23:23:23')
    tranzactie_service.undoRedoService.undo()
    assert tranzactie_service.get_All()[0].nr_bucati == '124'
    tranzactie_service.undoRedoService.redo()
    assert tranzactie_service.get_All()[0].nr_bucati == '12400'

    tranzactie_service.sterge('1')
    assert tranzactie_service.tranzactieRepository.read('1') is None
    tranzactie_service.undoRedoService.undo()
    assert len(tranzactie_service.get_All()) == 2
    tranzactie_service.undoRedoService.redo()
    assert len(tranzactie_service.get_All()) == 1


def test_undo_redo_scumpire_cu_un_procentaj():
    medicament_repository = RepositoryJson('test_undo_redo_medicament.json')
    medicament_validator = MedicamentValidator()
    undo_redo_service = UndoRedoService()
    medicament_service = MedicamentService(medicament_repository,
                                           medicament_validator,
                                           undo_redo_service)
    clear_file('test_undo_redo_medicament.json')
    medicament_service.adauga('1', 'Sirop', 'SIROPURI', '100.0', 'da')
    medicament_service.adauga('2', 'Seren', 'SIROPURI', '90.0', 'nu')
    medicament_service.Scumpirea_Cu_Un_Procentaj(10, 1000)
    medicament_service.undoRedoService.undo()
    assert medicament_service.get_All()[0].pret == '100.0'
    assert medicament_service.get_All()[1].pret == '90.0'
    medicament_service.undoRedoService.redo()
    assert medicament_service.get_All()[0].pret == '110.0'
    assert medicament_service.get_All()[1].pret == '99.0'


def test_undo_redo_generare_entitati():
    tranzactie_repository = RepositoryJson('test_undo_redo.json')
    tranzactie_validator = TranzactieValidator()
    medicament_repository = RepositoryJson('test_undo_redo_medicament.json')
    medicament_validator = MedicamentValidator()
    undo_redo_service = UndoRedoService()
    medicament_service = MedicamentService(medicament_repository,
                                           medicament_validator,
                                           undo_redo_service)
    card_client_repository = RepositoryJson('test_undo_redo_card.json')
    clear_file('test_undo_redo.json')
    clear_file('test_undo_redo_medicament.json')
    tranzactie_service = TranzactieService(tranzactie_repository,
                                           tranzactie_validator,
                                           medicament_repository,
                                           card_client_repository,
                                           undo_redo_service)
    tranzactie_service.Generare_Entitati(12)
    tranzactie_service.undoRedoService.undo()
    assert len(medicament_repository.read()) == 0
    tranzactie_service.undoRedoService.redo()
    assert len(medicament_repository.read()) == 12


def test_undo_redo_stergerea_tranzactiilor_interval():
    filename1 = "test_undo_redo.json"
    filename3 = "test_undo_redo_card.json"
    filename2 = "test_undo_redo_medicament.json"
    clear_file(filename1)
    clear_file(filename2)
    clear_file(filename3)
    tranzactie_validator = TranzactieValidator()
    repository_tranzactie = RepositoryJson(filename1)
    repository_medicament = RepositoryJson(filename2)
    repository_card = RepositoryJson(filename3)
    medicament_validator = MedicamentValidator()
    undoRedoService = UndoRedoService()
    medicament_service = MedicamentService(repository_medicament,
                                           medicament_validator,
                                           undoRedoService)
    medicament_service.adauga('1', 'Paracetamol', 'DAWDAWD', '80.8', 'nu')
    medicament_service.adauga('2', 'Antibiotic', 'DAWD', '100.8', 'nu')
    medicament_service.adauga('3', 'Parasinus', 'DDAWD', '90.0', 'da')
    card_validator = CardClientValidator()
    card_service = CardClientService(repository_card,
                                     card_validator,
                                     undoRedoService)
    card_service.adauga('1', 'Suciu', 'Sergiu',
                        '2341242143', '26.12.2000', '13.11.2020')
    tranzactie_service = TranzactieService(repository_tranzactie,
                                           tranzactie_validator,
                                           repository_medicament,
                                           repository_card,
                                           undoRedoService)
    tranzactie_service.adauga('1', '1', '1', '1', '11.12.2020 20:40:59')
    tranzactie_service.adauga('2', '2', 'nul', '1', '12.12.2017 20:40:59')
    tranzactie_service.adauga('3', '3', '1', '1', '12.02.2020 20:40:59')
    tranzactie_service.adauga('4', '2', 'nul', '1', '01.12.2019 20:40:59')
    data1 = datetime.datetime(2017, 11, 12)
    data2 = datetime.datetime(2019, 12, 12)
    tranzactie_service.Stergerea_Tranzactiilor_Interval(data1, data2)
    assert len(tranzactie_service.get_All()) == 2
    tranzactie_service.undoRedoService.undo()
    assert len(tranzactie_service.get_All()) == 4
    tranzactie_service.undoRedoService.redo()
    assert len(tranzactie_service.get_All()) == 2


def test_undo_redo_sterge_in_cascada():
    filename1 = "test_undo_redo.json"
    filename3 = "test_undo_redo_card.json"
    filename2 = "test_undo_redo_medicament.json"
    clear_file(filename1)
    clear_file(filename2)
    clear_file(filename3)
    tranzactie_validator = TranzactieValidator()
    repository_tranzactie = RepositoryJson(filename1)
    repository_medicament = RepositoryJson(filename2)
    repository_card = RepositoryJson(filename3)
    medicament_validator = MedicamentValidator()
    undoRedoService = UndoRedoService()
    medicament_service = MedicamentService(repository_medicament,
                                           medicament_validator,
                                           undoRedoService)
    medicament_service.adauga('1', 'Paracetamol', 'DAWDAWD', '80.8', 'nu')
    medicament_service.adauga('2', 'Antibiotic', 'DAWD', '100.8', 'nu')
    medicament_service.adauga('3', 'Parasinus', 'DDAWD', '90.0', 'da')
    card_validator = CardClientValidator()
    card_service = CardClientService(repository_card,
                                     card_validator,
                                     undoRedoService)
    card_service.adauga('1', 'Suciu', 'Sergiu',
                        '2341242143', '26.12.2000', '13.11.2020')
    card_service.adauga('2', 'Filip', 'Viorel',
                        '2342143', '26.12.2000', '13.11.2020')
    card_service.adauga('3', 'Dorel', 'Iancu',
                        '231242143', '26.12.2000', '13.11.2020')
    tranzactie_service = TranzactieService(repository_tranzactie,
                                           tranzactie_validator,
                                           repository_medicament,
                                           repository_card,
                                           undoRedoService)
    tranzactie_service.adauga('1', '1', '1', '1', '11.12.2020 20:40:59')
    tranzactie_service.adauga('2', '1', '2', '1', '12.12.2017 20:40:59')
    tranzactie_service.adauga('3', '3', '3', '1', '12.02.2020 20:40:59')
    tranzactie_service.adauga('4', '1', '1', '1', '01.12.2019 20:40:59')
    tranzactii_id = tranzactie_service.Stergere_In_Cascada('1')
    medicament = medicament_service.medicamentRepository.read('1')
    medicament_service.sterge('1')
    undoRedoService.clear_redo()
    stergereInCascadaOperations = StergereInCascadaOperations(
        medicament_service.medicamentRepository,
        tranzactie_service.tranzactieRepository,
        medicament,
        tranzactii_id
    )
    undoRedoService.Add_Undo_Operations(
        stergereInCascadaOperations)
    assert len(medicament_service.get_All()) == 2
    assert len(tranzactie_service.get_All()) == 1
    tranzactie_service.undoRedoService.undo()
    assert len(medicament_service.get_All()) == 3
    assert len(tranzactie_service.get_All()) == 4
    tranzactie_service.undoRedoService.redo()
    assert len(medicament_service.get_All()) == 2
    assert len(tranzactie_service.get_All()) == 1
