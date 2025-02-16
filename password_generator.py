import random
import string
import os
import tkinter as tk
from tkinter import filedialog
import pyperclip  # Clipboard functionality
from typing import Optional

# Constants
MIN_PASSWORD_LENGTH = 6
MIN_NUM_PASSWORDS = 1

def generate_password(length: int = 12, use_digits: bool = True, use_special_chars: bool = True, use_uppercase: bool = True, use_lowercase: bool = True) -> Optional[str]:
    """Generates a secure password with given parameters."""
    characters = (
        (string.ascii_lowercase if use_lowercase else "") +
        (string.ascii_uppercase if use_uppercase else "") +
        (string.digits if use_digits else "") +
        (string.punctuation if use_special_chars else "")
    )

    if not characters:
        print("❌ You must select at least one character type!")
        return None

    return ''.join(random.choice(characters) for _ in range(length))

def rate_password(password: str) -> str:
    """Rates password strength based on length and character variety."""
    if not password:
        return "❌ Invalid Password"

    length_score = len(password)
    variety_score = sum([
        any(c.islower() for c in password),  # Lowercase
        any(c.isupper() for c in password),  # Uppercase
        any(c.isdigit() for c in password),  # Numbers
        any(c in string.punctuation for c in password)  # Special characters
    ])

    # Determine strength level
    if length_score < 8 or variety_score < 2:
        return "🔴 Weak"
    elif length_score < 12 or variety_score < 3:
        return "🟡 Moderate"
    elif length_score < 16 or variety_score < 4:
        return "🟢 Strong"
    else:
        return "🔥 Very Strong"

def get_valid_number(prompt: str, min_value: int = 1) -> int:
    """Ensures the user enters a valid number."""
    while True:
        try:
            value = int(input(prompt))
            if value >= min_value:
                return value
            print(f"❌ Number must be at least {min_value}. Try again.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

def get_yes_no(prompt: str) -> bool:
    """Asks the user a yes/no question and ensures valid input."""
    while True:
        choice = input(prompt + " (y/n): ").strip().lower()
        if choice in ('y', 'n'):
            return choice == 'y'  # Returns True for 'y', False for 'n'
        print("❌ Invalid input. Please enter 'y' for yes or 'n' for no.")

def choose_save_location() -> str:
    """Opens a file dialog so the user can choose where to save the password file."""
    root = tk.Tk()
    root.withdraw()  # Hide the Tkinter root window

    file_path = filedialog.asksaveasfilename(
        title="Save Password File",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    return file_path  # Returns the full path the user chose

def copy_to_clipboard(passwords: list[str]) -> None:
    """Handles copying passwords to the clipboard."""
    if get_yes_no("\nDo you want to copy a password to the clipboard?"):
        while True:
            print("\nEnter the number of the password to copy (or type 'all' to copy all passwords).")
            choice = input("Your choice: ").strip().lower()

            if choice == "all":
                pyperclip.copy("\n".join(passwords))
                print("📋 All passwords copied to clipboard!")
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(passwords):
                pyperclip.copy(passwords[int(choice) - 1])
                print(f"📋 Password {choice} copied to clipboard!")
                break
            else:
                print("❌ Invalid choice. Please enter a valid number or 'all'.")

def save_to_file(passwords: list[str]) -> None:
    """Handles saving passwords to a file."""
    if get_yes_no("\nDo you want to save the passwords to a file?"):
        file_path = choose_save_location()  # Let the user pick a save location
        if file_path:  # If user selected a file
            with open(file_path, "a") as file:
                for password in passwords:
                    file.write(f"{password}  ➝  {rate_password(password)}\n")
            print(f"💾 Passwords saved to: **{file_path}**")
        else:
            print("❌ No file selected. Passwords not saved.")

def run_password_generator() -> None:
    """Main function to generate multiple passwords."""
    print("🔐 Secure Password Generator 🔐")

    while True:
        # Get user preferences
        num_passwords = get_valid_number("How many passwords do you want to generate? ", min_value=MIN_NUM_PASSWORDS)
        length = get_valid_number("Enter password length (min. 6 characters): ", min_value=MIN_PASSWORD_LENGTH)
        use_lowercase = get_yes_no("Include lowercase letters?")
        use_uppercase = get_yes_no("Include uppercase letters?")
        use_digits = get_yes_no("Include numbers?")
        use_special_chars = get_yes_no("Include special characters?")

        # Generate passwords
        passwords = [generate_password(length, use_digits, use_special_chars, use_uppercase, use_lowercase) for _ in range(num_passwords)]

        # Display generated passwords
        print("\n✅ Generated Passwords:")
        for i, password in enumerate(passwords, 1):
            strength = rate_password(password)
            print(f"{i}. {password}  ➝  {strength}")

        # Copy to clipboard
        copy_to_clipboard(passwords)

        # Save to file if user wants
        save_to_file(passwords)

        # Ask if they want another batch of passwords, otherwise exit
        if not get_yes_no("\nGenerate another batch of passwords?"):
            print("\n👋 Goodbye! Thanks for using the Secure Password Generator.")
            break

# Improved entry point
if __name__ == "__main__":
    try:
        run_password_generator()
    except KeyboardInterrupt:
        print("\n❌ Process interrupted. Exiting safely. 👋")
