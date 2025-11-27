from src.account import Account
import pytest

# Definiujemy fixturę lokalnie (chyba że masz ją w conftest.py, wtedy możesz ten fragment usunąć)
@pytest.fixture
def acc():
    return Account("John", "Doe", "12345678901")

class TestCredit:

    # --- SCENARIUSZ 1: Kredyt przyznany na podstawie 3 ostatnich wpłat ---
    
    def test_loan_approved_condition_deposits(self, acc):
        """Warunek 1: Ostatnie 3 transakcje to wpłaty."""
        # Przygotowanie historii
        acc.deposit(100)
        acc.deposit(200)
        acc.deposit(50)
        
        # Sprawdzenie
        assert acc.submit_for_loan(300) is True
        # Dodatkowo sprawdzamy, czy saldo wzrosło o kwotę kredytu
        assert acc.balance == 100 + 200 + 50 + 300

    # --- SCENARIUSZ 2: Kredyt przyznany na podstawie sumy transakcji ---

    def test_loan_approved_condition_sum(self, acc):
        """Warunek 2: Suma ostatnich 5 transakcji > kwota kredytu."""
        # Generujemy historię (5 wpłat po 100)
        acc.deposit(100)
        acc.deposit(100)
        acc.deposit(100)
        acc.deposit(100)
        acc.deposit(100) # Suma = 500
        
        # Psujemy warunek pierwszy (dodajemy wypłatę na koniec)
        acc.withdraw(50) 
        # Teraz historia ma 6 elementów. Ostatni to wypłata (-50), więc warunek 1 odpada.
        # Ale suma ostatnich 5 to: 100+100+100+100-50 = 350.
        
        # Wnioskujemy o 300 (350 > 300) -> Powinno przejść
        assert acc.submit_for_loan(300) is True

    # --- SCENARIUSZ 3: Kredyt odrzucony (Parametryzacja) ---

    @pytest.mark.parametrize("loan_amount", [
        1000, # Za duża kwota
        5000, # Jeszcze większa kwota
        100   # Nawet mała kwota nie przejdzie przy złej historii
    ])
    def test_loan_denied(self, acc, loan_amount):
        """Kredyt odrzucony: brak 3 wpłat z rzędu i za mała suma."""
        # Historia: Wpłata, Wypłata, Wypłata
        acc.deposit(50)
        acc.withdraw(20)
        acc.withdraw(10)
        
        # Żaden warunek nie jest spełniony
        assert acc.submit_for_loan(loan_amount) is False