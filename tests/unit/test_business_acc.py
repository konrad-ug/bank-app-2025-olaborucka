from src.account import BusinessAccount
import pytest
from unittest.mock import patch

# Fixture z mockiem - "udajemy", że API zawsze potwierdza NIP
@pytest.fixture
def biz_acc():
    with patch.object(BusinessAccount, 'verify_nip_with_gov', return_value=True):
        return BusinessAccount("firmax", "1234567890")

class Test_business_acc:
    
    def test_acc_create(self, biz_acc):
        assert biz_acc.company_name == "firmax"
        assert biz_acc.nip == "1234567890"

    def test_no_promo_for_business(self, biz_acc):
        assert biz_acc.balance == 0

    @pytest.mark.parametrize("invalid_nip", ["123", "12345678901", "nipfirmy", ""])
    def test_nip_validation_invalid(self, invalid_nip):
        # Tu nie musimy mockować, bo kod sprawdza długość PRZED requestem
        acc = BusinessAccount("firmax", invalid_nip)
        assert acc.nip == "Invalid"

    # --- NOWE TESTY FEATURE 18 ---

    def test_create_acc_with_non_existing_nip(self):
        """Sprawdza, czy rzuca błąd, gdy API mówi 'False'."""
        # Udajemy, że API zwróciło False (firma nie istnieje)
        with patch.object(BusinessAccount, 'verify_nip_with_gov', return_value=False):
            with pytest.raises(ValueError, match="Company not registered!!"):
                BusinessAccount("Januszex", "1234567890")

    @patch('src.account.requests.get')
    def test_verify_nip_real_call_mocked(self, mock_get):
        """Sprawdza logikę metody verify_nip_with_gov (mockując tylko requests)."""
        # Symulujemy odpowiedź z API: statusVat = Czynny
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": {"subject": {"statusVat": "Czynny"}}
        }

        # Tworzymy konto (musimy zmockować init, żeby przejść walidację w konstruktorze, 
        # a potem przetestować metodę verify_nip_with_gov ręcznie)
        with patch.object(BusinessAccount, 'verify_nip_with_gov', return_value=True):
            acc = BusinessAccount("Firma", "1234567890")
        
        # Testujemy samą metodę - teraz mockujemy tylko 'requests.get', 
        # więc logika wewnątrz verify_nip_with_gov zostanie wykonana
        assert acc.verify_nip_with_gov("1234567890") is True