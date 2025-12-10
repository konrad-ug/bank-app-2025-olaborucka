from flask import Flask, request, jsonify
from src.account import Account
from src.registry import AccountsRegistry

app = Flask(__name__)
registry = AccountsRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Request create account: {data}")
    checkpesel = data["pesel"]
    if registry.get_account_by_pesel(checkpesel) != None:
        return jsonify({"message": "Account with this pesel already exists"}), 409
    
    try:
        account = Account(data["name"], data["surname"], data["pesel"])
        registry.add_account(account)
        return jsonify({"message": "Account created"}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    accounts = registry.get_all_accounts()
    # Musimy zamienić obiekty na format JSON (słowniki)
    result = [
        {
            "name": acc.first_name, 
            "surname": acc.last_name, 
            "pesel": acc.pesel,
            "balance": acc.balance
        } 
        for acc in accounts
    ]
    return jsonify(result), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    count = registry.get_accounts_count()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account = registry.get_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    
    return jsonify({
        "name": account.first_name, 
        "surname": account.last_name, 
        "pesel": account.pesel,
        "balance": account.balance
    }), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    account = registry.get_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404

    data = request.get_json()
    
    # Aktualizujemy TYLKO to, co przyszło w requescie
    if "name" in data:
        account.first_name = data["name"]
    if "surname" in data:
        account.last_name = data["surname"]
    # Peselu zazwyczaj się nie zmienia, więc go pomijamy

    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    deleted = registry.delete_account(pesel)
    if deleted:
        return jsonify({"message": "Account deleted"}), 200
    else:
        return jsonify({"message": "Account not found"}), 404
    
@app.route("/api/accounts/<pesel>/transfer", methods={'POST'})
def transfer_money(pesel):
    account = registry.get_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    
    data = request.get_json()
    amnt = data["amount"]
    try:
        if data["type"] == "incoming" :
            account.deposit(amnt)

        elif data["type"] == "outgoing" :
            account.withdraw(amnt)
        
        elif data["type"] == "express" :
            account.express_transfer(amnt)
        else:
            jsonify({"message": "Invalid transfer type"}), 400

        return jsonify({"message ": "demand accepted"}) , 200
    
    except ValueError as e:
        return jsonify({"message" : "demand denied"}), 422
    

