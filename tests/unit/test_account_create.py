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
        assert len(acc.pesel) == 11

    def test_invalid_pesel_sets_invalid_string(self):
        acc = Account("John", "Doe", "12345")  # za krótki pesel
        assert acc.pesel == "invalid"

    def test_pesel_is_string(self):
        acc = Account("John", "Doe", "mamamakota")
        assert acc.pesel == "invalid"

    def test_promo_code_adds_bonus(self):
        acc = Account("John", "Doe", "80010112345", promo_code="PROM_ABC")
        assert acc.balance == 50

    def test_promo_code_none(self):
        acc = Account("John", "Doe", "80010112345")
        assert acc.balance == 0

    def test_promo_code_invalid_format(self):
        acc = Account("John", "Doe", "80010112345", promo_code="ABC_PROM")
        assert acc.balance == 0

    def test_ineligible_promo_invalid_pesel(self):
        acc = Account("John", "Doe", "1234")  # za krótki PESEL
        assert acc._is_eligible_for_promo() is False

    def test_ineligible_promo_non_digit_pesel(self):
        acc = Account("John", "Doe", "abcdefghijk")
        assert acc._is_eligible_for_promo() is False

    def test_promo_not_for_1959(self):
        acc = Account("Adam", "Nowak", "59010112345", promo_code="PROM_XYZ")
        assert acc.balance == 0  # brak bonusu, bo 1959

    def test_promo_yes_for_2005(self):
        acc = Account("Ola", "Kowalska", "05210112345", promo_code="PROM_XYZ")
        assert acc.balance == 50  # działa, bo 2005 > 1960

    def test_promo_year_2100(self):
        acc = Account("John", "Doe", "01410000000")  # mm = 41 → rok 2101
        assert acc._is_eligible_for_promo() is not False

    def test_promo_year_2200(self):
        acc = Account("John", "Doe", "01610000000")  # mm = 61 → rok 2201
        assert acc._is_eligible_for_promo() is not False

    def test_promo_year_1800(self):
        acc = Account("John", "Doe", "01810000000")  # mm = 81 → rok 1801
        assert acc._is_eligible_for_promo() is False

    def test_invalid_month_range(self):
        acc = Account("John", "Doe", "01990000000")  # mm = 99 → else: return False
        assert acc._is_eligible_for_promo() is False

