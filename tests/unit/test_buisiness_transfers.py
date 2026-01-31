from src.account import BusinessAccount
import pytest
from unittest.mock import patch

@pytest.fixture
def biz_acc():
    with patch.object(BusinessAccount, 'verify_nip_with_gov', return_value=True):
        return BusinessAccount("Januszex", "1234567890")

class Test_buisness_acc_transfers:

    def test_business_deposit(self, biz_acc):
        biz_acc.deposit(100)
        assert biz_acc.balance == 100

    def test_business_withdraw(self, biz_acc):
        biz_acc.deposit(100)
        biz_acc.withdraw(60)
        assert biz_acc.balance == 40

    def test_business_withdraw_error(self, biz_acc):
        biz_acc.deposit(100)
        with pytest.raises(ValueError):
            biz_acc.withdraw(200)

    @pytest.mark.parametrize("initial_money, transfer_amount, expected_balance", [
        (200, 100, 95), 
        (100, 100, -5)  
    ])
    def test_business_express_transfer_success(self, biz_acc, initial_money, transfer_amount, expected_balance):
        biz_acc.deposit(initial_money)
        biz_acc.express_transfer(transfer_amount)
        assert biz_acc.balance == expected_balance

    def test_business_express_transfer_insufficient_funds(self, biz_acc):
        biz_acc.deposit(100)
        with pytest.raises(ValueError):
            biz_acc.express_transfer(200)

    def test_business_history_updates(self, biz_acc):
        biz_acc.deposit(100)
        biz_acc.express_transfer(100)
        assert biz_acc.history == [100, -100, -5]