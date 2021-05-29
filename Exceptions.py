class VendingMachineException(Exception):
    def __init__(self, msg):
        self.msg = msg


class InvalidProductNumberException(VendingMachineException):
    def __init__(self):
        super().__init__("Niepoprawny numer produktu!")


class NotEnoughMoneyException(VendingMachineException):
    def __init__(self, price):
        super().__init__("Niewystarczająca ilość pieniędzy!\nCena produktu: " + str(price / 100) + " zł.")


class OnlyExactMoneyException(VendingMachineException):
    def __init__(self):
        super().__init__("Tylko odliczona kwota!")


class ProductUnavailableException(VendingMachineException):
    def __init__(self):
        super().__init__('Produkt jest niedostępny.')


class WithdrawException(VendingMachineException):
    def __init__(self):
        super().__init__('Brak wrzuconych monet.')
