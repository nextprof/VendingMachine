from Exceptions import *
from tkinter import *
from tkinter import messagebox
from functools import partial

class Item:
    def __init__(self, name):
        self.name = name


class Product(Item):
    def __init__(self, name, price):
        super(Product, self).__init__(name)
        self.price = price
        self.quantity = 5


def connect_dict(dictionary1, dictionary2):
    connected_dict = dictionary1.copy()
    for key in dictionary2:
        if key in connected_dict:
            connected_dict[key] += dictionary2[key]
        else:
            connected_dict[key] = dictionary2[key]
    return connected_dict


def get_coin_amount(dictionary):
    counter = 0
    for key, value in dictionary.items():
        counter += value
    return counter


class VendingMachine:
    coin_types = [1, 2, 5, 10, 20, 50, 100, 200, 500]
    coins = None

    products = {}

    def __init__(self):
        super().__init__()

        self.init_products()

        self.init_coins_dicts()

    def init_coins_dicts(self):
        self.coins = {}
        for c in self.coin_types:
            self.coins[c] = {
                'owned': 1,
                'inserted': 0
            }

    def get_inserted(self):
        return {key: self.coins[key]['inserted'] for key, value in self.coins.items() if
                self.coins[key]['inserted'] > 0}

    def get_inserted_value(self):
        val = 0
        for key, value in self.coins.items():
            val += key * value['inserted']
        return val

    def check_available_coins(self, dictionary):
        for key, value in dictionary.items():
            available = self.coins[key]['owned'] + self.coins[key]['inserted']
            if value > available:
                return False
        return True

    def payment(self, product_number):
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
        if product_number not in self.products:
            raise InvalidProductNumberException
        return self.products[product_number].price

    def withdraw(self):
        if self.get_inserted_value() == 0:
            raise WithdrawException
        all_inserted = self.get_inserted().copy()
        self.clear_inserted()
        return all_inserted

    def clear_inserted(self):
        for key in self.coins:
            self.coins[key]['inserted'] = 0

    def insert_coin(self, v):
        self.coins[v]['inserted'] += 1

    def init_products(self):
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


class BorderFrame(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.configure(borderwidth=2, relief="ridge")


class CoinUI(BorderFrame):
    def __init__(self, machine):
        super().__init__()

        self.machine = machine
        self.chosen_product = None
        self.coins_value_string = StringVar()
        self.coins_value_string.set("0.0")
        self.product_number_string = StringVar()
        self.product_number_string.set("")
        self.initUI()

    def add(self, v):
        self.machine.insert_coin(v)
        self.update_entries()

    def update_entries(self):
        print(self.machine.get_inserted_value())
        coin_value = self.machine.get_inserted_value()
        self.coins_value_string.set(float("{0:.2f}".format(coin_value / 100)))

    def initUI(self):
        self.pack(fill=BOTH, expand=True)

        counter = 0
        frame = BorderFrame(self)
        frame.pack()
        f = None
        for key in self.machine.coins:
            if counter % 3 == 0:
                f = Frame(frame)
                f.pack()
            part = partial(self.add, key)
            if float(key) < 100:
                text = str(int(key)) + " gr"
            else:
                text = str(int(key / 100)) + " zł"

            button = Button(f, command=part, text=text, width=6, bg="#f7f1b5")
            button.pack(side=LEFT, padx=5, pady=5)
            counter += 1

        f = Frame(self)
        f.pack()

        frame = Frame(f)
        frame.pack()
        label = Label(frame, text="Kredyty")
        label.pack(side=LEFT, padx=(30, 3), pady=5)
        entry = Entry(frame, textvariable=self.coins_value_string, state='readonly', justify='right', width=12)
        entry.pack(padx=(4, 15), pady=5)

        frame = Frame(f)
        frame.pack()
        label = Label(frame, text="Numer")
        label.pack(side=LEFT, padx=(30, 5), pady=5)
        entry = Entry(frame, textvariable=self.product_number_string, state='readonly', justify='right', width=12)
        entry.pack(padx=(5, 15), pady=5)

        frame = BorderFrame(self)
        frame.pack()
        for i in range(1, 11):
            if i % 3 == 1:
                f = Frame(frame)
                f.pack()
            if i == 10:
                part = partial(self.keyboard_click, -2)
                button = Button(f, command=part, text='Clear', width=6, bg="#bfaaaf")
                button.pack(side=LEFT, padx=5, pady=5)
            part = partial(self.keyboard_click, i % 10)
            button = Button(f, command=part, text=i % 10, width=6)
            button.pack(side=LEFT, padx=5, pady=5)
            if i == 10:
                part = partial(self.keyboard_click, -1)
                button = Button(f, command=part, text='<', width=6, bg="#bfaaaf")
                button.pack(side=LEFT, padx=5, pady=5)

        f = Frame(self)
        f.pack()
        frame = Frame(f)
        frame.pack()
        button = Button(frame, command=self.withdraw, text="Wypłać", width=6, bg="#c91c2d")
        button.pack(side=LEFT, padx=5, pady=5)
        button = Button(frame, command=self.pay, text="Zapłać", width=6, bg="#1ca6c9")
        button.pack(side=LEFT, padx=5, pady=5)

    def keyboard_click(self, v):
        if v == -1:
            number = self.product_number_string.get()
            if len(number) > 1:
                number = int(number)
                number /= 10
                self.product_number_string.set(int(number))
            else:
                self.product_number_string.set('')
        elif v == -2:
            self.product_number_string.set("")
        else:
            number = self.product_number_string.get()
            if len(number) > 0:
                number = int(number)
                number *= 10
                v += number
            self.product_number_string.set(v)

    def pay(self):
        if self.product_number_string.get() == '':
            return
        else:
            try:
                value, product = self.machine.payment(int(self.product_number_string.get()))
                info_1 = "Zakupiono produkt:\n\n\t" + product.name + '\n\n'
                if type(value) is str:
                    messagebox.showinfo('OK', info_1 + value)
                else:
                    info_2 = "Reszta:"
                    for k, v in value.items():
                        if k < 100:
                            t = str(int(k)) + ' gr'
                        else:
                            t = str(int(k / 100)) + ' zł'
                        info_2 += "\n\t" + str(int(v)) + ' x ' + t
                    messagebox.showinfo('OK', info_1 + info_2)  # INFO 2- RESZTA STRING

                self.product_number_string.set('')
                self.update_entries()
            except VendingMachineException as e:
                messagebox.showinfo('Error', e.msg)

    def withdraw(self):
        try:
            all_inserted = self.machine.withdraw()
            info_1 = "Wypłacono:"
            for k in all_inserted:
                if k < 100:
                    t = str(int(k)) + ' gr'
                else:
                    t = str(int(k / 100)) + ' zł'
                info_1 += "\n\t" + str(int(all_inserted[k])) + ' x ' + t
            messagebox.showinfo('OK', info_1)
            self.product_number_string.set('')
            self.update_entries()
        except VendingMachineException as e:
            messagebox.showinfo('Warning', e.msg)


class ProductsUI(BorderFrame):
    def __init__(self, machine):
        super().__init__()
        self.machine = machine

        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=True)
        product_color_hex = "#17e3a2"
        counter = 0
        f = None
        for number, product in self.machine.products.items():
            if counter % 4 == 0:
                f = Frame(self)
                f.pack()

            product_frame = Frame(f, borderwidth=2, relief="ridge", bg=product_color_hex)
            Label(product_frame, text=str(number), width=11, bg=product_color_hex).pack(padx=5, pady=2)
            Label(product_frame, text=str(product.name), bg=product_color_hex).pack(padx=5, pady=2)
            Label(product_frame,
                  text="Cena: " + str("{0:.2f}".format(product.price / 100)), bg=product_color_hex).pack(padx=5, pady=2)

            product_frame.pack(side=LEFT, padx=5, pady=5)
            counter += 1
