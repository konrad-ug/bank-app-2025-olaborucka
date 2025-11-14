from src.account import Account
import pytest 

class Test_credit:
    def test_three_actions(self):
        acc = Account("John", "Doe", "12345678901")
        acc.deposit(100)
        acc.deposit(200)
        acc.deposit(50)
        result = acc.submit_for_loan(300)
        assert result is True


    def test_three_deposits(self):
        acc = Account("John", "Doe", "12345678901")
        acc.deposit(100)
        acc.deposit(200)
        acc.deposit(50)
        assert all(t > 0 for t in acc.history[-3:])

    def test_5_lasttransaciotns(self):
        acc = Account("John", "Doe", "12345678901")
        acc.deposit(100)
        acc.deposit(200)
        acc.deposit(50)
        acc.withdraw(100)
        acc.express_transfer(10)
        result = acc.submit_for_loan(100)
        assert result is True

    def test_loan_denied(self):
        acc = Account("John", "Doe", "12345678901")
        acc.deposit(50)
        acc.withdraw(20)
        acc.withdraw(10)
        result = acc.submit_for_loan(1000)
        assert result is False




