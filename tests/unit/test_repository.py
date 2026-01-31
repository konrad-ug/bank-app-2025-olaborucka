import unittest
from unittest.mock import MagicMock, patch
from src.account import Account
from src.accounts_repository import MongoAccountsRepository
from src.account import BusinessAccount

class TestMongoRepository(unittest.TestCase):
    
    def setUp(self):
        self.account1 = Account("Jan", "Kowalski", "12345678901")
        self.account1.balance = 100
        self.account1.history = [100]

    @patch("src.accounts_repository.MongoClient")
    def test_save_all(self, mock_client):
        mock_db = mock_client.return_value["bank_app"]
        mock_collection = mock_db["accounts"]
        
        repo = MongoAccountsRepository()
        repo.save_all([self.account1])
        mock_collection.delete_many.assert_called_with({})
        
        mock_collection.insert_one.assert_called()
        
        args, _ = mock_collection.insert_one.call_args
        inserted_data = args[0]
        self.assertEqual(inserted_data["pesel"], "12345678901")
        self.assertEqual(inserted_data["balance"], 100)

    @patch("src.accounts_repository.MongoClient")
    def test_load_all(self, mock_client):
        mock_db = mock_client.return_value["bank_app"]
        mock_collection = mock_db["accounts"]
        
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
        

        accounts = repo.load_all()

        self.assertEqual(len(accounts), 1)
        self.assertIsInstance(accounts[0], Account)
        self.assertEqual(accounts[0].balance, 200)
        self.assertEqual(accounts[0].pesel, "12345678901")

    @patch("src.accounts_repository.MongoClient")
    def test_load_all_with_business(self, mock_client):
        mock_db = mock_client.return_value["bank_app"]
        mock_collection = mock_db["accounts"]
        
        mock_collection.find.return_value = [
            {
                "first_name": "Jan", "last_name": "Kowalski", "pesel": "12345678901",
                "balance": 200, "history": [], "type": "personal"
            },
            {
                "company_name": "Firma X", "nip": "1234567890", "pesel": "00000000000",
                "balance": 1000, "history": [], "type": "business"
            }
        ]
        
        repo = MongoAccountsRepository()
        accounts = repo.load_all()
        
        assert len(accounts) == 2
        assert isinstance(accounts[1], BusinessAccount)
        assert accounts[1].company_name == "Firma X"

    @patch("src.accounts_repository.MongoClient")
    def test_load_all_with_business(self, mock_client):
        mock_db = mock_client.return_value["bank_app"]
        mock_collection = mock_db["accounts"]
        
        mock_collection.find.return_value = [
            {
                "first_name": "Jan", "last_name": "Kowalski", "pesel": "12345678901",
                "balance": 200, "history": [], "type": "personal"
            },
            {
                "company_name": "Firma X", "nip": "1234567890", "pesel": "00000000000",
                "balance": 1000, "history": [], "type": "business"
            }
        ]
        
        repo = MongoAccountsRepository()
        with patch("src.account.BusinessAccount.verify_nip_with_gov", return_value=True):
            accounts = repo.load_all()
        
        assert len(accounts) == 2
        assert isinstance(accounts[1], BusinessAccount)
        assert accounts[1].company_name == "Firma X"

    @patch("src.accounts_repository.MongoClient")
    def test_clear_db(self, mock_client):
        mock_db = mock_client.return_value["bank_app"]
        mock_collection = mock_db["accounts"]
        repo = MongoAccountsRepository()
        repo.clear_db()
        mock_collection.delete_many.assert_called_once_with({})