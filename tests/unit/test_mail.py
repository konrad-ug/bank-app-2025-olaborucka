from src.account import Account, BusinessAccount
from unittest.mock import patch
from datetime import date

class TestMail:
    def test_email_personal_account(self):
        """Sprawdza wysłanie maila dla konta osobistego."""
        acc = Account("Jan", "Kowalski", "12345678901")
        acc.deposit(100)
        acc.withdraw(50)
        
        # Mockujemy SMTPClient wewnątrz modułu src.account
        with patch('src.account.SMTPClient') as MockSMTP:
            # Konfigurujemy mocka instancji
            mock_instance = MockSMTP.return_value
            mock_instance.send.return_value = True  # Symulujemy sukces wysyłki

            # Action
            result = acc.send_history_via_email("test@example.com")

            # Assert
            assert result is True
            
            # Sprawdzamy czy metoda send została wywołana
            mock_instance.send.assert_called_once()
            
            # Sprawdzamy argumenty wywołania (temat i treść)
            args, _ = mock_instance.send.call_args
            subject, message, email = args
            
            today = date.today().strftime("%Y-%m-%d")
            assert subject == f"Account Transfer History {today}"
            assert message == "Personal account history: [100, -50]"
            assert email == "test@example.com"

    def test_email_business_account(self):
        """Sprawdza wysłanie maila dla konta firmowego (inny komunikat)."""
        # Musimy zmockować NIP, żeby stworzyć firmę
        with patch.object(BusinessAccount, 'verify_nip_with_gov', return_value=True):
            acc = BusinessAccount("Firma", "1234567890")
            acc.deposit(1000)
            
            # Mockujemy SMTPClient
            with patch('src.account.SMTPClient') as MockSMTP:
                mock_instance = MockSMTP.return_value
                mock_instance.send.return_value = True

                result = acc.send_history_via_email("ceo@firma.com")

                assert result is True
                
                # Sprawdzamy treść dla firmy
                args, _ = mock_instance.send.call_args
                _, message, _ = args
                assert message == "Company account history: [1000]"

    def test_email_fail(self):
        """Sprawdza scenariusz, gdy wysyłka się nie uda (zwróci False)."""
        acc = Account("Jan", "Nowak", "12345678901")
        
        with patch('src.account.SMTPClient') as MockSMTP:
            mock_instance = MockSMTP.return_value
            mock_instance.send.return_value = False  # Symulujemy błąd serwera

            result = acc.send_history_via_email("wrong@mail.com")
            
            assert result is False