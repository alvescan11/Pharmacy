import datetime

from Domain.Stergere_In_Cascada_Operations import StergereInCascadaOperations
from Repository.Exceptii import IncorrectData, DuplicateIDError
from Service.Undo_Redo_Service import UndoRedoService
from Service.card_client_Service import CardClientService
from Service.medicament_Service import MedicamentService
from Service.tranzactie_Service import TranzactieService


class Consola:
    def __init__(self, medicamentService: MedicamentService,
                 cardClientService: CardClientService,
                 tranzactieService: TranzactieService,
                 undoRedoService: UndoRedoService):
        self.medicamentService = medicamentService
        self.cardClientService = cardClientService
        self.tranzactieService = tranzactieService
        self.undoRedoService = undoRedoService

    def Run_Menu(self) -> None:
        while True:
            print("1. CRUD medicament")
            print("2. CRUD card client")
            print("3. CRUD trazactie")
            print("4. Căutare medicamente și clienți. Căutare full text")
            print("5. Afișarea tuturor tranzacțiilor dintr-un "
                  "interval de zile dat")
            print("6. Generare n entitati")
            print("7. Afișarea medicamentelor ordonate descrescător "
                  "după numărul de vânzări.")
            print("8. Afișarea cardurilor client ordonate descrescător"
                  " după valoarea reducerilor obținute.")
            print("9. Ștergerea tuturor tranzacțiilor dintr-un "
                  "anumit interval de zile.")
            print("10. Scumpirea cu un procentaj dat a tuturor "
                  "medicamentelor cu prețul mai mic decât o valoare dată.")
            print("u. Undo")
            print("r. Redo")
            print("x. Iesire")

            optiune = input("Dati o optiune: ")
            if optiune == '1':
                self.Run_Crud_Medicament()
            elif optiune == '2':
                self.Run_Crud_Card_Client()
            elif optiune == '3':
                self.Run_Crud_Tranzactie()
            elif optiune == '4':
                self.Run_Cautare_Full_Text()
            elif optiune == '5':
                self.Run_Afisare_Tranzactii_Interval()
            elif optiune == '6':
                self.Run_Generare_Enititati()
            elif optiune == '7':
                self.Run_Ordonare_Descrescator_Dupa_Nr_Vanzari()
            elif optiune == '8':
                self.Run_Ordonare_Descrescator_Val_Reduceri()
            elif optiune == '9':
                self.Run_Stergerea_Tranzactiilor_Interval()
            elif optiune == '10':
                self.Run_Scumpirea_Cu_Un_Procentaj()
            elif optiune == 'u':
                self.undoRedoService.undo()
            elif optiune == 'r':
                self.undoRedoService.redo()
            elif optiune == 'x':
                break
            else:
                print("Nu exista aceasta optiune!")

    def Run_Crud_Medicament(self) -> None:
        while True:
            print("1. Adauga medicament")
            print("2. Sterge medicament")
            print("3. Modifica medicament")
            print("a. Afiseaza toate medicamentele")
            print("x. Iesire")
            optiune = input("Dati o optiune: ")
            if optiune == '1':
                self.UI_Adauga_Medicament()
            elif optiune == '2':
                self.UI_Sterge_Medicament()
            elif optiune == '3':
                self.UI_Modifica_Medicament()
            elif optiune == 'a':
                self.Show_All_Medicamente()
            elif optiune == 'x':
                break
            else:
                print("Nu exista aceasta optiune!")

    def UI_Adauga_Medicament(self) -> None:
        """
        Adauga un medicament
        """
        try:
            id_medicament = input("Dati id-ul medicamentului: ")
            nume = input("Dati numele medicamentului: ")
            producator = input("Dati producatorul medicamentului: ")
            pret = input("Dati pretul medicamentului: ")
            reteta = input("Specificati daca medicamentul se elibereaza"
                           " cu ajutorul unei retete sau nu: ")
            self.medicamentService.adauga(id_medicament,
                                          nume, producator,
                                          pret, reteta)
        except IncorrectData as ID:
            print(ID)
        except DuplicateIDError as DE:
            print(DE)
        except Exception as e:
            print(e)

    def UI_Sterge_Medicament(self) -> None:
        """
        Sterge un medicament
        """
        try:
            id_medicament = input("Dati id-ul medicamentului de sters: ")
            tranzactii_id = self.tranzactieService.\
                Stergere_In_Cascada(id_medicament)
            medicament = self.medicamentService.\
                medicamentRepository.read(id_medicament)
            self.medicamentService.sterge(id_medicament)
            self.undoRedoService.clear_redo()
            stergereInCascadaOperations = StergereInCascadaOperations(
                self.medicamentService.medicamentRepository,
                self.tranzactieService.tranzactieRepository,
                medicament,
                tranzactii_id
            )
            self.undoRedoService.Add_Undo_Operations(
                stergereInCascadaOperations)
        except DuplicateIDError as DE:
            print(DE)
        except Exception as e:
            print(e)

    def UI_Modifica_Medicament(self) -> None:
        """
        Modifica un medicament
        """
        try:
            id_medicament = input("Dati id-ul medicamentului de modificat: ")
            nume = input("Dati numele nou al medicamentului: ")
            producator = input("Dati producatorul nou al medicamentului: ")
            pret = input("Dati pretul nou al medicamentului: ")
            reteta = input("Specificati daca medicamentul se elibereaza"
                           " cu ajutorul unei retete sau nu: ")
            self.medicamentService.modifica(id_medicament,
                                            nume, producator,
                                            pret, reteta)
        except IncorrectData as ID:
            print(ID)
        except DuplicateIDError as DE:
            print(DE)
        except Exception as e:
            print(e)

    def Show_All_Medicamente(self) -> None:
        """
        Afiseaza toate medicamentele
        """
        for medicament in self.medicamentService.get_All():
            print(medicament)

    def Run_Crud_Card_Client(self) -> None:
        while True:
            print("1. Adauga card client")
            print("2. Sterge card client")
            print("3. Modifica card client")
            print("a. Afiseaza toate cardurile")
            print("x. Iesire")
            optiune = input("Dati o optiune: ")
            if optiune == '1':
                self.UI_Adauga_Card()
            elif optiune == '2':
                self.UI_Sterge_Card()
            elif optiune == '3':
                self.UI_Modifica_Card()
            elif optiune == 'a':
                self.Show_All_Card()
            elif optiune == 'x':
                break
            else:
                print("Nu exista aceasta optiune!")

    def Run_Crud_Tranzactie(self) -> None:
        while True:
            print("1. Adauga tranzactie")
            print("2. Sterge tranzactie")
            print("3. Modifica tranzactie")
            print("a. Afiseaza toate tranzactiile")
            print("x. Iesire")
            optiune = input("Dati o optiune: ")
            if optiune == '1':
                self.UI_Adauga_Tranzactie()
            elif optiune == '2':
                self.UI_Sterge_Tranzactie()
            elif optiune == '3':
                self.UI_Modifica_Tranzactie()
            elif optiune == 'a':
                self.Show_All_Tranzactii()
            elif optiune == 'x':
                break
            else:
                print("Nu exista aceasta optiune!")

    def UI_Adauga_Card(self) -> None:
        """
        Adauga un card client
        """
        try:
            id_card = input("Dati id-ul cardului: ")
            nume = input("Dati numele clientului: ")
            prenume = input("Dati prenumele clientului: ")
            CNP = input("Dati CNP-ul clientului: ")
            data_nasterii = datetime.datetime(int(input
                                                  ("Dati anul nasterii: ")),
                                              int(input
                                                  ("Dati luna nasterii: ")),
                                              int(input
                                                  ("Dati ziua naterii: ")))
            data_nasterii_copie = data_nasterii.strftime("%d.%m.%Y")
            data_inregistrarii = datetime.datetime(int(input("Dati anul"
                                                             " inregistrarii:"
                                                             " ")),
                                                   int(input("Dati luna "
                                                             "inregistrarii:"
                                                             " ")),
                                                   int(input("Dati ziua "
                                                             "inregistrarii:"
                                                             " ")))
            data_inregistrarii_copie = data_inregistrarii.strftime("%d.%m.%Y")
            d1 = data_nasterii_copie
            d2 = data_inregistrarii_copie
            self.cardClientService.adauga(id_card,
                                          nume,
                                          prenume,
                                          CNP,
                                          d1, d2)
        except IncorrectData as ID:
            print(ID)
        except DuplicateIDError as DE:
            print(DE)
        except Exception as e:
            print(e)

    def UI_Sterge_Card(self) -> None:
        """
        Sterge un card client
        """
        try:
            id_card = input("Dati id-ul cardului de sters: ")
            self.cardClientService.sterge(id_card)
        except DuplicateIDError as DE:
            print(DE)
        except Exception as e:
            print(e)

    def UI_Modifica_Card(self) -> None:
        """
        Modifica un card client
        """
        try:
            id_card = input("Dati id-ul cardului de modificat: ")
            nume = input("Dati numele nou al clientului: ")
            prenume = input("Dati prenumele nou al clientului: ")
            CNP = input("Dati CNP-ul nou al clientului: ")

            data_nasterii = datetime.datetime(int(
                input("Dati anul nasterii: ")),
                int(
                    input("Dati luna nasterii: ")),
                int(
                    input("Dati ziua nasterii: ")))
            data_nasterii_copie = data_nasterii.strftime("%d.%m.%Y")
            data_inregistrarii = datetime.datetime(int(
                input("Dati anul nou al inregistrarii: ")),
                int(
                    input("Dati luna noua a inregistrarii: ")),
                int(
                    input("Dati ziua noua a inregistrarii: ")))
            data_inregistrarii_copie = data_inregistrarii.strftime("%d.%m.%Y")
            d1 = data_nasterii_copie
            d2 = data_inregistrarii_copie
            self.cardClientService.modifica(id_card,
                                            nume,
                                            prenume,
                                            CNP,
                                            d1, d2)
        except IncorrectData as ID:
            print(ID)
        except DuplicateIDError as DE:
            print(DE)
        except Exception as e:
            print(e)

    def Show_All_Card(self) -> None:
        """
        Afiseaza toate cardurile
        """
        for card in self.cardClientService.get_All():
            print(card)

    def UI_Adauga_Tranzactie(self) -> None:
        """
        Adauga o tranzactie
        """
        try:
            id_tranzactie = input("Dati id-ul tranzactiei: ")
            id_medicament = input("Dati id-ul medicamentului: ")
            id_card_client = input("Dati id-ul cardului: ")
            nr_bucati = input("Dati numarul de bucati: ")
            data_si_ora = datetime.datetime(int(input("Dati anul: ")),
                                            int(input("Dati luna: ")),
                                            int(input("Dati ziua: ")),
                                            int(input("Dati ora: ")),
                                            int(input("Dati minutul: ")),
                                            int(input("Dati secunda: ")))
            data_si_ora_copie = data_si_ora.strftime("%d.%m.%Y %H:%M:%S")
            self.tranzactieService.adauga(id_tranzactie,
                                          id_medicament, id_card_client,
                                          nr_bucati, data_si_ora_copie)
        except IncorrectData as ID:
            print(ID)
        except DuplicateIDError as DE:
            print(DE)
        except Exception as e:
            print(e)
        else:
            if id_card_client != '0':
                list = self.medicamentService.get_All()
                reteta = ''
                for index in list:
                    if getattr(index, 'id_entitate') == id_medicament:
                        reteta = getattr(index, 'reteta')
                pret = 0
                for index in list:
                    if getattr(index, 'id_entitate') == id_medicament:
                        pret = float(getattr(index, 'pret'))
                pret_final = 0
                if reteta == 'nu':
                    pret_final = float(pret * float(nr_bucati)) - \
                                 float((0.10 * (pret * float(nr_bucati))))
                    print("Avand in vedere ca medicamentul necesita"
                          " o reteta s-a aplicat o reducere de 10 %"
                          " asupra pretului total, astfel de la"
                          "pretul de " + str(pret * float(nr_bucati))
                          + " s-a ajuns la pretul de " + str(pret_final))
                elif reteta == 'da':
                    pret_final = float(pret * float(nr_bucati)) - \
                                 float((0.15 * (pret * float(nr_bucati))))
                    print("Avand in vedere ca medicamentul necesita"
                          " o reteta s-a aplicat o reducere de 15 %"
                          " asupra pretului total, astfel de la"
                          "pretul de " + str(pret * float(nr_bucati))
                          + " s-a ajuns la pretul de " + str(pret_final))

    def UI_Sterge_Tranzactie(self) -> None:
        """
        Sterge o tranzactie
        """
        try:
            id_tranzactie = input("Dati id-ul tranzactiei pe care "
                                  "doriti sa o stergeti: ")
            self.tranzactieService.sterge(id_tranzactie)
        except DuplicateIDError as DE:
            print(DE)
        except Exception as e:
            print(e)

    def UI_Modifica_Tranzactie(self) -> None:
        """
        Modifica o tranzactie
        """
        try:
            id_tranzactie = input("Dati id-ul nou al tranzactiei: ")
            id_medicament = input("Dati id-ul nou al medicamentului: ")
            id_card_client = input("Dati id-ul nou al cardului: ")
            nr_bucati = input("Dati numarul nou de bucati: ")
            data_si_ora = datetime.datetime(int(input("Dati anul: ")),
                                            int(input("Dati luna: ")),
                                            int(input("Dati ziua: ")),
                                            int(input("Dati ora: ")),
                                            int(input("Dati minutul: ")),
                                            int(input("Dati secunda: ")))
            data_si_ora_copie = data_si_ora.strftime("%d.%m.%Y %H:%M:%S")
            self.tranzactieService.modifica(id_tranzactie,
                                            id_medicament, id_card_client,
                                            nr_bucati, data_si_ora_copie)
        except IncorrectData as ID:
            print(ID)
        except DuplicateIDError as DE:
            print(DE)
        except Exception as e:
            print(e)

    def Show_All_Tranzactii(self) -> None:
        """
        Afiseaza toate tranzactiile
        :return:
        """
        for tranzactie in self.tranzactieService.get_All():
            print(tranzactie)

    def Run_Cautare_Full_Text(self) -> None:
        """
        Cauta un cuvant un lista de medicamente sau in lista de carduri
        """
        string = input("Dati cuvantul pe care vreti sa il cautati: ")
        lista = self.tranzactieService.Cautare_Full_Text(string)
        for index in lista:
            print(index)

    def Run_Afisare_Tranzactii_Interval(self) -> None:
        """
        Afiseaza toate tranzactiile dintr-un interval dat
        """
        try:
            data1 = datetime.datetime(int(input("Dati anul datei 1: ")),
                                      int(input("Dati luna datei 1: ")),
                                      int(input("Dati ziua datei 1: ")))
            data2 = datetime.datetime(int(input("Dati anul datei 2: ")),
                                      int(input("Dati luna datei 2: ")),
                                      int(input("Dati ziua datei 2: ")))
            lista = self.tranzactieService. \
                Afisare_Tranzactii_Interval(data1, data2)
            for index in lista:
                print(index)
        except IncorrectData as ID:
            print(ID)
        except Exception as e:
            print(e)

    def Run_Generare_Enititati(self) -> None:
        """
        Genereaza n entitati
        """
        try:
            numar = int(input("Dati un numar: "))
            self.tranzactieService.Generare_Entitati(numar)
            self.Show_All_Medicamente()
        except IncorrectData as ID:
            print(ID)
        except Exception as e:
            print(e)

    def Run_Ordonare_Descrescator_Dupa_Nr_Vanzari(self) -> None:
        lista = self.tranzactieService. \
            Ordonare_Descrescator_Dupa_Nr_Vanzari()
        for index in lista:
            print(index)

    def Run_Stergerea_Tranzactiilor_Interval(self) -> None:
        try:
            an1 = int(input("Dati anul datei 1: "))
            luna1 = int(input("Dati luna datei 1: "))
            zi1 = int(input("Dati ziua datei 1: "))
            data1 = datetime.datetime(an1, luna1, zi1)
            an2 = int(input("Dati anul datei 2: "))
            luna2 = int(input("Dati luna datei 2: "))
            zi2 = int(input("Dati ziua datei 2: "))
            data2 = datetime.datetime(an2, luna2, zi2)
            self.tranzactieService. \
                Stergerea_Tranzactiilor_Interval(data1, data2)
            self.Show_All_Tranzactii()

        except IncorrectData as ID:
            print(ID)
        except Exception as e:
            print(e)

    def Run_Scumpirea_Cu_Un_Procentaj(self) -> None:
        try:
            procentaj = float(input("Dati un procentaj: "))
            pret_comp = float(input("Dati un pret de comparat: "))
            self.medicamentService. \
                Scumpirea_Cu_Un_Procentaj(procentaj, pret_comp)
            self.Show_All_Medicamente()

        except IncorrectData as ID:
            print(ID)
        except Exception as e:
            print(e)

    def Run_Ordonare_Descrescator_Val_Reduceri(self) -> None:
        lista = self.tranzactieService.Ordonare_Descrescator_Val_Reduceri()
        for index in lista:
            print(index)
