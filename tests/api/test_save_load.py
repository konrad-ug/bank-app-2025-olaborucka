import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:5000/api/accounts"

# Te testy wymagają działającego Mongo w tle
class TestSaveLoad:
    
    def test_save_and_load_flow(self):
        # 1. Wyczyść środowisko (opcjonalnie)
        # Tworzymy 2 konta
        pesel1 = "99010112345"
        pesel2 = "99010154321"
        
        requests.post(BASE_URL, json={"name": "Test1", "surname": "Save", "pesel": pesel1})
        requests.post(BASE_URL, json={"name": "Test2", "surname": "Save", "pesel": pesel2})
        
        # Zmieniamy saldo
        requests.post(f"{BASE_URL}/{pesel1}/transfer", json={"amount": 500, "type": "incoming"})
        
        # 2. Zapisz do bazy (SAVE)
        save_resp = requests.post(f"{BASE_URL}/save")
        assert save_resp.status_code == 200
        
        # 3. Usuń konto "z pamięci" (DELETE przez API)
        requests.delete(f"{BASE_URL}/{pesel1}")
        requests.delete(f"{BASE_URL}/{pesel2}")
        
        # Upewnij się, że zniknęły
        check = requests.get(f"{BASE_URL}/{pesel1}")
        assert check.status_code == 404
        
        # 4. Załaduj z bazy (LOAD)
        load_resp = requests.post(f"{BASE_URL}/load")
        assert load_resp.status_code == 200
        
        # 5. Sprawdź czy konta wróciły i mają poprawne dane
        acc1 = requests.get(f"{BASE_URL}/{pesel1}").json()
        assert acc1["name"] == "Test1"
        assert acc1["balance"] == 500 # Saldo musi być zachowane!
        
        acc2 = requests.get(f"{BASE_URL}/{pesel2}").json()
        assert acc2["name"] == "Test2"