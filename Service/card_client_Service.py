from datetime import datetime

from Domain.Add_Operations import AddOperations
from Domain.Delete_Operations import DeleteOperations
from Domain.Modify_Operations import ModifyOperations
from Domain.card_client import CardClient
from Domain.card_client_Validator import CardClientValidator
from Repository.Exceptii import DuplicateCNPError

from Repository.repository import Repository
from Service.Undo_Redo_Service import UndoRedoService


class CardClientService:
    def __init__(self, cardClientRepository: Repository,
                 cardClientValidator: CardClientValidator,
                 undoRedoService: UndoRedoService):
        self.cardClientRepository = cardClientRepository
        self.cardClientValidator = cardClientValidator
        self.undoRedoService = undoRedoService

    def get_All(self):
        """
        Afiseaza lista de carduri
        :return: Returneaza lista de carduri
        """
        return self.cardClientRepository.read()

    def adauga(self, id_card: str, nume: str, prenume: str, CNP: str,
               data_nasterii: str, data_inregistrarii: str) -> None:
        """
        Adauga un obiect de tip CardClient in lista
        :param id_card: id card client
        :param nume: nume client
        :param prenume: prenume client
        :param CNP: CNP client
        :param data_nasterii: data nasterii client
        :param data_inregistrarii: data inregistrarii client
        :return: None
        """
        lista = []
        for index in self.cardClientRepository.read():
            lista.append(getattr(index, 'CNP'))
        if CNP in lista:
            raise DuplicateCNPError("CNP-ul dat exista deja!")
        card_client = CardClient(id_card, nume, prenume, CNP,
                                 data_nasterii, data_inregistrarii)
        self.cardClientValidator.valideaza(card_client)
        self.cardClientRepository.adauga(card_client)
        self.undoRedoService.clear_redo()
        self.undoRedoService.Add_Undo_Operations(
            AddOperations(self.cardClientRepository, card_client))

    def sterge(self, id_card: str) -> None:
        """
        Sterge un obiect de tip CardClient din lista
        :param id_card: id card client
        :return: None
        """
        if self.cardClientRepository.read(id_card) is not None:
            card_client = self.cardClientRepository.read(id_card)
        self.cardClientRepository.sterge(id_card)
        self.undoRedoService.clear_redo()
        self.undoRedoService.Add_Undo_Operations(
            DeleteOperations(self.cardClientRepository, card_client))

    def modifica(self, id_card: str, nume: str, prenume: str, CNP: str,
                 data_nasterii: str, data_inregistrarii: str) -> None:
        """
        Modifica un obiect de tip CardClient in lista
        :param id_card: id card client
        :param nume: nume client
        :param prenume: prenume client
        :param CNP: CNP client
        :param data_nasterii: data nasterii client
        :param data_inregistrarii: data inregistrarii client
        :return: None
        """
        card_client_vechi = self.cardClientRepository.read(id_card)
        card_client = CardClient(id_card, nume, prenume, CNP,
                                 data_nasterii, data_inregistrarii)

        self.cardClientValidator.valideaza(card_client)
        self.cardClientRepository.modifica(card_client)
        self.undoRedoService.clear_redo()
        self.undoRedoService.Add_Undo_Operations(
            ModifyOperations(self.cardClientRepository,
                             card_client_vechi,
                             card_client))
