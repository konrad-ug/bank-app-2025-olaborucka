from src.account import Account
import pytest

@pytest.fixture
def acc():
    return Account("John", "Doe", "12345678901")

class Testtransfer:
    
    # PROSTE WPŁATY I WYPŁATY

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

    def test_minus_transfer(self, acc):
        with pytest.raises(ValueError):
            acc.deposit(-200)

    # PRZELEWY EKSPRESOWE
    
    @pytest.mark.parametrize("initial_money, amount, expected_result", [
        (200, 100, 99),  
        (100, 100, -1)   
    ])
    def test_express_transfer_success(self, acc, initial_money, amount, expected_result):
        acc.deposit(initial_money)
        acc.express_transfer(amount)
        assert acc.balance == expected_result

    def test_express_transfer_underlowest(self, acc):
        acc.deposit(100)
        with pytest.raises(ValueError):
            acc.express_transfer(200)

    # HISTORIA

    def test_history_deposit(self, acc):
        acc.deposit(100)
        assert acc.history == [100]

    def test_history_withdraw(self, acc):
        acc.deposit(200)
        acc.withdraw(200)
        assert acc.history == [200, -200]

    def test_history_express(self, acc):
        acc.deposit(100)
        acc.express_transfer(100)
        assert acc.history == [100, -100, -1]