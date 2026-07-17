from abc import ABC, abstractmethod

class ExtratorBase(ABC):

    @abstractmethod
    def extrair_canal(self):
        """Extrai posts de um canal."""
        pass

    @abstractmethod
    def extrair_hot(self):
        """Extrai posts da seção Hot."""
        pass

    @abstractmethod
    def extrair_new(self):
        """Extrai posts da seção New."""
        pass