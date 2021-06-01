from tkinter import *
from tkinter import messagebox
from functools import partial
from VendingMachine import *


class BorderFrame(Frame):
    """
    Klasa tworząca pole GUI z borderem
    """

    def __init__(self, master=None):
        super().__init__(master)
        self.configure(borderwidth=2, relief="ridge")


class CoinUI(BorderFrame):
    """
        Klasa tworząca GUI dla części odpowiedzialnej za zarządzanie monetami
    """

    def __init__(self, machine):
        super().__init__()

        self.machine = machine
        self.coins_value_string = StringVar()
        self.coins_value_string.set("0.0")
        self.product_number_string = StringVar()
        self.product_number_string.set("")
        self.initUI()

    def add(self, coin_type):
        """
        Metoda wprowadza monetę do "banku" automatu oraz ustawia nową wartość wprowadzonych monet na pole wyświetlające

        :param coin_type:
        """
        self.machine.insert_coin(coin_type)
        self.update_entries()

    def update_entries(self):
        """
        Ustawia wartość zmiennej odpowiedzialnej za wartość wprowadzonych monet
        """
        coin_value = self.machine.get_inserted_value()
        self.coins_value_string.set(float("{0:.2f}".format(coin_value / 100)))

    def initUI(self):
        """
        Metoda odpowiedzialna za inicjalizację całego GUI dla części związanej z monetami
        tworzenie przycisków związanych z wprowadzeniem numeru produktu,
        przycisków imitujących wprowadzanie monet do automatu,
        pól z dynamicznym wyświetlaniem numeru produktu oraz wartości wprowadzonych monet,
        przycisków odpowiedzialnych za czyszczenie dynamicznego pola tekstowego,
        przycisku cofającego ostatni wybrany numer produktu.
        Przycisków odpowiedzialnych za wypłatę wrzuconych monet bez kupna produktu oraz przycisku potwierdzającego kupno
        """
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
                button = Button(f, command=lambda: self.keyboard_click("clear"), text='Clear', width=6, bg="#bfaaaf")
                button.pack(side=LEFT, padx=5, pady=5)
            part = partial(self.keyboard_click, i % 10)
            button = Button(f, command=part, text=i % 10, width=6)
            button.pack(side=LEFT, padx=5, pady=5)
            if i == 10:
                button = Button(f, command=lambda: self.keyboard_click("remove"), text='<', width=6, bg="#bfaaaf")
                button.pack(side=LEFT, padx=5, pady=5)

        f = Frame(self)
        f.pack()
        frame = Frame(f)
        frame.pack()
        button = Button(frame, command=lambda: self.withdraw(), text="Wypłać", width=6, bg="#c91c2d")
        button.pack(side=LEFT, padx=5, pady=5)
        button = Button(frame, command=lambda: self.pay(), text="Zapłać", width=6, bg="#1ca6c9")
        button.pack(side=LEFT, padx=5, pady=5)

    def keyboard_click(self, intention):
        """
        Metoda obsługuje przycisk czyszczący dynamiczne pole tekstowe,
        oraz obsługuje przycisk cofający ostatni wybrany numer produktu.
        Dodatkowo aktualizuje pole wyświetlające numer produktu

        :param intention:
        """
        if intention == "remove":
            number = self.product_number_string.get()
            if len(number) > 1:
                number = int(number)
                number /= 10
                self.product_number_string.set(int(number))
            else:
                self.product_number_string.set('')
        elif intention == "clear":
            self.product_number_string.set("")
        else:
            number = self.product_number_string.get()
            if len(number) > 0:
                number = int(number)
                number *= 10
                intention += number
            self.product_number_string.set(intention)

    def pay(self):
        """
        Metoda wyświetla informacje o zakupionym produkcie oraz informacje o wydanej reszcie jeżeli istnieje.

        :return:
        """
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
                    messagebox.showinfo('OK', info_1 + info_2)

                self.product_number_string.set('')
                self.update_entries()
            except VendingMachineException as e:
                messagebox.showinfo('Error', e.msg)

    def withdraw(self):
        """
        Metoda odpowiedzialna za wypłacenie wprowadzonych monet
        """
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
    """
    Klasa tworząca GUI dla części odpowiedzialnej za wyświetlanie pól z produktami
    """

    def __init__(self, machine):
        super().__init__()
        self.machine = machine

        self.initUI()

    def initUI(self):
        """
            Metoda odpowiedzialna za inicjalizację całego GUI dla części związanej z produktami
            Tworzy pola w których znajduje się numer produktu, jego nazwa oraz cena.
        """
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
