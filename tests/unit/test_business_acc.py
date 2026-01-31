from src.account import BusinessAccount
import pytest
from unittest.mock import patch

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
        acc = BusinessAccount("firmax", invalid_nip)
        assert acc.nip == "Invalid"

    def test_create_acc_with_non_existing_nip(self):
        """Sprawdza, czy rzuca błąd, gdy API mówi 'False'."""
        with patch.object(BusinessAccount, 'verify_nip_with_gov', return_value=False):
            with pytest.raises(ValueError, match="Company not registered!!"):
                BusinessAccount("Januszex", "1234567890")

    @patch('src.account.requests.get')
    def test_verify_nip_real_call_mocked(self, mock_get):
        """Sprawdza logikę metody verify_nip_with_gov (mockując tylko requests)."""

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": {"subject": {"statusVat": "Czynny"}}
        }

        with patch.object(BusinessAccount, 'verify_nip_with_gov', return_value=True):
            acc = BusinessAccount("Firma", "1234567890")

        assert acc.verify_nip_with_gov("1234567890") is True