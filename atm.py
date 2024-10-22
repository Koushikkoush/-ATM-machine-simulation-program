import random
import string
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class ATM:
    def __init__(self, balance=0):
        self.balance = balance
        self.pin = self.generate_pin()

    def generate_pin(self):
        """Generates a random 4-digit PIN."""
        return ''.join(random.choices(string.digits, k=4))

    def authenticate(self, user_pin):
        """Authenticates the user based on their PIN."""
        return user_pin == self.pin

    def deposit(self, amount, user_pin):
        """Deposits the specified amount into the account after authentication."""
        if self.authenticate(user_pin):
            if amount > 0:
                self.balance += amount
                return f"Deposited {amount}. New balance: {self.balance}"
            else:
                return "Invalid deposit amount."
        else:
            return "Invalid PIN."

    def withdraw(self, amount, user_pin):
        """Withdraws the specified amount from the account after authentication."""
        if self.authenticate(user_pin):
            if amount > 0 and amount <= self.balance:
                self.balance -= amount
                return f"Withdrew {amount}. New balance: {self.balance}"
            else:
                return "Insufficient funds or invalid withdrawal amount."
        else:
            return "Invalid PIN."

    def check_balance(self, user_pin):
        """Checks the current account balance after authentication."""
        if self.authenticate(user_pin):
            return f"Your current balance is: {self.balance}"
        else:
            return "Invalid PIN."

    def change_pin(self, old_pin, new_pin):
        """Changes the user's PIN after authenticating with the old PIN."""
        if self.authenticate(old_pin):
            self.pin = new_pin
            return "PIN changed successfully."
        else:
            return "Incorrect old PIN."

class ATMInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Interface")
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Initialize ATM object
        self.atm = ATM()
        self.status_var = tk.StringVar()
        self.status_var.set("Your initial PIN is: " + self.atm.pin)

        self.create_widgets()

    def create_widgets(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # PIN Entry Section
        ttk.Label(main_frame, text="Enter PIN:", font=("Arial", 12)).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.pin_entry = ttk.Entry(main_frame, show="*", width=15)
        self.pin_entry.grid(row=0, column=1, pady=10)

        # Amount Entry Section
        ttk.Label(main_frame, text="Amount (Deposit/Withdraw):", font=("Arial", 12)).grid(row=1, column=0, sticky=tk.W, pady=10)
        self.amount_entry = ttk.Entry(main_frame, width=15)
        self.amount_entry.grid(row=1, column=1, pady=10)

        # Action Buttons
        button_frame = ttk.Frame(main_frame, padding="10 10 10 10")
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Deposit", command=self.deposit_action).grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(button_frame, text="Withdraw", command=self.withdraw_action).grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(button_frame, text="Check Balance", command=self.check_balance_action).grid(row=1, column=0, padx=10, pady=5)
        ttk.Button(button_frame, text="Change PIN", command=self.change_pin_action).grid(row=1, column=1, padx=10, pady=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).grid(row=2, column=0, columnspan=2, pady=10)

        # Status Bar
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, anchor="w", relief=tk.SUNKEN, padding=5)
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))

    def deposit_action(self):
        pin = self.pin_entry.get()
        amount = self.amount_entry.get()
        if amount.isdigit():
            result = self.atm.deposit(float(amount), pin)
        else:
            result = "Please enter a valid amount."
        self.update_status(result)

    def withdraw_action(self):
        pin = self.pin_entry.get()
        amount = self.amount_entry.get()
        if amount.isdigit():
            result = self.atm.withdraw(float(amount), pin)
        else:
            result = "Please enter a valid amount."
        self.update_status(result)

    def check_balance_action(self):
        pin = self.pin_entry.get()
        result = self.atm.check_balance(pin)
        self.update_status(result)

    def change_pin_action(self):
        old_pin = self.pin_entry.get()
        new_pin = simpledialog.askstring("New PIN", "Enter new PIN:", show="*")
        if new_pin and new_pin.isdigit() and len(new_pin) == 4:
            result = self.atm.change_pin(old_pin, new_pin)
        else:
            result = "Please enter a valid 4-digit PIN."
        self.update_status(result)

    def update_status(self, message):
        self.status_var.set(message)

def main():
    root = tk.Tk()
    atm_interface = ATMInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
