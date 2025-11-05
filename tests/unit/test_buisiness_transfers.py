from src.account import BusinessAccount
import pytest

class Test_buisness_acc_transfers:
    def test_business_deposit(self):
        acc = BusinessAccount("firmax", "123")
        acc.deposit(100)
        assert acc.balance == 100

    def test_business_withdraw(self):
        acc = BusinessAccount("firmax", "123")
        acc.deposit(100)
        acc.withdraw(60)
        assert acc.balance == 40

    def test_business_nomoney(self):
        acc = BusinessAccount("John", "12345678901")
        acc.deposit(100)
        with pytest.raises(ValueError):
            acc.withdraw(200)

    def test_business_saldo_after_deposit(self):
        acc = BusinessAccount("John", "12345678901")
        prevsaldo = acc.balance
        acc.deposit(100)
        assert acc.balance == prevsaldo + 100

    def test_business_express_trensfer(self):
        acc = BusinessAccount("John", "12345678901")
        acc.deposit(200)
        acc.express_transfer(100)
        assert acc.balance == 95

    def test_business_express_trasfer_lowest(self):
        acc = BusinessAccount("John", "12345678901")
        acc.deposit(100)
        acc.express_transfer(100)
        assert acc.balance == -5

    def test_business_express_transfer_underlowest(self):
        acc = BusinessAccount("John", "12345678901")
        acc.deposit(100)
        with pytest.raises(ValueError):
            acc.express_transfer(200)

