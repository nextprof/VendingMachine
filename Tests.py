import unittest
from VendingMachine import *
from Exceptions import *


class TestVendingMachine(unittest.TestCase):

    def setUp(self):
        self.vending_machine = VendingMachine()

    # Test sprawdzający cenę towaru
    def test_get_product_price(self):
        self.assertEqual(250, self.vending_machine.get_product_price(32))

    # Test oczekujący brak reszty
    def test_no_change(self):
        self.vending_machine.insert_coin(200)
        self.vending_machine.insert_coin(50)

        result = self.vending_machine.payment(32)
        self.assertEqual('Brak reszty.', result[0])

    # Test oczekujący 10gr reszty po wrzuconej nadwyżce
    def test_get10gr_change(self):
        self.vending_machine.coins[10]['owned'] = 1

        self.vending_machine.insert_coin(200)
        self.vending_machine.insert_coin(20)
        self.vending_machine.insert_coin(20)
        self.vending_machine.insert_coin(20)

        result = self.vending_machine.payment(32)
        self.assertEqual({10: 1}, result[0])

    # Test oczekujący wystąpienie wyjątku ProductUnavailableException gdy produkt jest niedostępny
    def test_out_of_stock(self):
        for i in range(5):
            self.vending_machine.insert_coin(200)
            self.vending_machine.insert_coin(50)
            self.vending_machine.payment(32)

        self.vending_machine.insert_coin(200)
        self.vending_machine.insert_coin(50)

        self.assertRaises(ProductUnavailableException, self.vending_machine.payment, 32)

    # Test oczekujący wystąpienie wyjątku InvalidProductNumberException gdy chcemy pobrać cenę nieistniejącego produktu
    def test_get_non_existing_product_price(self):
        self.assertRaises(InvalidProductNumberException, self.vending_machine.get_product_price, 5)

    # Test sprawdzający zwrot otrzymanych monet
    def test_withdraw_inserted_money(self):
        self.vending_machine.insert_coin(100)
        self.vending_machine.insert_coin(50)
        self.vending_machine.insert_coin(10)
        self.vending_machine.insert_coin(10)
        self.vending_machine.insert_coin(50)
        self.assertEqual({10: 2, 50: 2, 100: 1}, self.vending_machine.withdraw())

    # Test sprawdzający wrzucenie za małej kwoty, wybranie poprawnego numeru towaru,
    # wrzucenie reszty monet do odliczonej kwoty, ponowne wybranie poprawnego numeru towaru - oczekiwany brak reszty.
    def test_pay_missing_part(self):
        self.vending_machine.insert_coin(100)
        self.vending_machine.insert_coin(50)
        self.assertRaises(NotEnoughMoneyException, self.vending_machine.payment, 32)

        self.vending_machine.insert_coin(100)
        result = self.vending_machine.payment(32)
        self.assertEqual('Brak reszty.', result[0])

    # Test płatności odliczoną kwotą w monetach 1gr - oczekiwany brak reszty.
    def test_pay_in_cents(self):
        for i in range(250):
            self.vending_machine.insert_coin(1)
        result = self.vending_machine.payment(32)
        self.assertEqual('Brak reszty.', result[0])
