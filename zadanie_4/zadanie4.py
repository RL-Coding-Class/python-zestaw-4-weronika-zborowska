"""Zadanie pokazuje przykład obliczania pól różnych figrur,
z wykorzystaniem wielokreotnej dyspozycji (multiple dispatch)."""
# pylint: disable=function-redefined, no-value-for-parameter, too-many-function-args

from multipledispatch import dispatch
import math

class Figura(object):
    """Bazowa klasa reprezentująca figurę geometryczną."""
    # pylint: disable=too-few-public-methods
    def __init__(self):
        print("Figura init")

class Prostokat(Figura):
    """Klasa reprezentująca prostokąt."""
    # pylint: disable=too-few-public-methods
    def __init__(self, x: int, y: int):
        super().__init__()
        print("Prostokat init")
        self.x = x
        self.y = y

class Kwadrat(Prostokat):
    """Klasa reprezentująca kwadrat (dziedziczy po prostokąt)"""
    # pylint: disable=too-few-public-methods
    def __init__(self, x: int):
        super().__init__(x, x)
        print("Kwadrat init")

class Kolo(Figura):
    # pylint: disable=too-few-public-methods
    """Klasa reprezentująca koło"""
    def __init__(self, r: float):
        super().__init__()
        print("Kolo init")
        self.r = r

@dispatch(Figura)
def pole(instance: Figura):
    """Wersja domyślna dla obiektu typu Figura.
    Zwraca 0 i wypisuje informację, że to figura ogólna."""
    print("Pole: Figura")
    return 0

@dispatch(Prostokat)
def pole(p: Prostokat):
    """Obliczanie pola Prostokąta na podstawie obecnych wymiarów p.x i p.y."""
    print("Pole: Prostokat (bez parametrów)")
    return p.x * p.y

@dispatch(Prostokat, int, int)
def pole(p: Prostokat, x: int, y: int):
    """Zmienia wymiary Prostokąta p.x, p.y na nowe (x, y) i zwraca wynik."""
    print("Pole: Prostokat (z parametrami x, y)")
    p.x = x
    p.y = y
    return p.x * p.y

@dispatch(Kwadrat)
def pole(k: Kwadrat):
    """Obliczanie pola Kwadratu na podstawie obecnego boku (k.x)."""
    print("Pole: Kwadrat (bez parametrów)")
    return k.x * k.y

@dispatch(Kwadrat, int)
def pole(k: Kwadrat, x: int):
    """Zmienia bok Kwadratu na x i zwraca nowe pole."""
    print("Pole: Kwadrat (z parametrem x)")
    k.x = x
    k.y = x
    return k.x * k.y

@dispatch(Kolo)
def pole(k: Kolo):
    """Obliczanie pola Koła na podstawie obecnego promienia (k.r)."""
    print("Pole: Kolo (bez parametru)")
    return math.pi * (k.r ** 2)

@dispatch(Kolo, float)
def pole(k: Kolo, r: float):
    """Zmienia promień Koła na r i zwraca nowe pole."""
    print("Pole: Kolo (z parametrem r)")
    k.r = r
    return math.pi * (k.r ** 2)

def polaPowierzchni(listaFigur):
    for i in listaFigur:
        print(f"Pole obiektu: {pole(i)}")

if __name__ == "__main__":
    print("=== Tworzenie obiektów ===")
    a, b, c, d = Figura(), Prostokat(2, 4), Kwadrat(2), Kolo(3)

    print("\n=== Wywołania funkcji pole ===")
    print(f"Pole prostokąta (2x4): {pole(b)}")
    print(f"Pole kwadratu (bok=2): {pole(c)}")
    print(f"Pole koła (r=3): {pole(d)}")

    print("\n=== Zmiana wymiarów ===")
    print(f"Pole prostokąta po zmianie na 5x6: {pole(b, 5, 6)}")
    print(f"Pole kwadratu po zmianie boku na 7: {pole(c, 7)}")
    print(f"Pole koła po zmianie promienia na 4: {pole(d, 4.0)}")

    print("\n=== Polimorfizm w czasie wykonywania ===")
    polaPowierzchni([a, b, c, d])
