from abc import ABC, abstractmethod
import random

# --- Interface Segregation & Dependency Inversion ---
class ITransaction(ABC):
    @abstractmethod
    def get_transaction_description(self):
        pass

class IAccountManager(ABC):
    @abstractmethod
    def open_account(self, customer_name, teller_id):
        pass
    
    @abstractmethod
    def get_account(self, customer_id):
        pass

    @abstractmethod
    def deposit(self, customer_id, amount):
        pass
    
    @abstractmethod
    def withdraw(self, customer_id, amount):
        pass

# --- Single Responsibility: Transactions ---
class Transaction(ITransaction, ABC):
    def __init__(self, customer_id, teller_id):
        self._customer_id = customer_id
        self._teller_id = teller_id

    def get_customer_id(self):
        return self._customer_id

    def get_teller_id(self):
        return self._teller_id

class Deposit(Transaction):
    def __init__(self, customer_id, teller_id, amount):
        super().__init__(customer_id, teller_id)
        self._amount = amount

    def get_transaction_description(self):
        return f'Teller {self.get_teller_id()} deposited {self._amount} to account {self.get_customer_id()}'

class Withdrawal(Transaction):
    def __init__(self, customer_id, teller_id, amount):
        super().__init__(customer_id, teller_id)
        self._amount = amount

    def get_transaction_description(self):
        return f'Teller {self.get_teller_id()} withdrew {self._amount} from account {self.get_customer_id()}'

class OpenAccount(Transaction):
    def get_transaction_description(self):
        return f'Teller {self.get_teller_id()} opened account {self.get_customer_id()}'

# --- Single Responsibility: Bank Account ---
class BankAccount:
    def __init__(self, customer_id, name, balance=0):
        self._customer_id = customer_id
        self._name = name
        self._balance = balance

    def get_balance(self):
        return self._balance

    def deposit(self, amount):
        self._balance += amount

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount

# --- Single Responsibility: Account Manager ---
class AccountManager(IAccountManager):
    def __init__(self):
        self._accounts = []
    
    def open_account(self, customer_name, teller_id):
        customer_id = len(self._accounts)
        account = BankAccount(customer_id, customer_name)
        self._accounts.append(account)
        return OpenAccount(customer_id, teller_id)
    
    def get_account(self, customer_id):
        return self._accounts[customer_id]

    def deposit(self, customer_id, amount):
        self.get_account(customer_id).deposit(amount)

    def withdraw(self, customer_id, amount):
        self.get_account(customer_id).withdraw(amount)

# --- Single Responsibility: Transaction Manager ---
class TransactionManager:
    def __init__(self):
        self._transactions = []
    
    def log_transaction(self, transaction):
        self._transactions.append(transaction)
    
    def print_transactions(self):
        for transaction in self._transactions:
            print(transaction.get_transaction_description())

# --- Bank Teller ---
class BankTeller:
    def __init__(self, teller_id):
        self._id = teller_id

    def get_id(self):
        return self._id

# --- Open/Closed Principle: Bank Branch ---
class BankBranch:
    def __init__(self, address, cash_on_hand, account_manager, transaction_manager):
        self._address = address
        self._cash_on_hand = cash_on_hand
        self._account_manager = account_manager
        self._transaction_manager = transaction_manager
        self._tellers = []

    def add_teller(self, teller):
        self._tellers.append(teller)
    
    def _get_available_teller(self):
        return random.choice(self._tellers).get_id()

    def open_account(self, customer_name):
        teller_id = self._get_available_teller()
        transaction = self._account_manager.open_account(customer_name, teller_id)
        self._transaction_manager.log_transaction(transaction)
        return transaction.get_customer_id()
    
    def deposit(self, customer_id, amount):
        teller_id = self._get_available_teller()
        self._account_manager.deposit(customer_id, amount)
        self._transaction_manager.log_transaction(Deposit(customer_id, teller_id, amount))

    def withdraw(self, customer_id, amount):
        if amount > self._cash_on_hand:
            raise ValueError('Branch does not have enough cash')
        teller_id = self._get_available_teller()
        self._account_manager.withdraw(customer_id, amount)
        self._cash_on_hand -= amount
        self._transaction_manager.log_transaction(Withdrawal(customer_id, teller_id, amount))

# --- Bank (High-Level Module) ---
class Bank:
    def __init__(self):
        self._branches = []
        self._account_manager = AccountManager()
        self._transaction_manager = TransactionManager()

    def add_branch(self, address, initial_funds):
        branch = BankBranch(address, initial_funds, self._account_manager, self._transaction_manager)
        self._branches.append(branch)
        return branch
    
    def print_transactions(self):
        self._transaction_manager.print_transactions()

# --- Usage ---
bank = Bank()
branch1 = bank.add_branch("123 Main St", 1000)
branch2 = bank.add_branch("456 Elm St", 1000)

branch1.add_teller(BankTeller(1))
branch1.add_teller(BankTeller(2))
branch2.add_teller(BankTeller(3))
branch2.add_teller(BankTeller(4))

customer_id1 = branch1.open_account("John Doe")
customer_id2 = branch1.open_account("Bob Smith")
customer_id3 = branch2.open_account("Jane Doe")

branch1.deposit(customer_id1, 100)
branch1.deposit(customer_id2, 200)
branch2.deposit(customer_id3, 300)

branch1.withdraw(customer_id1, 50)

bank.print_transactions()