class AccountsRegistry:
    def __init__(self):
        # Tutaj trzymamy konta (zamiast w bazie danych)
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

    def get_account_by_pesel(self, pesel):
        # Przeszukaj listę, żeby znaleźć konto z danym peselem
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None

    def get_accounts_count(self):
        return len(self.accounts)