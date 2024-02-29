from Domain.card_client_Validator import CardClientValidator
from Domain.medicament_Validator import MedicamentValidator
from Domain.tranzactie_Validator import TranzactieValidator
from Repository.repository_Json import RepositoryJson
from Service.Undo_Redo_Service import UndoRedoService
from Service.card_client_Service import CardClientService
from Service.medicament_Service import MedicamentService
from Service.tranzactie_Service import TranzactieService
from Tests.Test_Repository_Json import test_card_client_repository,\
    test_tranzactie_repository, \
    test_medicament_repository
from Tests.Test_Card_Client_Service import test_card_client_service
from Tests.Test_Domain import test_tranzactie, test_medicament, test_card
from Tests.Test_Medicament_Service import test_medicament_service,\
    test_scumpirea_cu_un_procentaj
from Tests.Test_Tranzactie_Service import test_tranzactie_service, \
    test_cautare_full_text, \
    test_afisare_tranzactii_interval, \
    test_ordonare_descrescator_dupa_nr_vanzari, \
    test_stergerea_tranzactiilor_interval, \
    test_ordonare_descrescator_val_reduceri, test_stergere_in_cascada
from Tests.Test_Undo_Redo import test_undo_redo_medicament_service,\
    test_undo_redo_card_client_service, \
    test_undo_redo_tranzactie_service,\
    test_undo_redo_scumpire_cu_un_procentaj,\
    test_undo_redo_generare_entitati, \
    test_undo_redo_stergerea_tranzactiilor_interval,\
    test_undo_redo_sterge_in_cascada
from UI.console import Consola


def main():
    undoRedoService = UndoRedoService()
    medicamentValidator = MedicamentValidator()
    medicamentRepositoryJson = RepositoryJson("medicamente.json")
    medicamentService = MedicamentService(medicamentRepositoryJson,
                                          medicamentValidator,
                                          undoRedoService)
    cardclientValidator = CardClientValidator()
    cardclientRepositoryJson = RepositoryJson("carduri.json")
    cardService = CardClientService(cardclientRepositoryJson,
                                    cardclientValidator,
                                    undoRedoService)

    tranzactieValidator = TranzactieValidator()
    tranzactieRepositoryJson = RepositoryJson("tranzactie.json")
    tranzactieService = TranzactieService(tranzactieRepositoryJson,
                                          tranzactieValidator,
                                          medicamentRepositoryJson,
                                          cardclientRepositoryJson,
                                          undoRedoService)
    consola = Consola(medicamentService, cardService, tranzactieService,
                      undoRedoService)
    consola.Run_Menu()


if __name__ == '__main__':
    test_card_client_repository()
    test_tranzactie_repository()
    test_medicament_repository()
    test_card_client_service()
    test_medicament_service()
    test_tranzactie_service()
    test_cautare_full_text()
    test_afisare_tranzactii_interval()
    test_tranzactie()
    test_medicament()
    test_card()
    test_ordonare_descrescator_dupa_nr_vanzari()
    test_stergerea_tranzactiilor_interval()
    test_ordonare_descrescator_val_reduceri()
    test_scumpirea_cu_un_procentaj()
    test_stergere_in_cascada()
    test_undo_redo_medicament_service()
    test_undo_redo_card_client_service()
    test_undo_redo_tranzactie_service()
    test_undo_redo_scumpire_cu_un_procentaj()
    test_undo_redo_generare_entitati()
    test_undo_redo_stergerea_tranzactiilor_interval()
    test_undo_redo_sterge_in_cascada()
    main()
