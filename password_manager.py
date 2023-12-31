from cryptography.fernet import Fernet
import json
import os

class PasswordManager:
    def __init__(self, key_file="key.key", data_file="passwords.json"):
        self.key_file = key_file
        self.data_file = data_file
        self.load_key()
        self.load_data()

    def load_key(self):
        # Load or generate a key for encryption
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as key_file:
                self.key = key_file.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_file, "wb") as key_file:
                key_file.write(self.key)

        self.cipher = Fernet(self.key)

    def load_data(self):
        # Load existing password data or create an empty dictionary
        if os.path.exists(self.data_file):
            with open(self.data_file, "rb") as data_file:
                encrypted_data = data_file.read()
                decrypted_data = self.cipher.decrypt(encrypted_data)
                self.passwords = json.loads(decrypted_data)
        else:
            self.passwords = {}

    def save_data(self):
        # Save password data after encrypting it
        encrypted_data = self.cipher.encrypt(json.dumps(self.passwords).encode())
        with open(self.data_file, "wb") as data_file:
            data_file.write(encrypted_data)

    def add_password(self, account, password):
        # Add a new password
        self.passwords[account] = password
        self.save_data()
        print(f"Password for {account} added successfully.")

    def get_password(self, account):
        # Retrieve a password
        if account in self.passwords:
            return self.passwords[account]
        else:
            print(f"No password found for {account}.")

    def list_accounts(self):
        # List all stored accounts
        print("Stored Accounts:")
        for account in self.passwords:
            print(account)

if __name__ == "__main__":
    password_manager = PasswordManager()

    while True:
        print("\nPassword Manager Menu:")
        print("1. Add New Password")
        print("2. Get Password")
        print("3. List Accounts")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            account = input("Enter the account name: ")
            password = input("Enter the password: ")
            password_manager.add_password(account, password)
        elif choice == "2":
            account = input("Enter the account name: ")
            stored_password = password_manager.get_password(account)
            if stored_password:
                print(f"Password for {account}: {stored_password}")
        elif choice == "3":
            password_manager.list_accounts()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")
