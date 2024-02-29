from Domain.card_client import CardClient
from Domain.medicament import Medicament
from Domain.tranzactie import Tranzactie
from Repository.repository_Json import RepositoryJson
from utils import clear_file


def test_card_client_repository():
    filename = "test_card_client.json"
    clear_file(filename)
    cardClientRepositoryJson = RepositoryJson(filename)
    card1 = CardClient('1', 'Suciu', 'Sergiu', '4234234', '13.01.2002',
                       '12.11.2021')
    card2 = CardClient('2', 'Muresan', 'Andrei', '123222', '15.07.2001',
                       '11.11.2021')
    cardClientRepositoryJson.adauga(card1)
    cardClientRepositoryJson.adauga(card2)
    assert cardClientRepositoryJson.read('2') is not None
    card1_mod = CardClient('1', 'Marian', 'Sergiu', '4234234', '13.01.2002',
                           '12.11.2021')
    cardClientRepositoryJson.modifica(card1_mod)
    assert getattr(cardClientRepositoryJson.read('1'), 'nume') == 'Marian'


def test_medicament_repository():
    filename = "test_medicament.json"
    clear_file(filename)
    medicamentRepositoryJson = RepositoryJson(filename)
    medicament1 = Medicament('1', 'Paracetamol', 'DAWDAWD', '80.8', 'nu')
    medicament2 = Medicament('2', 'Antibiotic', 'TSEFSEF', '100.5', 'da')
    medicamentRepositoryJson.adauga(medicament1)
    medicamentRepositoryJson.adauga(medicament2)
    assert medicamentRepositoryJson.read('1') is not None
    assert medicamentRepositoryJson.read('2') is not None
    medicament1_modificat = Medicament('1', 'Parasinus', 'DAWDAWD', '80.8',
                                       'nu')
    medicamentRepositoryJson.modifica(medicament1_modificat)
    assert getattr(medicamentRepositoryJson.read('1'), 'nume') == 'Parasinus'


def test_tranzactie_repository():
    filename = 'test_tranzactie.json'
    clear_file(filename)
    tranzactieRepositoryJson = RepositoryJson(filename)
    tranzactie1 = Tranzactie('1', '1', '1', '123', '11.12.2020 20:40:59')
    tranzactie2 = Tranzactie('2', '1', '1', '12', '12.12.2020 16:35:51')
    tranzactieRepositoryJson.adauga(tranzactie1)
    tranzactieRepositoryJson.adauga(tranzactie2)
    assert tranzactieRepositoryJson.read(tranzactie1.id_entitate)\
           == tranzactie1
    assert tranzactieRepositoryJson.read(tranzactie2.id_entitate)\
           == tranzactie2
    try:
        tranzactie3 = Tranzactie('2', '1', '1', '12', '12.12.2020 16:35:51')
        tranzactieRepositoryJson.adauga(tranzactie3)
        assert False
    except Exception:
        assert True
    tranzactie1_modificat = Tranzactie('1', '1', '1', '234',
                                       '11.12.2020 20:40:59')
    tranzactieRepositoryJson.modifica(tranzactie1_modificat)
    assert getattr(tranzactieRepositoryJson.read('1'), 'nr_bucati') == '234'
