"""Zadanie polegające na użyciu dekoratorów singledispatch i singledispatchmethod
do osiągnięcia polimorfizmu zależnefo od typu pojedyńczego parametru."""
from functools import singledispatch, singledispatchmethod

@singledispatch
def log_event(event):
    """Domyślna interpretacja funkcji log_event"""
    raise NotImplementedError(f"Brak implementacji dla typu: {type(event)}")

@log_event.register
def _(event: str):
    """Implementacja log_event dla typu str."""
    print(f"[log_event - str] Logowanie zdarzenia: {event}")

@log_event.register
def _(event: int):
    """Implementacja log_event dla typu int"""
    print(f"[log_event - int] Logowanie błędu o kodzie: {event}")

@log_event.register
def _(event: dict):
    """Implementacja log_event dla typu dict."""
    print(f"[log_event - dict] Logowanie zdarzenia w formie słownika: {event}")

class EventHandler:
    """Klasa do obsługi zdarzeń za pomocą dekoratora @singledispatchmethod.
    Przechowuje licznik obsłużonych zdarzeń."""
    def __init__(self):
        """Inicjalizacja licznika zdarzeń."""
        self.event_count = 0

    @singledispatchmethod
    def handle_event(self, event):
        """Domyślna obsługa zdarzeń"""
        raise NotImplementedError(f"Nieobsługiwany typ zdarzenia: {type(event)}")

    @handle_event.register
    def _(self, event: str):
        """Obsługa zdarzenia typu str."""
        self.event_count += 1
        print(f"[EventHandler - str] Obsługa zdarzenia: {event}, "
              f"licznik zdarzeń = {self.event_count}")

    @handle_event.register
    def _(self, event: int):
        """Obsługa zdarzenia typu int.""" 
        self.event_count += 1
        print(f"[EventHandler - int] Obsługa zdarzenia numerycznego: {event}, "
              f"licznik zdarzeń = {self.event_count}")

    @handle_event.register
    def _(self, event: list):
        """Obsługa zdarzenia typu list."""
        self.event_count += 1
        print(f"[EventHandler - list] Obsługa listy zdarzeń: {event}, "
              f"licznik zdarzeń = {self.event_count}")

    def some_public_method(self):
        """Dodatkowa publiczna metoda, by uniknąć
        ostrzeżeń pylint o zbyt małej liczbie metod."""
        print("Wywołanie some_public_method w EventHandler.")

class DerivedHandler(EventHandler):
    """Klasa pochodna z nowymi rejestracjami typów w @singledispatchmethod.
    Zawiera m.in. nadpisaną obługę typu int i nową obsługę typu float."""

    @EventHandler.handle_event.register # pylint: disable=no-member
    def _(self, event: int):
        """Nadpisana obłusga zdarzeń typu int."""
        self.event_count += 1
        print(f"[DerivedHandler - int] Nowa obsługa zdarzenia numerycznego: {event}, "
              f"licznik zdarzeń = {self.event_count}")

    @EventHandler.handle_event.register # pylint: disable=no-member
    def _(self, event: float):
        """Obsługa zdarzeń typu float."""
        self.event_count += 1
        print(f"[DerivedHandler - float] Obsługa zdarzenia zmiennoprzecinkowego: {event}, "
              f"licznik zdarzeń = {self.event_count}")


if __name__ == "__main__":
    print("=== Globalne logowanie zdarzeń ===")
    log_event("Uruchomienie systemu")
    log_event(404)
    log_event({"typ": "error", "opis": "Nieznany błąd"})

    print("\n=== Klasa EventHandler ===")
    handler = EventHandler()
    handler.handle_event("Zdarzenie logowania")
    handler.handle_event(123)
    handler.handle_event(["zdarzenie1", "zdarzenie2", "zdarzenie3"])

    print("\n=== Obsługa nieobsługiwanego typu ===")
    try:
        log_event(3.14)
    except NotImplementedError as e:
        print(e)

    try:
        handler.handle_event(set([1, 2, 3]))
    except NotImplementedError as e:
        print(e)

    print("\n=== Klasa DerivedHandler ===")
    derived_handler = DerivedHandler()
    derived_handler.handle_event("Inne zdarzenie tekstowe")
    derived_handler.handle_event(789)
    derived_handler.handle_event(3.14)

    print("\n=== Niespodzianka przy wywołaniu handler.handle_event(12356789) ===")
    handler.handle_event(12356789)
