from src.account import BusinessAccount
import pytest


@pytest.fixture
def biz_acc():
    return BusinessAccount("firmax", "1234567890")

class Test_business_acc:
    
    # Poprawnego Konta

    def test_acc_create(self, biz_acc):
        assert biz_acc.company_name == "firmax"
        assert biz_acc.nip == "1234567890"

    def test_no_promo_for_business(self, biz_acc):

        assert biz_acc.balance == 0

    # Walidacji NIP

    @pytest.mark.parametrize("invalid_nip", [
        "123",         
        "12345678901",  
        "nipfirmy",     
        ""              
    ])
    def test_nip_validation_invalid(self, invalid_nip):
        acc = BusinessAccount("firmax", invalid_nip)
        assert acc.nip == "Invalid"