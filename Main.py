from GUI import *


class Program(Frame):

    def __init__(self):
        super().__init__()
        self._machine = VendingMachine()
        self.initUI()

    def initUI(self):
        """
        Inicjalizacja GUI, ustawienie nazwy okna
        """
        self.master.title("Vending Machine")

        coin_ui = CoinUI(self._machine)
        product_ui = ProductsUI(self._machine)
        product_ui.pack(side=LEFT)
        coin_ui.pack(side=RIGHT)


def main():
    root = Tk()
    Program()
    root.geometry("700x450+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()
