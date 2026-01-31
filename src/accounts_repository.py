from pymongo import MongoClient
import os
from src.account import Account, BusinessAccount

class MongoAccountsRepository:
    def __init__(self):
        host = os.environ.get("MONGO_HOST", "localhost")
        self._client = MongoClient(f"mongodb://{host}:27017/")
        self._db = self._client["bank_app"]
        self._collection = self._db["accounts"]

    def save_all(self, accounts):
        """Czyści kolekcję i zapisuje wszystkie konta."""
        self._collection.delete_many({})
        
        for account in accounts:
            account_data = account.to_dict()
            self._collection.insert_one(account_data)

    def load_all(self):
        """Pobiera wszystkie konta z bazy i zwraca listę obiektów."""
        accounts_data = self._collection.find()
        loaded_accounts = []

        for data in accounts_data:
            if data.get("type") == "business":
                acc = BusinessAccount(data["company_name"], data["nip"])
                acc.balance = data["balance"]
                acc.history = data["history"]
                loaded_accounts.append(acc)
            else:
                acc = Account(data["first_name"], data["last_name"], data["pesel"])
                acc.balance = data["balance"]
                acc.history = data["history"]
                loaded_accounts.append(acc)
        
        return loaded_accounts
    
    def clear_db(self):
        """Metoda pomocnicza do testów"""
        self._collection.delete_many({})