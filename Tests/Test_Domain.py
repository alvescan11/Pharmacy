from Domain.card_client import CardClient
from Domain.medicament import Medicament
from Domain.tranzactie import Tranzactie


def test_tranzactie():
    tranzactie = Tranzactie('1', '1', '1', '12', '12.01.2021 23:01:45')
    assert tranzactie.id_entitate == '1'
    assert tranzactie.id_medicament == '1'
    assert tranzactie.id_card_client == '1'
    assert tranzactie.nr_bucati == '12'
    assert tranzactie.data_si_ora == '12.01.2021 23:01:45'


def test_medicament():
    medicament = Medicament('1', 'Paracetamol', 'dadaw', '120.0', 'da')
    assert medicament.id_entitate == '1'
    assert medicament.nume == 'Paracetamol'
    assert medicament.producator == 'dadaw'
    assert medicament.pret == '120.0'
    assert medicament.reteta == 'da'


def test_card():
    card = CardClient('1', 'Suciu', 'Sergiu', '1212333',
                      '12.01.2020', '13.11.2020')
    assert card.id_entitate == '1'
    assert card.nume == 'Suciu'
    assert card.prenume == 'Sergiu'
    assert card.CNP == '1212333'
    assert card.data_nasterii == '12.01.2020'
    assert card.data_inregistrare == '13.11.2020'
