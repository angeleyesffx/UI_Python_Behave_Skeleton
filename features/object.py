#Classe helper para instaciar objetos
class Singleton:
    __instance = None

    def __init__(self, classe):
        self.classe = classe
        Singleton.__instance = self.classe

    @staticmethod
    def getInstance(self, classe):
        """ Static access method. """
        if Singleton.__instance is None:
            Singleton(classe)
            return Singleton.__instance
