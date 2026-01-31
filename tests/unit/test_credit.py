from src.account import Account
import pytest


@pytest.fixture
def acc():
    return Account("John", "Doe", "12345678901")

class TestCredit:
    
    def test_loan_approved_condition_deposits(self, acc):
        acc.deposit(100)
        acc.deposit(200)
        acc.deposit(50)
        
        assert acc.submit_for_loan(300) is True
        assert acc.balance == 100 + 200 + 50 + 300


    def test_loan_approved_condition_sum(self, acc):
        acc.deposit(100)
        acc.deposit(100)
        acc.deposit(100)
        acc.deposit(100)
        acc.deposit(100)
        
        
        acc.withdraw(50) 
        assert acc.submit_for_loan(300) is True


    @pytest.mark.parametrize("loan_amount", [
        1000, 
        5000, 
        100   
    ])
    def test_loan_denied(self, acc, loan_amount):
        acc.deposit(50)
        acc.withdraw(20)
        acc.withdraw(10)
        
        assert acc.submit_for_loan(loan_amount) is False