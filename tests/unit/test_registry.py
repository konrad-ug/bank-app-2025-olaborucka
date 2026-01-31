import pytest
from src.account import Account
from src.registry import AccountsRegistry


search_test_data = [
    ("12345678901", True), 
    ("00000000000", False),
    ("99999999999", False),
    ("", False)             
]

@pytest.fixture
def registry():
    return AccountsRegistry()

@pytest.fixture
def known_account():
    return Account("Jan", "Kowalski", "12345678901")

class TestAccountsRegistry:

    def test_add_account(self, registry, known_account):
        registry.add_account(known_account)
        assert registry.get_accounts_count() == 1

    
    @pytest.mark.parametrize("search_pesel, should_exist", search_test_data)
    def test_get_account_by_pesel(self, registry, known_account, search_pesel, should_exist):
        registry.add_account(known_account)

        result = registry.get_account_by_pesel(search_pesel)

        if should_exist:
            assert result == known_account
            assert result.pesel == "12345678901"
        else:
            assert result is None

    def test_delete_account_success(self,registry, known_account):
        registry.add_account(known_account)
        result = registry.delete_account(known_account.pesel)
        assert result is True
        assert registry.get_accounts_count() == 0

    def test_delete_account_fail(self, registry):
        result = registry.delete_account("00000000000")
        assert result is False

    def test_get_all_accounts(self, registry, known_account):
        registry.add_account(known_account)
        assert registry.get_all_accounts() == [known_account]

    def test_clear_registry(self, registry, known_account):
        registry.add_account(known_account)
        registry.clear()
        assert registry.get_accounts_count() == 0