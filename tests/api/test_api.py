import pytest
import requests
import random

BASE_URL = "http://127.0.0.1:5000/api/accounts"

@pytest.fixture
def uni_pesel():
    return "900101" + str( random.randint(10000, 99999))

class TestAccAPI:
    def test_create_and_get_acc(self, uni_pesel):
        payload = {
            "name": "James",
            "surname": "Hetfield",
            "pesel": uni_pesel
        }

        response = requests.post(BASE_URL, json=payload)
        assert response.status_code == 201

        response_get = requests.get(f"{BASE_URL}/{uni_pesel}")
        assert response_get.status_code ==200

        data = response_get.json()
        assert data["name"] == "James"
    
    def test_account_not_found(self):
        # Pytamy o PESEL, którego na pewno nie ma (np. same zera)
        response = requests.get(f"{BASE_URL}/00000000000")
        assert response.status_code == 404
        assert response.json()["message"] == "Account not found"

    def test_update_account(self, uni_pesel):
        # 1. SETUP: Tworzymy konto
        requests.post(BASE_URL, json={
            "name": "OldName", 
            "surname": "OldSurname", 
            "pesel": uni_pesel
        })

        # 2. ACTION: Aktualizujemy tylko nazwisko (PATCH)
        update_data = {"surname": "NewSurname"}
        response = requests.patch(f"{BASE_URL}/{uni_pesel}", json=update_data)
        assert response.status_code == 200

        # 3. ASSERT: Sprawdzamy czy zmiana zaszła
        check = requests.get(f"{BASE_URL}/{uni_pesel}")
        data = check.json()
        assert data["surname"] == "NewSurname"
        assert data["name"] == "OldName" # Imię powinno zostać stare

    def test_delete_account(self, uni_pesel):
        # 1. SETUP: Tworzymy konto
        requests.post(BASE_URL, json={
            "name": "ToDel", 
            "surname": "ToDel", 
            "pesel": uni_pesel
        })

        # 2. ACTION: Usuwamy (DELETE)
        response = requests.delete(f"{BASE_URL}/{uni_pesel}")
        assert response.status_code == 200

        # 3. ASSERT: Sprawdzamy, czy konto zniknęło (powinno zwrócić 404)
        check = requests.get(f"{BASE_URL}/{uni_pesel}")
        assert check.status_code == 404
