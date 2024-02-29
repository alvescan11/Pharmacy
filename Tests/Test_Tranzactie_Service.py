import datetime

from Domain.card_client import CardClient
from Domain.card_client_Validator import CardClientValidator
from Domain.medicament import Medicament
from Domain.medicament_Validator import MedicamentValidator
from Domain.tranzactie import Tranzactie
from Domain.tranzactie_Validator import TranzactieValidator
from Repository.repository_Json import RepositoryJson
from Service.Undo_Redo_Service import UndoRedoService
from Service.card_client_Service import CardClientService
from Service.medicament_Service import MedicamentService
from Service.tranzactie_Service import TranzactieService
from ViewModel.Card_Client_cu_reducere import CardClientCuReducere
from ViewModel.Medicament_cu_nr_bucati import MedicamentCuNrBucati
from utils import clear_file


def test_tranzactie_service():
    filename1 = "test_tranzactie.json"
    filename3 = "test_card_client.json"
    filename2 = "test_medicament.json"
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
    tranzactie_service.adauga('1', '1', '1', '123', '11.12.2020 20:40:59')
    assert len(tranzactie_service.get_All()) == 1
    tranzactie_service.modifica('1', '1', 'nul', '123', '11.12.2020 20:40:59')
    for index in tranzactie_service.get_All():
        id = getattr(index, 'id_entitate')
        if id == '1':
            id_card = getattr(index, 'id_card_client')
    assert id_card == 'nul'
    tranzactie_service.sterge('1')
    assert len(tranzactie_service.get_All()) == 0


def test_cautare_full_text():
    filename1 = "test_tranzactie.json"
    filename3 = "test_card_client.json"
    filename2 = "test_medicament.json"
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
    card_validator = CardClientValidator()
    card_service = CardClientService(repository_card,
                                     card_validator,
                                     undoRedoService)
    card_service.adauga('2', 'Suciu', 'Sergiu',
                        '2341242143', '26.12.2000', '13.11.2020')
    tranzactie_service = TranzactieService(repository_tranzactie,
                                           tranzactie_validator,
                                           repository_medicament,
                                           repository_card,
                                           undoRedoService)
    assert tranzactie_service.Cautare_Full_Text('e') == \
           [Medicament('1', 'Paracetamol', 'DAWDAWD', '80.8', 'nu'),
            CardClient('2', 'Suciu', 'Sergiu',
                       '2341242143', '26.12.2000', '13.11.2020')]


def test_afisare_tranzactii_interval():
    filename1 = "test_tranzactie.json"
    filename3 = "test_card_client.json"
    filename2 = "test_medicament.json"
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
    tranzactie_service.adauga('1', '1', '1', '123', '11.12.2020 20:40:59')
    tranzactie_service.adauga('2', '2', 'nul', '23', '12.12.2017 20:40:59')
    tranzactie_service.adauga('3', '3', '1', '12', '12.02.2020 20:40:59')
    tranzactie_service.adauga('4', '1', 'nul', '13', '01.12.2019 20:40:59')
    data1 = datetime.datetime(2017, 1, 1)
    data2 = datetime.datetime(2019, 1, 1)
    assert tranzactie_service.Afisare_Tranzactii_Interval(data1, data2) == \
           [Tranzactie('2', '2', 'nul', '23', '12.12.2017 20:40:59')]


def test_ordonare_descrescator_dupa_nr_vanzari():
    filename1 = "test_tranzactie.json"
    filename3 = "test_card_client.json"
    filename2 = "test_medicament.json"
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
    medicament_service.adauga('1', 'Paracetamol', 'DAWDD', '80.8', 'nu')
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
    tranzactie_service.adauga('1', '1', '1', '123', '11.12.2020 20:40:59')
    tranzactie_service.adauga('2', '2', 'nul', '23', '12.12.2017 20:40:59')
    tranzactie_service.adauga('3', '3', '1', '12', '12.02.2020 20:40:59')
    tranzactie_service.adauga('4', '1', 'nul', '13', '01.12.2019 20:40:59')
    assert tranzactie_service.Ordonare_Descrescator_Dupa_Nr_Vanzari() == [
        MedicamentCuNrBucati('1', 'Paracetamol', 'DAWDD', 80.8, 'nu', 136),
        MedicamentCuNrBucati('2', 'Antibiotic', 'DAWD', 100.8, 'nu', 23),
        MedicamentCuNrBucati('3', 'Parasinus', 'DDAWD', 90.0, 'da', 12)]


def test_stergerea_tranzactiilor_interval():
    filename1 = "test_tranzactie.json"
    filename3 = "test_card_client.json"
    filename2 = "test_medicament.json"
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
    assert tranzactie_service.get_All() == \
           [Tranzactie('1', '1', '1', '1', '11.12.2020 20:40:59'),
            Tranzactie('3', '3', '1', '1', '12.02.2020 20:40:59')]


def test_ordonare_descrescator_val_reduceri():
    filename1 = "test_tranzactie.json"
    filename3 = "test_card_client.json"
    filename2 = "test_medicament.json"
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
    tranzactie_service.adauga('2', '2', '2', '1', '12.12.2017 20:40:59')
    tranzactie_service.adauga('3', '3', '3', '1', '12.02.2020 20:40:59')
    tranzactie_service.adauga('4', '2', '1', '1', '01.12.2019 20:40:59')
    assert tranzactie_service.Ordonare_Descrescator_Val_Reduceri() == \
           [CardClientCuReducere('1', 'Suciu', 'Sergiu',
                                 '2341242143',
                                 '26.12.2000',
                                 '13.11.2020',
                                 163.44),
            CardClientCuReducere('2', 'Filip', 'Viorel',
                                 '2342143',
                                 '26.12.2000',
                                 '13.11.2020',
                                 90.72),
            CardClientCuReducere('3', 'Dorel', 'Iancu',
                                 '231242143',
                                 '26.12.2000',
                                 '13.11.2020', 76.5)
            ]


def test_stergere_in_cascada():
    filename1 = "test_tranzactie.json"
    filename3 = "test_card_client.json"
    filename2 = "test_medicament.json"
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
    tranzactie_service.Stergere_In_Cascada('1')

    assert tranzactie_service.get_All() == \
           [Tranzactie('3', '3', '3', '1', '12.02.2020 20:40:59')]
