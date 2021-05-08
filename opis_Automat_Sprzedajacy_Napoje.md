3. Automat sprzedajacy napoje

Opis zadania

Automat przechowuje informacje o monetach znajdujacych sie w nim (1, 2, 5,
10, 20, 50gr, 1, 2, 5zł)
Automat przechowuje informacje o towarach znajdujacych sie w nim (przedmioty o
numerach od 30 do 50), kazdy o określonej cenie w okreslonej liczbie (domyślnie
po 5 sztuk każdego towaru)
Okno z przyciskami pozwalajacymi na wrzucanie monet, polem wyświetlajacym
kwote wrzuconych monet, przyciskiem przerywajacym transakcje (wyrzuca
wrzucone monety), przyciskami 0-9 pozwalajacymi wpisaé numer wybranego
towaru oraz polem wyswietlajacym wpisany numer towaru.
Po wybraniu poprawnego numeru towaru

Jesti wrzucono za mato monet, wyskakuje okno z informacja o cenie towaru
oraz (jesli towar sie skończyl) o jego braku w automacie.

Jesli wrzucono monety, których wartosć jest większa lub równa cenie wybranego
towaru, automat sprawdza czy towar jest dostepny i czy moze wydać reszte
 Brak towaru: wyskakuje okienko z informacja o braku w automacie,
 Brak reszty/moze wydac: wyskakuje okienko z informacja o
 zakupach, wydaje reszte (dolicza wrzucone monety, odlicza wydane
 jako reszta, odlicza wydany towar), odejmuje towar.
 Nie moze wydać: wyskakuje okienko z napisem *Tylko odliczona kwota”.

Testy

1.Sprawdzenie ceny jednego towaru - oczekiwana informacja o cenie.
2.Wrzucenie odliczonej kwoty, zakup towaru - oczekiwany brak reszty.
3.Wrzucenie wiekszej kwoty, zakup towaru - oczekiwana reszta.
4.Wykupienie calego asortymentu, proba zakupu po wyczerpaniu towaru -
oczekiwana informacja o braku.
5.Sprawdzenie ceny towaru o nieprawidtowym numerze (<30 lub >50) -
oczekiwana informacja o błędzie
6.Wrzucenie kilku monet, przerwanie transakcji - oczekiwany zwrot monet.
7.Wrzucenie za małej kwoty, wybranie poprawnego numeru towaru, wrzucenie
reszty monet do odliczonej kwoty, ponowne wybranie poprawnego numeru towaru
- oczekiwany brak reszty.
8.Zakup towaru placac po 1 gr - suma stu monet ma byé równa 1zł (dla floatow
suma sto razy 0,01+0,01+...+0.01 nie bedzie równa 1.0), Platności mozna dokonać
za pomoca petli for w interpreterze.

https://github.com/nextprof/VendingMachine