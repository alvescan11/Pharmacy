import datetime
import functools
from functools import reduce
from random import randrange, choice, uniform, sample

from Domain.Adaugare_Entitati_Operations import AdaugareEntitatiOperations
from Domain.Add_Operations import AddOperations
from Domain.Delete_Operations import DeleteOperations
from Domain.Modify_Operations import ModifyOperations
from Domain.Stergere_Entitati_Operations import StergereEntitatiOperations
from Domain.Stergere_In_Cascada_Operations import StergereInCascadaOperations
from Domain.medicament import Medicament
from Domain.tranzactie import Tranzactie
from Domain.tranzactie_Validator import TranzactieValidator
from Repository.Exceptii import IncorrectRange, ModifyTransaction, \
    AddingTransaction

from Repository.repository import Repository
from Service.Undo_Redo_Service import UndoRedoService
from ViewModel.Card_Client_cu_reducere import CardClientCuReducere
from ViewModel.Medicament_cu_nr_bucati import MedicamentCuNrBucati
from utils import my_sorted


class TranzactieService:

    def __init__(self, tranzactieRepository: Repository,
                 tranzactieValidator: TranzactieValidator,
                 medicamentRepository: Repository,
                 cardClientRepository: Repository,
                 undoRedoService: UndoRedoService):
        self.tranzactieRepository = tranzactieRepository
        self.medicamentRepository = medicamentRepository
        self.cardClientRepository = cardClientRepository
        self.tranzactieValidator = tranzactieValidator
        self.undoRedoService = undoRedoService

    def get_All(self):
        """
        Afiseaza lista de tranzactie
        :return: Returneaza lista de tranzactie
        """
        return self.tranzactieRepository.read()

    def adauga(self, id_tranzactie: str, id_medicament: str,
               id_card_client: str, nr_bucati: str, data_si_ora: str) -> None:
        """
        Adauga un obict de tip Tranzactie in lista
        :param id_tranzactie: id-ul tranzactie
        :param id_medicament: id-ul medicamentului
        :param id_card_client: id-ul cardului de client
        :param nr_bucati: numarul de bucati
        :param data_si_ora: data si ora la care s-a facut tranzactia
        :return: None
        """
        if self.medicamentRepository.read(id_medicament) is not None and \
                self.cardClientRepository.read(id_card_client) is not None:
            tranzactie = Tranzactie(id_tranzactie, id_medicament,
                                    id_card_client, nr_bucati, data_si_ora)
            self.tranzactieValidator.valideaza(tranzactie)
            self.tranzactieRepository.adauga(tranzactie)
            self.undoRedoService.Add_Undo_Operations(
                AddOperations(self.tranzactieRepository, tranzactie))

        elif self.medicamentRepository.read(id_medicament) is not None and \
                id_card_client == 'nul':
            tranzactie = Tranzactie(id_tranzactie, id_medicament,
                                    id_card_client, nr_bucati, data_si_ora)
            self.tranzactieValidator.valideaza(tranzactie)
            self.tranzactieRepository.adauga(tranzactie)
            self.undoRedoService.clear_redo()
            self.undoRedoService.Add_Undo_Operations(
                AddOperations(self.tranzactieRepository, tranzactie))
        else:
            raise AddingTransaction("Nu puteti adauga aceasta tranzactie!")

    def sterge(self, id_tranzactie: str) -> None:
        """
        Sterge un obiect de tip Tranzactie din lista
        :param id_tranzactie: id-ul tranzactiei
        :return: None
        """
        if self.tranzactieRepository.read(id_tranzactie) is not None:
            tranzactie = self.tranzactieRepository.read(id_tranzactie)
        self.tranzactieRepository.sterge(id_tranzactie)
        self.undoRedoService.clear_redo()
        self.undoRedoService.Add_Undo_Operations(
            DeleteOperations(self.tranzactieRepository, tranzactie))

    def modifica(self, id_tranzactie: str, id_medicament: str,
                 id_card_client: str, nr_bucati: str,
                 data_si_ora: str) -> None:
        """
        Adauga un obict de tip Tranzactie in lista
        :param id_tranzactie: id-ul tranzactie
        :param id_medicament: id-ul medicamentului
        :param id_card_client: id-ul cardului de client
        :param nr_bucati: numarul de bucati
        :param data_si_ora: data si ora la care s-a facut tranzactia
        :return: None
        """
        if self.medicamentRepository.read(id_medicament) is not None and \
                (self.cardClientRepository.read(id_card_client)
                 is not None or id_card_client == 'nul'):
            tranzactie_veche = self.tranzactieRepository.read(id_tranzactie)
            tranzactie = Tranzactie(id_tranzactie, id_medicament,
                                    id_card_client, nr_bucati, data_si_ora)
            self.tranzactieValidator.valideaza(tranzactie)
            self.tranzactieRepository.modifica(tranzactie)
            self.undoRedoService.clear_redo()
            self.undoRedoService.Add_Undo_Operations(
                ModifyOperations(self.tranzactieRepository,
                                 tranzactie_veche, tranzactie))
        else:
            raise ModifyTransaction("Nu puteti modifica aceasta tranzactie!")

    def Cautare_Full_Text(self, string: str):
        """
        Aceasta functie cauta un cuvant sau o portiune de cuvant
        in lista de medicamente sau in lista de clienti
        :param string: Cuvantul sau portiunea de cuvant pe care o cautam
        :return: Returneaza lista obiectelor care contin cuvantul cautat
        """
        list_medicamente = self.medicamentRepository.read()
        lista = []
        for index in list_medicamente:
            nume = getattr(index, 'nume')
            producator = getattr(index, 'producator')
            pret = getattr(index, 'pret')
            reteta = getattr(index, 'reteta')
            if string in nume:
                lista.append(index)
            elif string in producator:
                lista.append(index)
            elif string in str(pret):
                lista.append(index)
            elif string in reteta:
                lista.append(index)
        list_clienti = self.cardClientRepository.read()
        for index in list_clienti:
            nume = getattr(index, 'nume')
            prenume = getattr(index, 'prenume')
            CNP = getattr(index, 'CNP')
            data_nasterii = getattr(index, 'data_nasterii')
            data_inregistrarii = getattr(index, 'data_inregistrare')
            if string in nume:
                lista.append(index)
            elif string in prenume:
                lista.append(index)
            elif string in CNP:
                lista.append(index)
            elif string in str(data_nasterii):
                lista.append(index)
            elif string in str(data_inregistrarii):
                lista.append(index)
        return lista

    def get_data(self, tranzactie: Tranzactie):
        """
        Functia ne da data unei tranzactii in format datetime
        :param tranzactie: O tranzactie
        :return:
        """
        data_si_ora = tranzactie.data_si_ora
        data = data_si_ora.split(" ")[0]
        data_components = data.split('.')
        data = datetime.datetime(int(data_components[2]),
                                 int(data_components[1]),
                                 int(data_components[0]))
        return data

    def Afisare_Tranzactii_Interval(self, data1: datetime.datetime,
                                    data2: datetime.datetime):
        """
        Aceasta functie afiseaza toate tranzactiile care sunt facute
         intr-un interval dat
        :param data1: prima data a intervalului
        :param data2: a doua data a intervalului
        :return: lista de obiecte de tip Tranzactie care sunt in intervalul
         dat
        """
        if data2 < data1:
            raise IncorrectRange("Data2 trebuie sa fie mai mare decat data1")
        """lista_tranzactii_interval = []
                lista_tranzactii = self.tranzactieRepository.read()
                for index in lista_tranzactii:
                    data_str = getattr(index, 'data_si_ora')
                    data = data_str.split(" ")
                    data_mea = datetime.datetime(int(data[0][6:]),
                                                 int(data[0][3:5]),
                                                 int(data[0][0:2]))
                    if data_mea >= data1 and data_mea <= data2:
                        lista_tranzactii_interval.append(index)
                return lista_tranzactii_interval"""
        lista_tranzactii = self.get_All()
        lista_tranzactii_finala = [tranz for tranz in
                                   lista_tranzactii if
                                   data1 <= self.get_data(tranz) <= data2]
        return lista_tranzactii_finala

    def Generare_Entitati(self, numar: int):
        """
        Genereaza n entitati random
        :param numar: numarul de entitati pe care dorim sa le generam
        :return: Returneaza o lista cu cele n entitati
        """
        my_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                   'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'x', 'y', 'z']
        lista = []
        element = self.medicamentRepository.read()
        maxim = -1
        lista_elem = list(filter(lambda x: x.id_entitate, element))
        if len(lista_elem) != 0:
            maxim = functools.reduce(lambda a, b:
                                     a if int(
                                         getattr(a, 'id_entitate')) > int(
                                         getattr(b, 'id_entitate')) else b,
                                     lista_elem)
        else:
            maxim = Medicament('0', '0', '0', '0', 'da')
        entitati_adaugate = []
        for index in range(int(maxim.id_entitate) + 1,
                           int(maxim.id_entitate) + numar + 1):
            k = randrange(4, 10)
            nume = sample(my_list, k)
            nume_medicament = ""
            for i in nume:
                nume_medicament = nume_medicament + i
            producator = sample(my_list, k)
            prod = ""
            for y in producator:
                prod = prod + y
            id_medicament = str(randrange(index, index + 1))

            if id_medicament not in self.tranzactieRepository.read():
                medicament = Medicament(id_medicament,
                                        nume_medicament,
                                        prod,
                                        str(float
                                            (int
                                             (float
                                              (uniform(1.0,
                                                       300.0) * 1000)))
                                            / 1000),
                                        choice(['da', 'nu']))
                entitati_adaugate.append(medicament)
                self.medicamentRepository.adauga(medicament)
        self.undoRedoService.clear_redo()
        stergere_entitati = AdaugareEntitatiOperations(
            self.medicamentRepository,
            entitati_adaugate)
        self.undoRedoService.Add_Undo_Operations(stergere_entitati)

    def Ordonare_Descrescator_Dupa_Nr_Vanzari(self):
        """
        Ordoneaza descrescator medicamentele dupa numarul de vanzari
        :return: Lista sortata descrescator
        """
        """Numar_bucati_medicamente = {}
        for medicament in self.__medicamentRepository.read():
            Numar_bucati_medicamente[medicament.id_entitate] = []
        for tranzactie in self.tranzactieRepository.read():
            Numar_bucati_medicamente[tranzactie.id_medicament]. \
                append(tranzactie.nr_bucati)
        rezultat = []
        for id_medicament in Numar_bucati_medicamente:
            bucati = Numar_bucati_medicamente[id_medicament]
            suma = 0
            for bucata in bucati:
                suma = suma + float(bucata)
            if suma > 0:
                rezultat.append(
                    {"medicament": self.__medicamentRepository.
                        read(id_medicament),
                     "nr_vanzari": suma}
                )
            suma = 0
        return sorted(rezultat,
                      key=lambda y: y["nr_vanzari"], reverse=True)"""
        lista_medicamente = self.medicamentRepository.read()
        lista_tranzactii = self.get_All()
        result = []

        def medicamente_vanzare(lista_med: list[Medicament]):
            if not lista_med:
                return []
            medicament = lista_med[0]
            tranzactii_cu_id_med = filter(lambda tranz:
                                          tranz.id_medicament ==
                                          medicament.id_entitate,
                                          lista_tranzactii)
            numar_bucati = sum(int(tranzactie.nr_bucati) for tranzactie
                               in tranzactii_cu_id_med)
            nume = medicament.nume
            producator = medicament.producator
            pret = medicament.pret
            reteta = medicament.reteta
            medicament_cu_nr_bucati = MedicamentCuNrBucati(
                medicament.id_entitate,
                nume, producator,
                float(pret), reteta,
                numar_bucati)
            return [medicament_cu_nr_bucati] + medicamente_vanzare(
                lista_med[1:])

        result = medicamente_vanzare(lista_medicamente)
        return sorted(result, key=lambda x: x.nr_bucati, reverse=True)

    def Stergerea_Tranzactiilor_Interval(self, data1: datetime.datetime,
                                         data2: datetime.datetime):
        """
        Aceasta functie sterge toate tranzactiile dintr-un
        interval dat
        :param data1: prima data a intervalului
        :param data2: a doua data a intervalului
        :return: None
        """
        if data2 < data1:
            raise IncorrectRange("Data2 trebuie sa fie mai mare decat data1")
        tranzactii_sterse = []
        lista_tranzactii = self.get_All()
        lista_tranzactii_finala = list(tranz for tranz in
                                       lista_tranzactii if
                                       self.get_data(tranz) < data1 or
                                       self.get_data(tranz) > data2)
        for tranzactie in lista_tranzactii:
            if tranzactie not in lista_tranzactii_finala:
                tranzactii_sterse.append(tranzactie)
                self.tranzactieRepository.sterge(tranzactie.id_entitate)
        self.undoRedoService.clear_redo()
        stergere_entitati = StergereEntitatiOperations(
            self.tranzactieRepository,
            tranzactii_sterse)
        self.undoRedoService.Add_Undo_Operations(stergere_entitati)

    def Ordonare_Descrescator_Val_Reduceri(self):
        """
        Ordoneaza descrescator cardurile dupa valoarea reducerilor efectuate
        """
        """rezultat = []
        lista_tranzactii = self.tranzactieRepository.read()
        lista_carduri = self.cardClientRepository.read()
        lista_medicamente = self.medicamentRepository.read()
        for card_client in lista_carduri:
            tranzactii_cu_id_card = list(filter(
                lambda x: x.id_card_client == card_client.id_entitate,
                lista_tranzactii))
            suma_reducere = 0
            for tranz in tranzactii_cu_id_card:
                for medicament in lista_medicamente:
                    if tranz.id_medicament == medicament.id_entitate:
                        if medicament.reteta == 'DA':
                            suma_reducere += float(
                                float(medicament.pret)
                                * tranz.nr_bucati * 15) / 100
                        if medicament.reteta == 'NU':
                            suma_reducere += float(
                                float(medicament.pret)
                                * tranz.nr_bucati * 10) / 100
            nume = card_client.nume
            prenume = card_client.prenume
            CNP = card_client.CNP
            data_nasterii = card_client.data_nasterii
            data_inregistrarii = card_client.data_inregistrare
            rezultat.append(CardClientCuReducere(
                card_client.id_entitate, nume, prenume, CNP,
                data_nasterii, data_inregistrarii, suma_reducere))
        return sorted(rezultat,
                         key=lambda v: v.suma_reducere, reverse=True)"""
        Reduceri_Card = {}
        Nr_Bucati_Card = {}
        for card in self.cardClientRepository.read():
            Reduceri_Card[card.id_entitate] = []
            Nr_Bucati_Card[card.id_entitate] = []
        for tranzactie in self.tranzactieRepository.read():
            Reduceri_Card[tranzactie.id_card_client]. \
                append(tranzactie.id_medicament)
            Nr_Bucati_Card[tranzactie.id_card_client]. \
                append(tranzactie.nr_bucati)
        rezultat = []
        for index1 in Reduceri_Card:
            for index2 in Nr_Bucati_Card:
                if index1 == index2:
                    lista_id_med = Reduceri_Card.get(index1)
                    lista_nr_bucati = Nr_Bucati_Card.get(index2)
                    suma = 0
                    for i in range(len(lista_id_med)):
                        for j in range(len(lista_nr_bucati)):
                            if i == j:
                                for index in \
                                        self.medicamentRepository.read():
                                    if lista_id_med[i] == \
                                            getattr(index, "id_entitate"):
                                        pret = float(getattr(index, "pret"))
                                        reteta = getattr(index, "reteta")
                                        pret_final = 0
                                        l1 = float(pret *
                                                   float
                                                   (lista_nr_bucati[j]))
                                        l2 = float((0.10 *
                                                    (pret *
                                                     float
                                                     (lista_nr_bucati[j]))))
                                        l3 = float((0.15 *
                                                    (pret *
                                                     float
                                                     (lista_nr_bucati[j]))))
                                        if reteta == 'nu':
                                            pret_final = l1 - l2
                                        elif reteta == 'da':
                                            pret_final = l1 - l3
                                        k = self.cardClientRepository
                                        kard = k.read(index1)
                                        suma = suma + pret_final
                                        if i == len(lista_nr_bucati) - 1:
                                            rezultat.append(
                                                CardClientCuReducere(
                                                    kard.id_entitate,
                                                    kard.nume,
                                                    kard.prenume,
                                                    kard.CNP,
                                                    kard.data_nasterii,
                                                    kard.data_inregistrare,
                                                    suma
                                                ))
        return my_sorted(rezultat,
                         key=lambda v: v.suma_reducere, reverse=True)

    def Stergere_In_Cascada(self, id_medicament: str):
        """
        Aceasta functie sterge tranzactiile care contin id-ul
        medicamentului sters din  lista de medicamente
        :param id_medicament: id-ul medicamentului care este sters
        :return: None
        """
        lista = self.get_All()
        tranzactii_cu_id = list(filter(
            lambda x: x.id_medicament == id_medicament,
            lista))
        for tranz in tranzactii_cu_id:
            self.tranzactieRepository.sterge(tranz.id_entitate)
        return tranzactii_cu_id
