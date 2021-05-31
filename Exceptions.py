class VendingMachineException(Exception):
    """Klasa wyjątków wykorzystywana w informowaniu o błędzie, jej wystąpienie nie kończy programu
    CLASS:
    *VendingMachineException - przechowuje wiadomość."""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class InvalidProductNumberException(VendingMachineException):
    """Klasa wyjątków wykorzystywana w informowaniu o błędzie, jej wystąpienie nie kończy działania programu
    CLASS:
    *InvalidProductNumberException - informuje, że wprowadzony przez klienta numer produktu nie jest prawidłowy,
    jej wystąpienie nie kończy działania programu."""
    def __init__(self):
        super().__init__("Niepoprawny numer produktu!")


class NotEnoughMoneyException(VendingMachineException):
    """Klasa wyjątków wykorzystywana w informowaniu o błędzie, jej wystąpienie nie kończy działania programu
    CLASS:
    *NotEnoughMoneyException - informuje, że wprowadzone przez klienta pieniądze nie wystarczają na zakup produktu,
    jej wystąpienie nie kończy działania programu."""
    def __init__(self, price):
        super().__init__("Niewystarczająca ilość pieniędzy!\nCena produktu: " + str(price / 100) + " zł.")


class OnlyExactMoneyException(VendingMachineException):
    """Klasa wyjątków wykorzystywana w informowaniu o błędzie, jej wystąpienie nie kończy działania programu
    CLASS:
    *OnlyExactMoneyException - informuje, że klient musi zapłacić odliczoną kwotą, jeżeli chce zakupić produkt,
    jej wystąpienie nie kończy działania programu."""
    def __init__(self):
        super().__init__("Tylko odliczona kwota!")


class ProductUnavailableException(VendingMachineException):
    """Klasa wyjątków wykorzystywana w informowaniu o błędzie, jej wystąpienie nie kończy działania programu
    CLASS:
    *ProductUnavailableException - informuje, że produkt który klient chce zakupić, jest niedostępny,
    jej wystąpienie nie kończy działania programu."""
    def __init__(self):
        super().__init__('Produkt jest niedostępny.')


class WithdrawException(VendingMachineException):
    """Klasa wyjątków wykorzystywana w informowaniu o błędzie, jej wystąpienie nie kończy działania programu
    CLASS:
    *WithdrawException - informuje, że klient nie wrzucił żadnych monet, wiec zwrot monet jest niemożliwy."""
    def __init__(self):
        super().__init__('Brak wrzuconych monet.')


