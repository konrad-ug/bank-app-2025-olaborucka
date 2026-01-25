import unittest
from unittest.mock import MagicMock, patch
from src.account import Account
from src.accounts_repository import MongoAccountsRepository

class TestMongoRepository(unittest.TestCase):
    
    def setUp(self):
        self.account1 = Account("Jan", "Kowalski", "12345678901")
        self.account1.balance = 100
        self.account1.history = [100]

    @patch("src.accounts_repository.MongoClient")
    def test_save_all(self, mock_client):
        # Konfiguracja Mocka
        mock_db = mock_client.return_value["bank_app"]
        mock_collection = mock_db["accounts"]
        
        repo = MongoAccountsRepository()
        
        # Action
        repo.save_all([self.account1])
        
        # Assert
        # Sprawdzamy czy wyczyszczono kolekcję
        mock_collection.delete_many.assert_called_with({})
        # Sprawdzamy czy wstawiono dane
        mock_collection.insert_one.assert_called()
        
        # Sprawdzamy co dokładnie zostało wstawione
        args, _ = mock_collection.insert_one.call_args
        inserted_data = args[0]
        self.assertEqual(inserted_data["pesel"], "12345678901")
        self.assertEqual(inserted_data["balance"], 100)

    @patch("src.accounts_repository.MongoClient")
    def test_load_all(self, mock_client):
        # Konfiguracja Mocka - symulujemy dane w bazie
        mock_db = mock_client.return_value["bank_app"]
        mock_collection = mock_db["accounts"]
        
        # find() zwraca listę słowników
        mock_collection.find.return_value = [
            {
                "first_name": "Jan",
                "last_name": "Kowalski",
                "pesel": "12345678901",
                "balance": 200,
                "history": [100, 100],
                "type": "personal"
            }
        ]
        
        repo = MongoAccountsRepository()
        
        # Action
        accounts = repo.load_all()
        
        # Assert
        self.assertEqual(len(accounts), 1)
        self.assertIsInstance(accounts[0], Account)
        self.assertEqual(accounts[0].balance, 200)
        self.assertEqual(accounts[0].pesel, "12345678901")