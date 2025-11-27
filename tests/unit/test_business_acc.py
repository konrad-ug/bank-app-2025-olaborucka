from src.account import BusinessAccount
import pytest

# Definiujemy fixturę (lub jeśli masz ją w conftest.py, to pytest ją sam znajdzie)
@pytest.fixture
def biz_acc():
    return BusinessAccount("firmax", "1234567890")

class Test_business_acc:
    
    # --- Testy Poprawnego Konta (Używają fixtury) ---

    def test_acc_create(self, biz_acc):
        """Sprawdza, czy konto z fixtury ma poprawne dane."""
        assert biz_acc.company_name == "firmax"
        assert biz_acc.nip == "1234567890"

    def test_no_promo_for_business(self, biz_acc):
        """Konto firmowe nie powinno mieć promocji na start."""
        assert biz_acc.balance == 0

    # --- Testy Walidacji NIP (Parametryzacja) ---

    @pytest.mark.parametrize("invalid_nip", [
        "123",          # Za krótki
        "12345678901",  # Za długi (11 znaków)
        "nipfirmy",     # Litery
        ""              # Pusty
    ])
    def test_nip_validation_invalid(self, invalid_nip):
        """Sprawdza, czy błędny NIP jest ustawiany na 'Invalid'."""
        # Tu tworzymy konto ręcznie, bo testujemy konstruktor z błędnymi danymi
        acc = BusinessAccount("firmax", invalid_nip)
        assert acc.nip == "Invalid"