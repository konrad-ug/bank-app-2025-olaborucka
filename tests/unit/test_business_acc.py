from src.account import BusinessAccount
import pytest

class Test_business_acc:
    def test_acc_create(self):
        acc = BusinessAccount("firmax", "1234567890")
        assert acc.company_name == "firmax"
        assert acc.nip == "1234567890"

    def test_nip_validation(self):
        acc = BusinessAccount("firmax", "123")
        assert acc.nip == "Invalid"

