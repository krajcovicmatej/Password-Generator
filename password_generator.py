import random
import string
import os
import tkinter as tk
from tkinter import filedialog

def generate_password(length=12, use_digits=True, use_special_chars=True, use_uppercase=True, use_lowercase=True):
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

def get_valid_number(prompt, min_value=1):
    """Ensures the user enters a valid number."""
    while True:
        try:
            value = int(input(prompt))
            if value >= min_value:
                return value
            print(f"❌ Number must be at least {min_value}. Try again.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

def get_yes_no(prompt):
    """Asks the user a yes/no question and ensures valid input."""
    while True:
        choice = input(prompt + " (y/n): ").strip().lower()
        if choice in ('y', 'n'):
            return choice == 'y'  # Returns True for 'y', False for 'n'
        print("❌ Invalid input. Please enter 'y' for yes or 'n' for no.")

def choose_save_location():
    """Opens a file dialog so the user can choose where to save the password file."""
    root = tk.Tk()
    root.withdraw()  # Hide the Tkinter root window

    file_path = filedialog.asksaveasfilename(
        title="Save Password File",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    return file_path  # Returns the full path the user chose

def run_password_generator():
    """Main function to generate multiple passwords."""
    print("🔐 Secure Password Generator 🔐")

    while True:
        # Get user preferences
        num_passwords = get_valid_number("How many passwords do you want to generate? ", min_value=1)
        length = get_valid_number("Enter password length (min. 6 characters): ", min_value=6)
        use_lowercase = get_yes_no("Include lowercase letters?")
        use_uppercase = get_yes_no("Include uppercase letters?")
        use_digits = get_yes_no("Include numbers?")
        use_special_chars = get_yes_no("Include special characters?")

        # Generate passwords
        passwords = [generate_password(length, use_digits, use_special_chars, use_uppercase, use_lowercase) for _ in range(num_passwords)]

        # Display generated passwords
        print("\n✅ Generated Passwords:")
        for i, password in enumerate(passwords, 1):
            print(f"{i}. {password}")

        # Save to file if user wants
        if get_yes_no("\nDo you want to save the passwords to a file?"):
            file_path = choose_save_location()  # Let the user pick a save location
            if file_path:  # If user selected a file
                with open(file_path, "a") as file:
                    for password in passwords:
                        file.write(password + "\n")
                print(f"💾 Passwords saved to: **{file_path}**")
            else:
                print("❌ No file selected. Passwords not saved.")

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
