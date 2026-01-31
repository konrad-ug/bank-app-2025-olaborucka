from src.account import Account, BusinessAccount
from unittest.mock import patch
from datetime import date

class TestMail:
    def test_email_personal_account(self):
        """Sprawdza wysłanie maila dla konta osobistego."""
        acc = Account("Jan", "Kowalski", "12345678901")
        acc.deposit(100)
        acc.withdraw(50)
        
        with patch('src.account.SMTPClient') as MockSMTP:
            mock_instance = MockSMTP.return_value
            mock_instance.send.return_value = True 

            result = acc.send_history_via_email("test@example.com")

            assert result is True

            mock_instance.send.assert_called_once()
            
            args, _ = mock_instance.send.call_args
            subject, message, email = args
            
            today = date.today().strftime("%Y-%m-%d")
            assert subject == f"Account Transfer History {today}"
            assert message == "Personal account history: [100, -50]"
            assert email == "test@example.com"

    def test_email_business_account(self):
        """Sprawdza wysłanie maila dla konta firmowego (inny komunikat)."""
        with patch.object(BusinessAccount, 'verify_nip_with_gov', return_value=True):
            acc = BusinessAccount("Firma", "1234567890")
            acc.deposit(1000)

            with patch('src.account.SMTPClient') as MockSMTP:
                mock_instance = MockSMTP.return_value
                mock_instance.send.return_value = True

                result = acc.send_history_via_email("ceo@firma.com")

                assert result is True
                
                args, _ = mock_instance.send.call_args
                _, message, _ = args
                assert message == "Company account history: [1000]"

    def test_email_fail(self):
        """Sprawdza scenariusz, gdy wysyłka się nie uda (zwróci False)."""
        acc = Account("Jan", "Nowak", "12345678901")
        
        with patch('src.account.SMTPClient') as MockSMTP:
            mock_instance = MockSMTP.return_value
            mock_instance.send.return_value = False 

            result = acc.send_history_via_email("wrong@mail.com")
            
            assert result is False
    
    def test_smtp_client_real_send_returns_false(self):
        from src.smtp_client import SMTPClient
        client = SMTPClient()
        assert client.send("Subject", "Message", "test@test.pl") is False