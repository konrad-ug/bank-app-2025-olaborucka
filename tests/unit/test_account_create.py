from src.account import Account
import pytest

# --- TU BYŁO BRAKUJĄCE OGNIWO! ---
# Definiujemy fixturę wewnątrz pliku, żeby testy ją widziały
@pytest.fixture
def acc():
    return Account("John", "Doe", "12345678901")
# ---------------------------------

class TestAccount:
    
    # --- GRUPA 1: Testy podstawowe ---
    def test_initial_attributes(self, acc):
        """Sprawdza, czy nowo utworzone konto ma poprawne dane startowe."""
        assert acc.balance == 0
        assert len(acc.pesel) == 11
        assert acc.first_name == "John" 

    # --- GRUPA 2: Walidacja błędnego PESELu ---
    @pytest.mark.parametrize("invalid_pesel", [
        "12345",          # Za krótki
        "1234567890123",  # Za długi
        "mamamakota",     # Litery zamiast cyfr
        "",               # Pusty string
    ])
    def test_pesel_validation_invalid_input(self, invalid_pesel):
        """Sprawdza, czy podanie błędnego PESELu ustawia go na 'invalid'."""
        acc = Account("John", "Doe", invalid_pesel)
        assert acc.pesel == "invalid"

    # --- GRUPA 3: Logika roczników i promocji ---
    @pytest.mark.parametrize("pesel, expected_eligible", [
        ("59010112345", False), # 1959 - za stary
        ("05210112345", True),  # 2005 - OK
        ("01410000000", True),  # 2101 - OK
        ("01610000000", True),  # 2201 - OK
        ("01810000000", False), # 1801 - za stary
        ("01990000000", False), # Błędny miesiąc
        ("1234", False),        # Za krótki pesel (długość)
        ("abcdefghijk", False)  # Litery
    ])
    def test_promo_eligibility_logic(self, pesel, expected_eligible):
        """Sprawdza logikę metody _is_eligible_for_promo dla różnych PESELi."""
        acc = Account("Test", "User", pesel)
        assert acc._is_eligible_for_promo() is expected_eligible

    # --- GRUPA 4: Kody promocyjne ---
    @pytest.mark.parametrize("promo_code, expected_balance", [
        ("PROM_ABC", 50), # Poprawny kod -> bonus
        (None, 0),        # Brak kodu -> brak bonusu
        ("ABC_PROM", 0),  # Zły format -> brak bonusu
        ("PROM", 0),      # Zły format (brak podłogi "_") -> brak bonusu.
    ])
    def test_initial_balance_with_promo_code(self, promo_code, expected_balance):
        """Sprawdza saldo początkowe w zależności od kodu promocyjnego."""
        valid_promo_pesel = "05210112345" 
        
        acc = Account("John", "Doe", valid_promo_pesel, promo_code=promo_code)
        assert acc.balance == expected_balance