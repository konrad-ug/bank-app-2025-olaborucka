from behave import *
import requests

URL = "http://127.0.0.1:5000"

@step('I create an account using name: "{name}", last name: "{last_name}", pesel: "{pesel}"')
def create_account(context, name, last_name, pesel):
    json_body = {
        "name": name,
        "surname": last_name,
        "pesel": pesel
    }
    create_resp = requests.post(URL + "/api/accounts", json=json_body)
    assert create_resp.status_code == 201, f"Failed to create account {pesel}. Status: {create_resp.status_code}, Msg: {create_resp.text}"

@step('Account registry is empty')
def clear_account_registry(context):
    response = requests.get(URL + "/api/accounts")
    assert response.status_code == 200, f"Failed to fetch accounts for cleanup. Status: {response.status_code}. Did you restart Flask?"
    
    accounts = response.json()
    for account in accounts:
        pesel = account["pesel"]
        del_resp = requests.delete(URL + f"/api/accounts/{pesel}")
        assert del_resp.status_code == 200, f"Failed to delete {pesel}"
    
    count_resp = requests.get(URL + "/api/accounts/count")
    assert count_resp.status_code == 200
    count = count_resp.json()["count"]
    assert count == 0, f"Registry cleanup failed: still has {count} accounts"

@step('Number of accounts in registry equals: "{count}"')
def is_account_count_equal_to(context, count):
    response = requests.get(URL + "/api/accounts/count")
    assert response.status_code == 200
    current_count = response.json()["count"]
    assert current_count == int(count), f"Expected {count} accounts, but got {current_count}"

@step('Account with pesel "{pesel}" exists in registry')
def check_account_with_pesel_exists(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200, f"Account {pesel} not found"
    assert response.json()["pesel"] == pesel

@step('Account with pesel "{pesel}" does not exist in registry')
def check_account_with_pesel_does_not_exist(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 404, f"Account {pesel} should not exist but does"

@when('I delete account with pesel: "{pesel}"')
def delete_account(context, pesel):
    response = requests.delete(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200, f"Delete failed: {response.text}"

@when('I update "{field}" of account with pesel: "{pesel}" to "{value}"')
def update_field(context, field, pesel, value):
    if field not in ["name", "surname"]:
        raise ValueError(f"Invalid field: {field}. Must be 'name' or 'surname'.")
    
    json_body = { field: value }
    response = requests.patch(URL + f"/api/accounts/{pesel}", json=json_body)
    assert response.status_code == 200, f"Update failed: {response.text}"

@then('Account with pesel "{pesel}" has "{field}" equal to "{value}"')
def field_equals_to(context, pesel, field, value):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    data = response.json()
    assert data[field] == value

@step('I make a transfer of "{amount}" type "{transfer_type}" to account with pesel "{pesel}" and expect status "{status}"')
def make_transfer_expect_status(context, amount, transfer_type, pesel, status):
    json_body = {
        "amount": float(amount),
        "type": transfer_type
    }
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    assert response.status_code == int(status), f"Expected status {status}, but got {response.status_code}"

@step('Account with pesel "{pesel}" has balance equal to "{balance}"')
def account_balance_equals(context, pesel, balance):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    data = response.json()
    assert str(data["balance"]) == balance, f"Expected balance {balance}, but got {data['balance']}"