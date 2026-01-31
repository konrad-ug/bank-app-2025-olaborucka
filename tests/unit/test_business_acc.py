from src.account import BusinessAccount
import pytest
from unittest.mock import patch
import requests

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


    @patch('src.account.requests.get')
    def test_verify_nip_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError()
        with patch.object(BusinessAccount, 'verify_nip_with_gov', return_value=True):
            acc = BusinessAccount("Firma", "1234567890")

        assert acc.verify_nip_with_gov("1234567890") is False

    @patch('src.account.requests.get')
    def test_verify_nip_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError()
        with patch.object(BusinessAccount, 'verify_nip_with_gov', return_value=True):
            acc = BusinessAccount("Firma", "1234567890")
        
        assert acc.verify_nip_with_gov("1234567890") is False

    @patch('src.account.requests.get')
    def test_verify_nip_exception_path(self, mock_get):
        from src.account import BusinessAccount
        import requests
        mock_get.side_effect = Exception("Totalny błąd sieci")
        
        with pytest.raises(ValueError, match="Company not registered!!"):
             BusinessAccount("Psuja", "1234567890")
             
        with patch.object(BusinessAccount, 'verify_nip_with_gov', return_value=True):
             acc = BusinessAccount("Test", "1234567890")
        assert acc.verify_nip_with_gov("1234567890") is False 

    @patch('src.account.requests.get')
    def test_verify_nip_not_active_vat(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": {"subject": {"statusVat": "Zwolniony"}}
        }
        
        with patch.object(BusinessAccount, 'verify_nip_with_gov', return_value=True):
            acc = BusinessAccount("Firma", "1234567890")
        
        assert acc.verify_nip_with_gov("1234567890") is False

    def test_business_to_dict(self, biz_acc):
        biz_acc.deposit(1000)
        biz_acc.history = [1000]
        result = biz_acc.to_dict()
        
        assert result["company_name"] == "firmax"
        assert result["balance"] == 1000
        assert result["type"] == "business"
        assert result["nip"] == "1234567890"