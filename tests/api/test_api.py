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
        response = requests.get(f"{BASE_URL}/00000000000")
        assert response.status_code == 404
        assert response.json()["message"] == "Account not found"

    def test_update_account(self, uni_pesel):
        requests.post(BASE_URL, json={
            "name": "OldName", 
            "surname": "OldSurname", 
            "pesel": uni_pesel
        })

        update_data = {"surname": "NewSurname"}
        response = requests.patch(f"{BASE_URL}/{uni_pesel}", json=update_data)
        assert response.status_code == 200

        check = requests.get(f"{BASE_URL}/{uni_pesel}")
        data = check.json()
        assert data["surname"] == "NewSurname"
        assert data["name"] == "OldName"

    def test_delete_account(self, uni_pesel):

        requests.post(BASE_URL, json={
            "name": "ToDel", 
            "surname": "ToDel", 
            "pesel": uni_pesel
        })


        response = requests.delete(f"{BASE_URL}/{uni_pesel}")
        assert response.status_code == 200

        check = requests.get(f"{BASE_URL}/{uni_pesel}")
        assert check.status_code == 404

    def test_create_duplicate_account(self, uni_pesel):
        payload ={
            "name": "name",
            "surname" :"surname",
            "pesel": uni_pesel
        }
        response_1= requests.post(BASE_URL, json=payload)
        assert response_1.status_code == 201

        response_2 = requests.post(BASE_URL, json=payload)
        assert response_2.status_code == 409
        assert response_2.json()["message"] == "Account with this pesel already exists"
        
    def test_transfer_incoming(self, uni_pesel):
        """1. Test wpłaty (incoming) - saldo powinno wzrosnąć."""
        # Krok 1: Tworzymy konto (saldo 0)
        requests.post(BASE_URL, json={"name": "Jan", "surname": "Kow", "pesel": uni_pesel})
        
        # Krok 2: Robimy wpłatę
        response = requests.post(f"{BASE_URL}/{uni_pesel}/transfer", json={
            "amount": 1000,
            "type": "incoming"
        })
        assert response.status_code == 200
        assert response.json()["message"] == "demand accepted" # lub Twoja wiadomość
        
        # Krok 3: Sprawdzamy saldo
        check = requests.get(f"{BASE_URL}/{uni_pesel}")
        assert check.json()["balance"] == 1000

    def test_transfer_outgoing(self, uni_pesel):
        """2. Test wypłaty (outgoing) - saldo powinno zmaleć."""
        requests.post(BASE_URL, json={"name": "Jan", "surname": "Kow", "pesel": uni_pesel})
        
        # Najpierw wpłacamy 1000
        requests.post(f"{BASE_URL}/{uni_pesel}/transfer", json={"amount": 1000, "type": "incoming"})
        
        # Teraz wypłacamy 400
        response = requests.post(f"{BASE_URL}/{uni_pesel}/transfer", json={
            "amount": 400,
            "type": "outgoing"
        })
        assert response.status_code == 200
        
        # Sprawdzamy saldo (1000 - 400 = 600)
        check = requests.get(f"{BASE_URL}/{uni_pesel}")
        assert check.json()["balance"] == 600

    def test_transfer_outgoing_fail(self, uni_pesel):
        """3. Test błędu wypłaty (za mało środków) - kod 422."""
        requests.post(BASE_URL, json={"name": "Biedny", "surname": "Jan", "pesel": uni_pesel})
        
        # Konto ma saldo 0. Próbujemy wypłacić 100.
        response = requests.post(f"{BASE_URL}/{uni_pesel}/transfer", json={
            "amount": 100,
            "type": "outgoing"
        })
        
        # Oczekujemy błędu "Unprocessable Entity"
        assert response.status_code == 422
        # Opcjonalnie: sprawdź treść błędu
        # assert response.json()["message"] == "brak wystarczajacych srodkow na koncie"

    def test_transfer_invalid_type(self, uni_pesel):
        """4. Test nieznanego typu przelewu - kod 400."""
        requests.post(BASE_URL, json={"name": "Jan", "surname": "Kow", "pesel": uni_pesel})
        
        response = requests.post(f"{BASE_URL}/{uni_pesel}/transfer", json={
            "amount": 100,
            "type": "kradziez" # Nieznany typ
        })
        assert response.status_code == 400

    def test_transfer_account_not_found(self):
        """5. Przelew na nieistniejące konto - kod 404."""
        response = requests.post(f"{BASE_URL}/00000000000/transfer", json={
            "amount": 100,
            "type": "incoming"
        })
        assert response.status_code == 404

    