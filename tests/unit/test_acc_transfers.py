
from src.account import Account
import pytest

@pytest.fixture
def acc():
    return Account("John", "Doe", "12345678901")


class Testtransfer:
    def test_saldo_deposit(self, acc):
        acc.deposit(100)
        assert acc.balance == 100

    def test_withdraw_decrease(self, acc):
        acc.deposit(100)
        acc.withdraw(10)
        assert acc.balance == 90

    def test_withdraw_nomoney(self, acc):
        acc.deposit(100)
        with pytest.raises(ValueError):
            acc.withdraw(200)

    def test_saldo_after_deposit(self, acc):
        prevsaldo = acc.balance
        acc.deposit(100)
        assert acc.balance == prevsaldo + 100

    def test_minus_transfer(self, acc):
        with pytest.raises(ValueError):
            acc.deposit(-200)

    def test_express_trensfer(self, acc):
        acc.deposit(200)
        acc.express_transfer(100)
        assert acc.balance == 99

    def test_express_trasfer_lowest(self, acc):

        acc.deposit(100)
        acc.express_transfer(100)
        assert acc.balance == -1

    def test_express_transfer_underlowest(self, acc):
        acc.deposit(100)
        with pytest.raises(ValueError):
            acc.express_transfer(200)

    def test_history_deposit(self,acc):
        acc.deposit(100)
        assert acc.history == [100]

    def test_history_withdraw(self,acc):
        acc.deposit(200)
        acc.withdraw(200)
        assert acc.history == [200,-200]

    def test_history_express(self,acc):
        acc.deposit(100)
        acc.express_transfer(100)
        assert acc.history == [100,-100, -1]





