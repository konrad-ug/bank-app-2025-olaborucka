from behave import *
import requests

URL = "http://127.0.0.1:5000"

@step('I make a transfer of "{amount}" type "{transfer_type}" to account with pesel "{pesel}"')
def make_transfer(context, amount, transfer_type, pesel):
    json_body = {
        "amount": float(amount),
        "type": transfer_type
    }
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    assert response.status_code == 200, f"Transfer failed: {response.text}"

# TO JEST TEN BRAKUJĄCY FRAGMENT:
@then('Account with pesel "{pesel}" has balance equal to "{balance}"')
def check_balance(context, pesel, balance):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    assert response.json()["balance"] == float(balance)