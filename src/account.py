import requests
import os
from datetime import date
from src.smtp_client import SMTPClient 

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
    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "pesel": self.pesel,
            "balance": self.balance,
            "history": self.history,
            "type": "personal"
        }

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
        if self.balance - total < -fee:
            raise ValueError("Saldo nie może spaść poniżej dozwolonej opłaty.")
        self.balance -= amount
        self.history.append(-amount)
        self.balance -= fee
        self.history.append(-fee)

    def send_history_via_email(self, email):
        today = date.today().strftime("%Y-%m-%d")
        subject = f"Account Transfer History {today}"
        message = f"Personal account history: {self.history}"
        
        smtp = SMTPClient()
        return smtp.send(subject, message, email)

    def _check_last_3_deposits(self):
        if len(self.history) < 3:
            return False
        return all(t > 0 for t in self.history[-3:])

    def _check_sum_of_last_5_transactions(self, amount):
        if len(self.history) < 5:
            return False
        return sum(self.history[-5:]) > amount

    def submit_for_loan(self, amount):
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
        self.promo_code = None 

        if len(nip) != 10 or not nip.isdigit():
            self.nip = "Invalid"
        else:
            self.nip = nip
            if not self.verify_nip_with_gov(nip):
                raise ValueError("Company not registered!!")

    def verify_nip_with_gov(self, nip):
        try:
            base_url = os.environ.get("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl/")
            today = date.today().strftime("%Y-%m-%d")
            url = f"{base_url}api/search/nip/{nip}?date={today}"
            print(f"Sending request to: {url}")
            
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                subject = data.get("result", {}).get("subject")
                if subject and subject.get("statusVat") == "Czynny":
                    return True
            return False
        except Exception as e:
            print(f"Error checking NIP: {e}")
            return False

    def express_transfer(self, amount):
        fee = 5
        total = amount + fee
        if self.balance - total < -fee:
            raise ValueError("Saldo nie może spaść poniżej dozwolonej opłaty.")
        self.balance -= amount
        self.history.append(-amount)
        self.balance -= fee
        self.history.append(-fee)

    def take_loan(self, amount):
        if self.balance < 2* amount:
            return False
        if -1775 not in self.history:
            return False
        
        self.balance += amount
        self.history.append(amount)
        return True

    def send_history_via_email(self, email):
        today = date.today().strftime("%Y-%m-%d")
        subject = f"Account Transfer History {today}"
        message = f"Company account history: {self.history}"
        
        smtp = SMTPClient()
        return smtp.send(subject, message, email)
    def to_dict(self):
        return {
            "company_name": self.company_name,
            "nip": self.nip,
            "balance": self.balance,
            "history": self.history,
            "type": "business",
            "pesel": self.pesel 
        }