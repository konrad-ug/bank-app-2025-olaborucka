from src.account import Account

class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "80010112345")
        assert account.first_name == "John"
        assert account.last_name == "Doe"

    def test_acc_balance_is0(self):
        acc = Account("John", "Doe", "80010112345")
        assert acc.balance == 0

    def test_acc_pesel(self):
        acc = Account("John", "Doe", "12345678901")
        assert acc.pesel == "12345678901"

    def test_acc_pesel_validation(self):
        acc = Account("John", "Doe", "12345678901")
        assert acc.pesel == "12345678901"

    def test_promo_code_adds_bonus(self):
        acc = Account("John", "Doe", "80010112345", promo_code="PROM_ABC")
        assert acc.balance == 50

    def test_promo_code_none(self):
        acc = Account("John", "Doe", "80010112345")
        assert acc.balance == 0

    def test_promo_code_invalid_format(self):
        acc = Account("John", "Doe", "80010112345", promo_code="ABC_PROM")
        assert acc.balance == 0

    def test_promo_not_for_1959(self):
        acc = Account("Adam", "Nowak", "59010112345", promo_code="PROM_XYZ")
        assert acc.balance == 0  # brak bonusu, bo 1959

    def test_promo_yes_for_2005(self):
        acc = Account("Ola", "Kowalska", "05210112345", promo_code="PROM_XYZ")
        assert acc.balance == 50  # działa, bo 2005 > 1960
