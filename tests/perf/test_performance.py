import pytest
import requests
import random

BASE_URL = "http://127.0.0.1:5000/api/accounts"

class TestPerformance:
    
    def test_perf_create_and_delete_account(self):
        """
        Tworzy i usuwa konto 100 razy.
        Wymaga czasu odpowiedzi < 0.5s dla każdej operacji.
        """
        for _ in range(100):
            # Generujemy losowy PESEL, żeby nie było konfliktów
            pesel = f"991122{random.randint(10000, 99999)}"
            payload = {
                "name": "Perf",
                "surname": "Test",
                "pesel": pesel
            }

            # 1. Tworzenie (z timeoutem 0.5s)
            try:
                create_resp = requests.post(BASE_URL, json=payload, timeout=0.5)
                assert create_resp.status_code == 201
            except requests.Timeout:
                pytest.fail(f"Create account timed out (>0.5s) for pesel {pesel}")

            # 2. Usuwanie (z timeoutem 0.5s)
            try:
                delete_resp = requests.delete(f"{BASE_URL}/{pesel}", timeout=0.5)
                assert delete_resp.status_code == 200
            except requests.Timeout:
                pytest.fail(f"Delete account timed out (>0.5s) for pesel {pesel}")

    def test_perf_incoming_transfers(self):
        """
        Tworzy konto i wykonuje 100 przelewów przychodzących.
        Wymaga czasu odpowiedzi < 0.5s dla każdego przelewu.
        Sprawdza końcowe saldo.
        """
        # Setup: Tworzymy jedno konto
        pesel = f"881122{random.randint(10000, 99999)}"
        create_payload = {"name": "Perf", "surname": "Transfer", "pesel": pesel}
        requests.post(BASE_URL, json=create_payload)

        transfer_count = 100
        amount_per_transfer = 10

        # Action: 100 przelewów
        for _ in range(transfer_count):
            transfer_payload = {
                "amount": amount_per_transfer,
                "type": "incoming"
            }
            try:
                resp = requests.post(f"{BASE_URL}/{pesel}/transfer", json=transfer_payload, timeout=0.5)
                assert resp.status_code == 200
            except requests.Timeout:
                pytest.fail(f"Transfer timed out (>0.5s) for pesel {pesel}")

        # Assert: Sprawdzenie salda
        get_resp = requests.get(f"{BASE_URL}/{pesel}")
        assert get_resp.status_code == 200
        expected_balance = transfer_count * amount_per_transfer
        assert get_resp.json()["balance"] == expected_balance
        
        # Cleanup (opcjonalnie): Usunięcie konta
        requests.delete(f"{BASE_URL}/{pesel}")