import jsonpickle

from Domain.entitate import Entitate
from Repository.repository_In_Memory import RepositoryInMemory


class RepositoryJson(RepositoryInMemory):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def __readFile(self):
        """
        Citeste un fisier
        """
        try:
            with open(self.filename, "r") as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __writeFile(self) -> None:
        """
        Afiseaza un fisier
        """
        with open(self.filename, "w") as f:
            f.write(jsonpickle.dumps(self.entitati, indent=2))

    def read(self, id_entitate=None):
        """
        Verifica daca exista o entitate cu id-ul dat
        Daca nu se va pune nici un parametru aceste functii
        ea va returna lista de obiecte
        :param id_entitate: id-ul entitatii pe care il cautam
        :return: Daca id_entitate este None va returna lista de obiecte
                 Daca id_entitate este in lista de entitai va returna id
                 card
                 Daca id_entitate nu este in lista de entitati va returna
                 None
        """
        self.entitati = self.__readFile()
        return super().read(id_entitate)

    def adauga(self, entitate: Entitate) -> None:
        """
        Adauga un obiect de tip Entitate in lista
        :param entitate: obiect de tip Entitate
        :return: None
        """
        self.entitati = self.__readFile()
        super().adauga(entitate)
        self.__writeFile()

    def sterge(self, id_entitate: str) -> None:
        """
        Sterge un obiect de tip Entitate din lista
        :param id_entitate: obiect de tip Entitate
        :return: None
        """
        self.entitati = self.__readFile()
        super().sterge(id_entitate)
        self.__writeFile()

    def modifica(self, entitate: Entitate) -> None:
        """
        Modifica un obiect de tip Entitate in lista
        :param entitate: obiect de tip Entitate
        :return: None
        """
        self.entitati = self.__readFile()
        super().modifica(entitate)
        self.__writeFile()
