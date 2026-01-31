class AccountsRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

    def get_account_by_pesel(self, pesel):
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None

    def get_accounts_count(self):
        return len(self.accounts)
    
    def delete_account(self, pesel):
        for account in self.accounts:
            if account.pesel == pesel:
                self.accounts.remove(account)
                return True
        return False

    def get_all_accounts(self):
        return self.accounts
    def clear(self):
        self.accounts = []