class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0
        self.history = []

        if len(pesel) == 11:
            self.pesel = pesel
        else:
            self.pesel = "invalid"

        self.promo_code = promo_code
        if promo_code and promo_code.startswith("PROM_") and self._is_eligible_for_promo():
            self.balance += 50

    def _is_eligible_for_promo(self):
        pesel = self.pesel
        if len(pesel) != 11 or not pesel.isdigit():
            return False

        yy = int(pesel[0:2])
        mm = int(pesel[2:4])

        if 1 <= mm <= 12:
            year = 1900 + yy
        elif 21 <= mm <= 32:
            year = 2000 + yy
        elif 41 <= mm <= 52:
            year = 2100 + yy
        elif 61 <= mm <= 72:
            year = 2200 + yy
        elif 81 <= mm <= 92:
            year = 1800 + yy
        else:
            return False

        return year > 1960

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.history.append(amount)
        else:
            raise ValueError("nie mozna wpłacic ujemnej wartosci")

    def withdraw(self, amount):
        if self.balance < amount:
            raise ValueError("brak wystarczajacych srodkow na koncie")
        self.balance -= amount
        self.history.append(-amount)


    def express_transfer(self, amount):
        fee = 1
        total = amount + fee
        # można spaść do -fee, ale nie niżej
        if self.balance - total < -fee:
            raise ValueError("Saldo nie może spaść poniżej dozwolonej opłaty.")
        self.balance -= amount
        self.history.append(-amount)
        self.balance -= fee
        self.history.append(-fee)

    def _check_last_3_deposits(self):
        """Metoda pomocnicza: sprawdza warunek 3 ostatnich wpłat."""
        if len(self.history) < 3:
            return False
        return all(t > 0 for t in self.history[-3:])

    def _check_sum_of_last_5_transactions(self, amount):
        """Metoda pomocnicza: sprawdza warunek sumy 5 transakcji."""
        if len(self.history) < 5:
            return False
        return sum(self.history[-5:]) > amount

    def submit_for_loan(self, amount):
        """Główna metoda kredytowa - teraz jest czysta i czytelna."""
        # Sprawdzamy, czy którykolwiek z warunków jest spełniony
        condition1 = self._check_last_3_deposits()
        condition2 = self._check_sum_of_last_5_transactions(amount)

        if condition1 or condition2:
            self.balance += amount
            self.history.append(amount)
            return True
            
        return False




class BusinessAccount(Account):
    def __init__(self, company_name, nip):
        super().__init__(first_name=None, last_name=None, pesel="00000000000")
        self.company_name = company_name

        if len(nip) == 10 and nip.isdigit():
            self.nip = nip
        else:
            self.nip = "Invalid"

        self.promo_code = None  # brak promocji

    def express_transfer(self, amount):
        fee = 5
        total = amount + fee
        # można spaść do -fee, ale nie niżej
        if self.balance - total < -fee:
            raise ValueError("Saldo nie może spaść poniżej dozwolonej opłaty.")
        self.balance -= amount
        self.history.append(-amount)
        self.balance -= fee
        self.history.append(-fee)
