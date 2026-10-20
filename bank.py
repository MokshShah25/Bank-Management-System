"""
Bank Management System
An improvised, robust, and user-friendly banking console application.
"""

import json
import os
import random
import re
import string
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class Bank:
    """Manages bank accounts, transactions, and persistent JSON storage."""

    def __init__(self, database_path: str = "data.json") -> None:
        self.database_path = Path(database_path)
        self.data: List[Dict[str, Any]] = self._load_data()

    def _load_data(self) -> List[Dict[str, Any]]:
        """Safely loads account data from the JSON database file.
        
        Handles missing files, empty files (0 bytes), and corrupted JSON gracefully.
        """
        if not self.database_path.exists():
            self._save_initial_data([])
            return []

        try:
            # Check if file is empty
            if self.database_path.stat().st_size == 0:
                self._save_initial_data([])
                return []

            with open(self.database_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    self._save_initial_data([])
                    return []
                return json.loads(content)
        except (json.JSONDecodeError, OSError) as error:
            print(f"[!] Warning: Could not parse database file ({error}). Initializing empty database.")
            self._save_initial_data([])
            return []

    def _save_initial_data(self, initial_data: List[Dict[str, Any]]) -> None:
        """Helper to safely write initial data."""
        try:
            with open(self.database_path, "w", encoding="utf-8") as file:
                json.dump(initial_data, file, indent=4)
        except OSError as error:
            print(f"[!] Error creating database file: {error}")

    def _save_data(self) -> bool:
        """Saves current data to JSON file with indentation for readability."""
        try:
            with open(self.database_path, "w", encoding="utf-8") as file:
                json.dump(self.data, file, indent=4)
            return True
        except OSError as error:
            print(f"[!] Database write error: {error}")
            return False

    def _find_account(self, account_no: str) -> Optional[Dict[str, Any]]:
        """Finds an account by account number."""
        for account in self.data:
            if account.get("accountNo.") == account_no.strip():
                return account
        return None

    def _authenticate(self, account_no: str, pin: str) -> Optional[Dict[str, Any]]:
        """Authenticates user credentials against the database."""
        account = self._find_account(account_no)
        if not account:
            return None
        # PIN comparison supports both str and int for backward compatibility
        if str(account.get("pin")) == pin.strip():
            return account
        return None

    def _generate_unique_account_no(self) -> str:
        """Generates a unique 7-character account identifier."""
        existing_accs = {acc.get("accountNo.") for acc in self.data}
        while True:
            alpha = random.choices(string.ascii_uppercase, k=3)
            digits = random.choices(string.digits, k=3)
            special = random.choices(["@", "*", "!"], k=1)
            chars = alpha + digits + special
            random.shuffle(chars)
            account_no = "".join(chars)
            if account_no not in existing_accs:
                return account_no

    @staticmethod
    def _prompt_non_empty(prompt_text: str) -> str:
        """Prompts user until a non-empty string is provided."""
        while True:
            val = input(prompt_text).strip()
            if val:
                return val
            print("Input cannot be empty. Please try again.")

    @staticmethod
    def _prompt_pin(prompt_text: str = "Enter 4-digit PIN: ") -> str:
        """Validates that PIN is exactly 4 numeric digits."""
        while True:
            pin = input(prompt_text).strip()
            if len(pin) == 4 and pin.isdigit():
                return pin
            print("Invalid PIN! PIN must be exactly 4 numeric digits (e.g., 1234).")

    @staticmethod
    def _prompt_email(prompt_text: str = "Enter email address: ") -> str:
        """Validates email format."""
        email_pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$")
        while True:
            email = input(prompt_text).strip()
            if email_pattern.match(email):
                return email
            print("Invalid email format (e.g., user@example.com). Please try again.")

    @staticmethod
    def _prompt_float(prompt_text: str, min_val: float = 0.01, max_val: Optional[float] = None) -> float:
        """Prompts user for a positive float value with optional bounds."""
        while True:
            user_input = input(prompt_text).strip()
            try:
                val = float(user_input)
                if val < min_val:
                    print(f"Amount must be at least {min_val:,.2f}.")
                    continue
                if max_val is not None and val > max_val:
                    print(f"Amount cannot exceed {max_val:,.2f}.")
                    continue
                return round(val, 2)
            except ValueError:
                print("Invalid number format. Please enter a valid numerical amount.")

    def _log_transaction(self, account: Dict[str, Any], trans_type: str, amount: float) -> None:
        """Logs a transaction record in the account history."""
        if "transactions" not in account or not isinstance(account["transactions"], list):
            account["transactions"] = []

        record = {
            "type": trans_type,
            "amount": amount,
            "balance": round(account["balance"], 2),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        account["transactions"].append(record)

    # ------------------ Public Banking Actions ------------------

    def create_account(self) -> None:
        """Handles new bank account creation with validation."""
        print("\n--- CREATE ACCOUNT ---")
        name = self._prompt_non_empty("Enter name: ")

        # Validate Age
        while True:
            age_str = input("Enter age: ").strip()
            if not age_str.isdigit():
                print("Age must be a valid integer.")
                continue
            age = int(age_str)
            if age < 0 or age > 130:
                print("Please enter a realistic age.")
                continue
            if age < 18:
                print("\n[!] Sorry, you must be at least 18 years old to open an account.")
                return
            break

        email = self._prompt_email("Enter email address: ")
        pin = self._prompt_pin("Create a 4-digit PIN: ")
        account_no = self._generate_unique_account_no()

        # Optional initial deposit
        initial_deposit = 0.0
        deposit_choice = input("Would you like to make an initial deposit? (y/n): ").strip().lower()
        if deposit_choice in ["y", "yes"]:
            initial_deposit = self._prompt_float("Enter initial deposit amount: ", min_val=1.0, max_val=100000.0)

        new_account: Dict[str, Any] = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "accountNo.": account_no,
            "balance": initial_deposit,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "transactions": []
        }

        if initial_deposit > 0:
            self._log_transaction(new_account, "INITIAL DEPOSIT", initial_deposit)

        self.data.append(new_account)
        if self._save_data():
            print("\n" + "=" * 40)
            print("Account created successfully!")
            print(f"Account Holder : {name}")
            print(f"Account Number : {account_no}")
            print(f"Opening Balance: {initial_deposit:,.2f}")
            print("=" * 40)
            print("Please keep your account number and PIN confidential.\n")

    def deposit(self) -> None:
        """Deposits funds into an authenticated account."""
        print("\n--- DEPOSIT MONEY ---")
        account_no = input("Account number: ").strip()
        pin = input("PIN: ").strip()

        account = self._authenticate(account_no, pin)
        if not account:
            print("[!] Invalid account number or PIN.")
            return

        max_deposit_limit = 100000.0
        amount = self._prompt_float(
            f"Enter amount to deposit (Max {max_deposit_limit:,.2f}): ",
            min_val=1.0,
            max_val=max_deposit_limit
        )

        account["balance"] = round(account["balance"] + amount, 2)
        self._log_transaction(account, "DEPOSIT", amount)
        self._save_data()

        print("\n[+] Amount deposited successfully!")
        print(f"Deposited Amount: {amount:,.2f}")
        print(f"Current Balance : {account['balance']:,.2f}\n")

    def withdraw(self) -> None:
        """Withdraws funds from an authenticated account if balance permits."""
        print("\n--- WITHDRAW MONEY ---")
        account_no = input("Account number: ").strip()
        pin = input("PIN: ").strip()

        account = self._authenticate(account_no, pin)
        if not account:
            print("[!] Invalid account number or PIN.")
            return

        current_balance = account["balance"]
        if current_balance <= 0:
            print(f"[!] Insufficient funds. Current balance is 0.00.")
            return

        amount = self._prompt_float(
            f"Enter amount to withdraw (Available: {current_balance:,.2f}): ",
            min_val=1.0
        )

        if amount > current_balance:
            print(f"[!] Insufficient balance! Your available balance is {current_balance:,.2f}.")
            return

        account["balance"] = round(account["balance"] - amount, 2)
        self._log_transaction(account, "WITHDRAWAL", amount)
        self._save_data()

        print("\n[+] Amount withdrawn successfully!")
        print(f"Withdrawn Amount: {amount:,.2f}")
        print(f"Remaining Balance: {account['balance']:,.2f}\n")

    def check_details(self) -> None:
        """Displays account details and recent transaction statement."""
        print("\n--- CHECK ACCOUNT DETAILS ---")
        account_no = input("Account number: ").strip()
        pin = input("PIN: ").strip()

        account = self._authenticate(account_no, pin)
        if not account:
            print("[!] Invalid account number or PIN.")
            return

        print("\n" + "=" * 45)
        print("            ACCOUNT DETAILS")
        print("=" * 45)
        print(f"Account Number : {account.get('accountNo.')}")
        print(f"Account Holder : {account.get('name')}")
        print(f"Age            : {account.get('age')}")
        print(f"Email          : {account.get('email')}")
        print(f"Total Balance  : {account.get('balance', 0):,.2f}")
        if account.get("created_at"):
            print(f"Opened On      : {account.get('created_at')}")
        print("-" * 45)

        # Recent Transactions
        transactions = account.get("transactions", [])
        if transactions:
            print("Recent Transactions (Last 5):")
            for t in transactions[-5:]:
                print(f" • [{t['timestamp']}] {t['type']:<15} : {t['amount']:>10,.2f} | Bal: {t['balance']:>10,.2f}")
        else:
            print("No transaction history recorded yet.")
        print("=" * 45 + "\n")

    def update_pin(self) -> None:
        """Dedicated method to update an account's PIN securely."""
        print("\n--- UPDATE PIN ---")
        account_no = input("Account number: ").strip()
        current_pin = input("Current PIN: ").strip()

        account = self._authenticate(account_no, current_pin)
        if not account:
            print("[!] Invalid account number or PIN.")
            return

        new_pin = self._prompt_pin("Enter new 4-digit PIN: ")
        if new_pin == current_pin:
            print("[!] New PIN cannot be the same as your current PIN.")
            return

        confirm_pin = input("Confirm new 4-digit PIN: ").strip()
        if new_pin != confirm_pin:
            print("[!] PINs do not match. Update cancelled.")
            return

        account["pin"] = new_pin
        self._save_data()
        print("\n[+] PIN updated successfully!\n")

    def update_email(self) -> None:
        """Dedicated method to update an account's email address."""
        print("\n--- UPDATE EMAIL ---")
        account_no = input("Account number: ").strip()
        pin = input("PIN: ").strip()

        account = self._authenticate(account_no, pin)
        if not account:
            print("[!] Invalid account number or PIN.")
            return

        print(f"Current Email: {account.get('email')}")
        new_email = self._prompt_email("Enter new email address: ")

        if new_email.lower() == account.get("email", "").lower():
            print("[!] New email is the same as current email.")
            return

        account["email"] = new_email
        self._save_data()
        print("\n[+] Email address updated successfully!\n")

    def delete_account(self) -> None:
        """Deletes an account after authenticating and confirming."""
        print("\n--- DELETE ACCOUNT ---")
        account_no = input("Account number: ").strip()
        pin = input("PIN: ").strip()

        account = self._authenticate(account_no, pin)
        if not account:
            print("[!] Invalid account number or PIN.")
            return

        if account.get("balance", 0) > 0:
            print(f"[!] Warning: This account has a remaining balance of {account['balance']:,.2f}.")

        confirm = input("Are you sure you want to permanently delete this account? (yes/no): ").strip().lower()
        if confirm in ["yes", "y"]:
            self.data.remove(account)
            self._save_data()
            print("\n[+] Account deleted successfully.\n")
        else:
            print("Account deletion cancelled.")

    def view_all_accounts_admin(self) -> None:
        """Secure administrative view of all accounts requiring Admin ID and Password."""
        print("\n--- SECURE ADMIN ACCESS ---")
        admin_id = input("Enter Admin ID: ").strip()
        admin_pass = input("Enter Admin Password: ").strip()

        expected_id = os.getenv("BANK_ADMIN_ID", "admin")
        expected_pass = os.getenv("BANK_ADMIN_PASS", "Admin@123")

        if admin_id != expected_id or admin_pass != expected_pass:
            print("[!] Access Denied: Invalid Admin ID or Password.")
            return

        print("\n[+] Admin Authentication Successful.")
        print("=" * 80)
        print(f"{'Acc Number':<12} | {'Holder Name':<20} | {'Email':<26} | {'Balance':>12}")
        print("=" * 80)
        if not self.data:
            print("No registered accounts found in database.")
        else:
            for acc in self.data:
                print(f"{acc.get('accountNo.', 'N/A'):<12} | {acc.get('name', 'N/A'):<20} | {acc.get('email', 'N/A'):<26} | {acc.get('balance', 0.0):>12,.2f}")
        print("=" * 80 + "\n")


def main() -> None:
    """Main application loop with clean menu navigation."""
    bank = Bank()

    menu = """
========== PYTHON BANK ==========

1. Create account
2. Deposit money
3. Withdraw money
4. Check account details
5. Update PIN
6. Update email
7. Delete account
8. View all accounts (Admin)
9. Exit

================================="""

    actions = {
        "1": bank.create_account,
        "2": bank.deposit,
        "3": bank.withdraw,
        "4": bank.check_details,
        "5": bank.update_pin,
        "6": bank.update_email,
        "7": bank.delete_account,
        "8": bank.view_all_accounts_admin,
    }

    while True:
        print(menu)
        choice = input("Enter your choice: ").strip()

        if choice == "9":
            print("\nThank you for using Python Bank. Have a great day!")
            break

        action = actions.get(choice)
        if action:
            try:
                action()
            except KeyboardInterrupt:
                print("\nOperation cancelled by user.")
        else:
            print("\n[!] Invalid choice. Please enter a number between 1 and 9.")


if __name__ == "__main__":
    main()
