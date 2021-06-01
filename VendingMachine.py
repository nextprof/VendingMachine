from Exceptions import *


class Item:
    """
    CLASS:
        *Item - klasa imitująca przedmiot.
    FIELDS:
        *name - zmienna przechowująca nazwę przedmiotu.
    """

    def __init__(self, name):
        self.name = name


class Product(Item):
    """
        CLASS:
            *Product - klasa imitująca produkt.
        FIELDS:
            *name - zmienna przechowująca nazwę przedmiotu.
            *price - zmienna przechowująca cenę przedmiotu.
            *quantity - zmienna przechowująca ilość przedmiotu.
        """

    def __init__(self, name, price):
        super(Product, self).__init__(name)
        self.price = price
        self.quantity = 5


def connect_dict(dictionary1, dictionary2):
    """
        Metoda scala 2 słowniki w 1 i go zwraca.
    :param dictionary1:
    :param dictionary2:
    :return: dictionary, słownik który jest stworzony z 2 słowników podanych w argumentach
    """
    connected_dict = dictionary1.copy()
    for key in dictionary2:
        if key in connected_dict:
            connected_dict[key] += dictionary2[key]
        else:
            connected_dict[key] = dictionary2[key]
    return connected_dict


def get_coin_amount(dictionary):
    """
    :param dictionary:
    :return: int - Ilość monet
    """
    counter = 0
    for value in dictionary.values():
        counter += value
    return counter


class VendingMachine:
    """
        CLASS:
            *VendingMachine - klasa imitująca automat z napojami.
        FIELDS:
            *coin_types - lista przechowująca możliwe wartości monet w groszach.
            *products - słownik w którym znajdują się produkty, key - nr produktu, value - produkt.
            *coins - słownik który posiada informacje o wszystkich monetach, wrzuconych i posiadanych.
            Key - typ monety, value - słownik którego key - 'inserted' lub 'owned' a value to ilość monet.
        """
    coin_types = [1, 2, 5, 10, 20, 50, 100, 200, 500]
    coins = None

    products = {}

    def __init__(self):
        super().__init__()

        self.init_products()

        self.init_coins_dicts()

    def init_coins_dicts(self):
        """
        Klasa inicjalizująca stan monet automatu na 1 posiadaną monetę każdego typu
        """

        self.coins = {
            c: {'owned': 1, 'inserted': 0}
            for c
            in self.coin_types
        }

    def get_inserted(self):
        """
        :return: zwraca słownik wrzuconych monet przez klienta
        """
        return {key: self.coins[key]['inserted'] for key, value in self.coins.items() if
                self.coins[key]['inserted'] > 0}

    def get_inserted_value(self):
        """
        :return: int, zwraca wartość wrzuconych monet przez klienta
        """
        val = 0
        for key, value in self.coins.items():
            val += key * value['inserted']
        return val

    def get_valid_coins_type(self):
        coins_new = [c for c in self.coin_types if c < 1000]
        return coins_new

    def check_available_coins(self, dictionary):
        """
        :return: boolean, sprawdza czy stan monet w dictionary jest wystarczający
        """
        for key, value in dictionary.items():
            available = self.coins[key]['owned'] + self.coins[key]['inserted']
            if value > available:
                return False
        return True

    def payment(self, product_number):
        """
        Funkcja sprawdza czy istnieje produkt o takim numerze, jeżeli nie zgłasza InvalidProductNumberException,
        jeżeli produkt istnieje, ale jest niedostępny zgłasza ProductUnavailableException,
        jeżeli wartość wprowadzonych monet jest niewystarczająca zgłasza NotEnoughMoneyException
        Ilość produktu zostaje zmniejszona o 1, jeżeli trzeba wydać resztę zwraca ją.
        Jeżeli automat nie posiada monet ,aby wydać resztę zgłasza OnlyExactMoneyException

        :param product_number:
        :return: Jeżeli brak reszty zwraca string oraz produkt
        , gdy występuję wydanie reszty zwraca słownik z monetami oraz produkt
        """
        if product_number not in self.products:
            raise InvalidProductNumberException

        product = self.products[product_number]
        if product.quantity < 1:
            raise ProductUnavailableException

        price = product.price
        inserted = self.get_inserted_value()
        change = inserted - price

        if change < 0:
            raise NotEnoughMoneyException(self.products[product_number].price)

        elif change == 0:
            product.quantity -= 1
            self.clear_inserted()
            return 'Brak reszty.', product

        past_dictionary = {0: {}}
        for i in range(1, change + 1):
            for coin in self.coin_types:
                rest = i - coin
                if rest < 0:
                    continue

                if rest not in past_dictionary:
                    continue

                dictionary = {coin: 1}
                new_connected_dict = connect_dict(
                    past_dictionary[rest],
                    dictionary
                )

                if not self.check_available_coins(new_connected_dict):
                    continue
                if i not in past_dictionary:
                    past_dictionary[i] = new_connected_dict
                else:
                    if get_coin_amount(past_dictionary[i]) > get_coin_amount(new_connected_dict):
                        past_dictionary[i] = new_connected_dict

        if change not in past_dictionary:
            raise OnlyExactMoneyException

        for key in self.coins:
            self.coins[key]['owned'] += self.coins[key]['inserted']
        for key in past_dictionary[change]:
            self.coins[key]['owned'] -= past_dictionary[change][key]

        self.clear_inserted()

        product.quantity -= 1

        return past_dictionary[change], product

    def get_product_price(self, product_number):
        """
        :param product_number:
        :return: cena produktu
        """
        if product_number not in self.products:
            raise InvalidProductNumberException
        return self.products[product_number].price

    def withdraw(self):
        """
        :return: słownik z wprowadzonymi monetami przez użytkownika
        """
        if self.get_inserted_value() == 0:
            raise WithdrawException
        all_inserted = self.get_inserted().copy()
        self.clear_inserted()
        return all_inserted

    def clear_inserted(self):
        """
        Ustawia wprowadzone monety na 0
        """
        for key in self.coins:
            self.coins[key]['inserted'] = 0

    def insert_coin(self, coin_type):
        """
        Dodaje monetę do słownika przechowującego monety wprowadzone przez klienta

        :param coin_type:
        """
        self.coins[coin_type]['inserted'] += 1

    def init_products(self):
        """
        Klasa inicjująca stan automatu wprowadzająca 20 produktów o różnych cenach z różnymi numerami produktu 30-50
        """
        self.products[30] = Product("Woda 0.3l", 150)
        self.products[31] = Product("Woda 0.5l", 200)
        self.products[32] = Product("Coca-Cola 0.3l", 250)
        self.products[33] = Product("Coca-Cola 0.5l", 500)
        self.products[34] = Product("Sprite 0.3l", 250)
        self.products[35] = Product("Sprite 0.5l", 500)
        self.products[36] = Product("Miranda 0.3l", 250)
        self.products[37] = Product("Miranda 0.5l", 500)
        self.products[38] = Product("Lipton 0.3l", 50)
        self.products[39] = Product("Lipton 0.5l", 450)
        self.products[40] = Product("Dzik Energy 0.5l", 550)
        self.products[41] = Product("RedBull 0.2l", 780)
        self.products[42] = Product("7up 0.5l", 150)
        self.products[43] = Product("Fanta 0.5l", 400)
        self.products[44] = Product("Tonic 0.3l", 320)
        self.products[45] = Product("Tonic 0.5l", 470)
        self.products[46] = Product("Monster 0.5l", 500)
        self.products[47] = Product("Sok jabłko 0.2l", 130)
        self.products[48] = Product("Sok jabłko 0.3l", 200)
        self.products[49] = Product("Sok jabłko 0.5l", 260)
