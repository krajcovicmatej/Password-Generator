import random
import string
import os  # Import os module to handle file paths

def generate_password(length, use_digits=True, use_special_chars=True, use_uppercase=True, use_lowercase=True):
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

def run_password_generator():
    """Main function to generate passwords in a loop."""
    print("🔐 Secure Password Generator 🔐")

    while True:
        # Get user preferences
        length = get_valid_number("Enter password length (min. 6 characters): ", min_value=6)
        use_lowercase = get_yes_no("Include lowercase letters?")
        use_uppercase = get_yes_no("Include uppercase letters?")
        use_digits = get_yes_no("Include numbers?")
        use_special_chars = get_yes_no("Include special characters?")

        # Generate and display password
        password = generate_password(length, use_digits, use_special_chars, use_uppercase, use_lowercase)
        if password:
            print(f"\n✅ Generated password: **{password}**")

            # Save to file if user wants
            if get_yes_no("Do you want to save the password to a file?"):
                file_path = os.path.abspath("passwords.txt")  # Get full path of the file
                with open(file_path, "a") as file:
                    file.write(password + "\n")
                print(f"💾 Password saved to: **{file_path}**")

        # Ask if they want another password, otherwise exit
        if not get_yes_no("\nGenerate another password?"):
            print("\n👋 Goodbye! Thanks for using the Secure Password Generator.")
            break

# Improved entry point
if __name__ == "__main__":
    try:
        run_password_generator()
    except KeyboardInterrupt:
        print("\n❌ Process interrupted. Exiting safely. 👋")
