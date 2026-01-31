import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:5000/api/accounts"

class TestSaveLoad:
    
    def test_save_and_load_flow(self):

        pesel1 = "99010112345"
        pesel2 = "99010154321"
        
        requests.post(BASE_URL, json={"name": "Test1", "surname": "Save", "pesel": pesel1})
        requests.post(BASE_URL, json={"name": "Test2", "surname": "Save", "pesel": pesel2})

        requests.post(f"{BASE_URL}/{pesel1}/transfer", json={"amount": 500, "type": "incoming"})
 
        save_resp = requests.post(f"{BASE_URL}/save")
        assert save_resp.status_code == 200
        
        requests.delete(f"{BASE_URL}/{pesel1}")
        requests.delete(f"{BASE_URL}/{pesel2}")
        
        check = requests.get(f"{BASE_URL}/{pesel1}")
        assert check.status_code == 404
        
        load_resp = requests.post(f"{BASE_URL}/load")
        assert load_resp.status_code == 200
        
        acc1 = requests.get(f"{BASE_URL}/{pesel1}").json()
        assert acc1["name"] == "Test1"
        assert acc1["balance"] == 500 
        
        acc2 = requests.get(f"{BASE_URL}/{pesel2}").json()
        assert acc2["name"] == "Test2"