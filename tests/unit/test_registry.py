import pytest
from src.account import Account
from src.registry import AccountsRegistry


search_test_data = [
    # (Szukany PESEL, Czy spodziewamy się znaleźć? (True/False))
    ("12345678901", True),  # To jest PESEL Jana - powinien być
    ("00000000000", False), # Tego nie ma - None
    ("99999999999", False), # Tego też nie - None
    ("", False)             # Pusty string - None
]

@pytest.fixture
def registry():
    return AccountsRegistry()

@pytest.fixture
def known_account():
    return Account("Jan", "Kowalski", "12345678901")

class TestAccountsRegistry:

    def test_add_account(self, registry, known_account):
        """Prosty test dodawania (nie wymaga parametryzacji)."""
        registry.add_account(known_account)
        assert registry.get_accounts_count() == 1

    # --- PARAMETRYZACJA WYSZUKIWANIA ---
    
    @pytest.mark.parametrize("search_pesel, should_exist", search_test_data)
    def test_get_account_by_pesel(self, registry, known_account, search_pesel, should_exist):
        # 1. SETUP: Dodajemy "znane konto" do rejestru
        registry.add_account(known_account)

        # 2. ACTION: Szukamy podanego w parametrach PESEL-u
        result = registry.get_account_by_pesel(search_pesel)

        # 3. ASSERT: Sprawdzamy wynik
        if should_exist:
            # Jeśli miało znaleźć -> wynik musi być obiektem i to TYM KONKRETNYM obiektem
            assert result == known_account
            assert result.pesel == "12345678901"
        else:
            # Jeśli miało NIE znaleźć -> wynik musi być None
            assert result is None