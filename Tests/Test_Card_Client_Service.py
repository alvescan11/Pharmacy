from Domain.card_client_Validator import CardClientValidator
from Repository.repository_Json import RepositoryJson
from Service.Undo_Redo_Service import UndoRedoService
from Service.card_client_Service import CardClientService
from utils import clear_file


def test_card_client_service():
    filename = "test_card_client.json"
    clear_file(filename)
    card_validator = CardClientValidator()
    card_repository = RepositoryJson(filename)
    undoRedoService = UndoRedoService()
    card_service = CardClientService(card_repository,
                                     card_validator,
                                     undoRedoService)
    card_service.adauga('1', 'Suciu', 'Sergiu',
                        '2341242143', '26.12.2000', '13.11.2020')
    assert len(card_service.get_All()) == 1
    card_service.modifica('1', 'Marian', 'George',
                          '2341242143', '26.12.2000', '13.11.2020')
    for index in card_service.get_All():
        id = getattr(index, 'id_entitate')
        if id == '1':
            nume = getattr(index, 'nume')
    assert nume == 'Marian'
    card_service.sterge('1')
    assert len(card_service.get_All()) == 0
