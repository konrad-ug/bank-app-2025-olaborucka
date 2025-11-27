from src.account import BusinessAccount
import pytest

# 1. Definiujemy fixturę dla Konta Firmowego
# Ustawiamy poprawny NIP (10 cyfr), żeby konto było w pełni sprawne.
@pytest.fixture
def biz_acc():
    return BusinessAccount("Januszex", "1234567890")

class Test_buisness_acc_transfers:

    # --- Testy Podstawowe (Wpłaty/Wypłaty) ---

    def test_business_deposit(self, biz_acc):
        biz_acc.deposit(100)
        assert biz_acc.balance == 100

    def test_business_withdraw(self, biz_acc):
        biz_acc.deposit(100)
        biz_acc.withdraw(60)
        assert biz_acc.balance == 40

    def test_business_withdraw_error(self, biz_acc):
        """Sprawdza błąd przy próbie wypłaty ponad stan."""
        biz_acc.deposit(100)
        with pytest.raises(ValueError):
            biz_acc.withdraw(200)

    # --- Testy Przelewów Ekspresowych (Parametryzacja) ---
    # Łączymy: test_business_express_trensfer i test_business_express_trasfer_lowest
    # Pamiętamy: Opłata dla firm to 5 zł!
    
    @pytest.mark.parametrize("initial_money, transfer_amount, expected_balance", [
        (200, 100, 95), # 200 - 100 - 5 = 95
        (100, 100, -5)  # 100 - 100 - 5 = -5 (limit debetu to -5)
    ])
    def test_business_express_transfer_success(self, biz_acc, initial_money, transfer_amount, expected_balance):
        biz_acc.deposit(initial_money)
        biz_acc.express_transfer(transfer_amount)
        assert biz_acc.balance == expected_balance

    # --- Testy Graniczne i Historia ---

    def test_business_express_transfer_insufficient_funds(self, biz_acc):
        """Sprawdza, czy rzuca błąd, gdy przekroczymy limit (saldo < -5)."""
        biz_acc.deposit(100)
        with pytest.raises(ValueError):
            biz_acc.express_transfer(200) # Po operacji byłoby -105, a limit to -5

    def test_business_history_updates(self, biz_acc):
        """Sprawdza historię po przelewie ekspresowym."""
        biz_acc.deposit(100)
        biz_acc.express_transfer(100)
        # Oczekiwana historia: [Wpłata 100, Przelew -100, Opłata -5]
        assert biz_acc.history == [100, -100, -5]