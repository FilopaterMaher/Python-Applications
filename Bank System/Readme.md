# **Bank Management System**

This project is a simple **banking system** that manages customer accounts, transactions, and bank branches using **OOP principles and SOLID design patterns**.

---

## **Project Structure**
The system is designed with **SOLID principles** to ensure **scalability, maintainability, and clean architecture**.

### **Applied SOLID Principles & Design Patterns**

### 1️⃣ **Single Responsibility Principle (SRP)**
- Initially, the `BankSystem` class handled **both account management and transaction logging**.
- Now, we have **separate classes** for each responsibility:
  - `AccountManager`: Manages customer accounts (creating, depositing, withdrawing).
  - `TransactionManager`: Logs transactions without modifying account logic.

✅ **Why?** This ensures that each class has **only one reason to change**, improving modularity.

---

### 2️⃣ **Open/Closed Principle (OCP)**
- The `Transaction` class is an **abstract base class**, and transaction types (`Deposit`, `Withdrawal`, `OpenAccount`) **inherit from it**.
- New transaction types (e.g., **Transfer, LoanPayment**) can be added **without modifying existing code**.

✅ **Why?** The system is **open for extension but closed for modification**, making future updates safer.

---

### 3️⃣ **Liskov Substitution Principle (LSP)**
- All transactions (`Deposit`, `Withdrawal`, `OpenAccount`) **correctly extend** the `Transaction` class **without altering behavior**.
- The `get_transaction_description()` method behaves **consistently** across all transaction types.

✅ **Why?** This ensures that **substituting any subclass does not break the program**, making the system robust.

---

### 4️⃣ **Interface Segregation Principle (ISP)**
- Instead of forcing one interface to do everything, we split it into **specialized interfaces**:
  - `ITransaction`: Defines the interface for transactions.
  - `IAccountManager`: Defines account operations.
- `BankBranch` only depends on what it actually needs.

✅ **Why?** This prevents **forcing classes to implement unnecessary methods**, making the code **clean and focused**.

---

### 5️⃣ **Dependency Inversion Principle (DIP)**
- `BankBranch` depends on **abstractions (`IAccountManager`, `TransactionManager`)** instead of concrete classes like `BankSystem`.
- This allows us to swap implementations easily **without breaking the system**.

✅ **Why?** This makes the code **loosely coupled**, so components can evolve independently.

---
