from src.account import BusinessAccount
import pytest

# --- DANE TESTOWE (Tak jak na screenshocie) ---

# Struktura danych: (historia, saldo_początkowe, kwota_kredytu, oczekiwany_wynik, oczekiwane_saldo_końcowe)
company_loan_tests = [
    # Przypadek 1: Sukces (ZUS jest, saldo 2000 >= 2*1000)
    ([-1775], 2000, 1000, True, 3000),
    
    # Przypadek 2: Porażka - Brak ZUS (jest inna transakcja, saldo OK)
    ([-100, 500], 2000, 1000, False, 2000),
    
    # Przypadek 3: Porażka - Za małe saldo (ZUS jest, ale saldo 1000 < 2*1000)
    ([-1775], 1000, 1000, False, 1000),
    
    # Przypadek 4: Porażka - Pusta historia (Brak ZUS)
    ([], 5000, 1000, False, 5000),
]

# Nazwy testów, które wyświetlą się w terminalu (ids)
test_ids = [
    "success_sufficient_balance_and_zus",
    "fail_no_zus_payment",
    "fail_insufficient_balance",
    "fail_empty_history"
]

@pytest.fixture
def biz_acc():
    return BusinessAccount("Januszex", "1234567890")

class TestBusinessCredit:

    @pytest.mark.parametrize(
        "history, initial_balance, loan_amount, expected_result, expected_final_balance", 
        company_loan_tests, 
        ids=test_ids
    )
    def test_business_loan(self, biz_acc, history, initial_balance, loan_amount, expected_result, expected_final_balance):
        # 1. SETUP - Ręczne ustawienie stanu obiektu (jak na screenie)
        # Nadpisujemy listę historii i saldo, zamiast robić deposit()
        biz_acc.history = history
        biz_acc.balance = initial_balance

        # 2. ACTION - Próba wzięcia kredytu
        result = biz_acc.take_loan(loan_amount)

        # 3. ASSERT - Sprawdzenie wyniku i salda końcowego
        assert result is expected_result
        assert biz_acc.balance == expected_final_balance