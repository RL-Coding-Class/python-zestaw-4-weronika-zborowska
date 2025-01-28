"""Moduł z klasami: Pojazd,Samochod, Autobus i klasami fabryk do ich tworzenia."""
from abc import ABC, abstractmethod

class Pojazd(ABC):
    """Klasa bazowa reprezentująca dowolny pojazd"""
    def __init__(self, model: str, rok: int):
        self._model = model
        self._rok = rok
        self._predkosc = 0

    @property
    def predkosc(self) -> float:
        """Getter dla prędkości pojazdu"""
        return self._predkosc

    @predkosc.setter
    def predkosc(self, value: float):
        """Setter dla prędkosci pojazdu. Odrzuca wartości ujemne"""
        if value < 0:
            raise ValueError("Prędkość nie może być ujemna!")
        self._predkosc = value

    @predkosc.deleter
    def predkosc(self):
        """Deleter, reseruje prędkośc do zera"""
        self._predkosc = 0

class Samochod(Pojazd):
    """Klasa dziedzicząca po Pojazd, reprezentuje samochod"""
    def __init__(self, model: str, rok: int, liczba_drzwi: int = 4):
        """Inicjalizuje obiekt Samochód."""
        super().__init__(model, rok)
        self.liczba_drzwi = liczba_drzwi

class Autobus(Pojazd):
    """Klasa dziedzicząca po Pojazd, reprezentuje autobus"""
    def __init__(self, model: str, rok: int, liczba_miejsc: int = 50):
        """Inicjalizuje obiekt autobus"""
        super().__init__(model, rok)
        self.liczba_miejsc = liczba_miejsc

class FabrykaPojazdow(ABC):
    """Klasa abstrakcyjna reprezentująca ogólną fabrykę pojazdów""" 
    def __init__(self, nazwa: str):
        """Inicjalizuje obiekt FabrykaPojazdow"""
        self._nazwa = nazwa
        self._liczba_wyprodukowanych = 0

    @property
    def nazwa(self) -> str:
        """Własciwość zwracająca nazwę fabryki."""
        return self._nazwa

    @abstractmethod
    def stworz_pojazd(self, model: str, rok: int, **kwargs):
        """Tworzy konkrenty pojazd (samochód lub autobus)
        i inkrementuje licznik."""
        pass

    @classmethod
    def utworz_fabryke(cls, typ_fabryki: str, nazwa: str):
        """Metoda klasowa tworząca określony typ fabryki (samochód lub autobus)."""
        if typ_fabryki == 'samochod':
            return FabrykaSamochodow(nazwa)
        if typ_fabryki == 'autobus':
            return FabrykaAutobusow(nazwa)
        raise ValueError("Nieznany typ fabryki!")

    @staticmethod
    def sprawdz_rok(rok: int) -> bool:
        """Sprawdza, czy rok produkcji jest w dopuszczalnym zakresie."""
        return 1900 <= rok <= 2024

    def _zwieksz_licznik(self):
        """Zwiększa licznik wyprodukowanych pojazdów o 1."""
        self._liczba_wyprodukowanych += 1

    def ile_wyprodukowano(self) -> int:
        """Zwraca liczbę wszystkich wyprodukowanych pojazdów"""
        return self._liczba_wyprodukowanych

class FabrykaSamochodow(FabrykaPojazdow):
    """Klasa reprezentująca fabrykę samochodów"""
    def stworz_pojazd(self, model: str, rok: int, liczba_drzwi: int = 4) -> Samochod:
        """Tworzy obiekt klasy Samochod"""
        if not self.sprawdz_rok(rok):
            raise ValueError("Nieprawidłowy rok produkcji!")
        self._zwieksz_licznik()
        return Samochod(model, rok, liczba_drzwi)

class FabrykaAutobusow(FabrykaPojazdow):
    """Klasa reprezentująca fabrykę autobusów."""
    def stworz_pojazd(self, model: str, rok: int, liczba_miejsc: int = 50) -> Autobus:
        """Tworzy obiekt klasy Autobus."""
        if not self.sprawdz_rok(rok):
            raise ValueError("Nieprawidłowy rok produkcji!")
        self._zwieksz_licznik()
        return Autobus(model, rok, liczba_miejsc)

def main():
    """Funkcja główna, która tworzy przykładowe fabryki pojazdów,
    produkuje samochód i autobus, demonstruje działanie
    gettera/settera/deletera prędkości i licznika wyprodukowanych pojazdów.
    """
    fabryka_samochodow = FabrykaPojazdow.utworz_fabryke('samochod', "Fabryka Samochodów Warszawa")
    fabryka_autobusow = FabrykaPojazdow.utworz_fabryke('autobus', "Fabryka Autobusów Kraków")

    print(f"Nazwa fabryki: {fabryka_samochodow.nazwa}")
    print(f"Nazwa fabryki: {fabryka_autobusow.nazwa}")

    samochod = fabryka_samochodow.stworz_pojazd("Fiat", 2023, liczba_drzwi=5)
    autobus = fabryka_autobusow.stworz_pojazd("Solaris", 2023, liczba_miejsc=60)

    samochod.predkosc = 50
    print(f"Prędkość samochodu: {samochod.predkosc}")
    del samochod.predkosc
    print(f"Prędkość po reset: {samochod.predkosc}")

    print(f"Wyprodukowano samochodów: {fabryka_samochodow.ile_wyprodukowano()}")
    print(f"Wyprodukowano autobusów: {fabryka_autobusow.ile_wyprodukowano()}")

if __name__ == "__main__":
    main()
