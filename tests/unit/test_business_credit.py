from src.account import BusinessAccount
import pytest
from unittest.mock import patch

company_loan_tests = [
    ([-1775], 2000, 1000, True, 3000),
    ([-100, 500], 2000, 1000, False, 2000),
    ([-1775], 1000, 1000, False, 1000),
    ([], 5000, 1000, False, 5000),
]

test_ids = [
    "success_sufficient_balance_and_zus",
    "fail_no_zus_payment",
    "fail_insufficient_balance",
    "fail_empty_history"
]

@pytest.fixture
def biz_acc():
    with patch.object(BusinessAccount, 'verify_nip_with_gov', return_value=True):
        return BusinessAccount("Januszex", "1234567890")

class TestBusinessCredit:

    @pytest.mark.parametrize(
        "history, initial_balance, loan_amount, expected_result, expected_final_balance", 
        company_loan_tests, 
        ids=test_ids
    )
    def test_business_loan(self, biz_acc, history, initial_balance, loan_amount, expected_result, expected_final_balance):
        biz_acc.history = history
        biz_acc.balance = initial_balance

        result = biz_acc.take_loan(loan_amount)

        assert result is expected_result
        assert biz_acc.balance == expected_final_balance

    def test_business_loan_denied_no_zus_transfer(self, biz_acc):
        biz_acc.balance = 10000 
        biz_acc.history = [1000, 2000] 
        assert biz_acc.take_loan(1000) is False 

    def test_loan_denied_due_to_no_zus_only(self, biz_acc):
        biz_acc.balance = 10000  
        biz_acc.history = [500, 1000] 
        result = biz_acc.take_loan(1000)
        assert result is False
    