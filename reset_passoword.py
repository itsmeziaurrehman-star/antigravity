# ==============================================================================
# Password Reset Program
# Uses basic Python and file handling without any external or built-in libraries
# ==============================================================================

def main():
    file_name = "password.txt"

    # Step 1: Read the existing password from password.txt
    try:
        file = open(file_name, "r")
        saved_password = file.read().strip()
        file.close()
    except FileNotFoundError:
        print(f"Error: '{file_name}' not found!")
        print("Creating a new 'password.txt' with default password: Default@12345")
        saved_password = "Default@12345"
        file = open(file_name, "w")
        file.write(saved_password)
        file.close()

    print("---------------------------------------------")
    print("           PASSWORD RESET SYSTEM             ")
    print("---------------------------------------------")

    # Step 2: Ask user for old password and verify match
    old_password = input("Enter current (old) password: ")

    if old_password != saved_password:
        print("\n[!] Authentication Failed: Old password does not match.")
        return

    print("\n[+] Old password matched! You may now set a new password.")

    # Step 3: Loop to input and validate the new password
    while True:
        print("\nNew Password Requirements:")
        print(" 1. Must be greater than 8 characters long (> 8)")
        print(" 2. Must contain at least one numeric digit (0-9)")
        print(" 3. Must contain at least one alphabet character")
        print(" 4. Must contain at least one uppercase letter (A-Z)")
        print(" 5. Must contain at least one special character (!@#$%^&*...)")

        new_password = input("\nEnter new password: ")

        # ----------------- VALIDATION CHECKS -----------------
        errors = []

        # Requirement 1: Length check (> 8 characters)
        if len(new_password) <= 8:
            errors.append("Password must be strictly greater than 8 characters.")

        # Requirement 2: Character type checks
        has_numeric = False
        has_alphabet = False
        has_uppercase = False
        has_special = False

        special_characters = "!@#$%^&*()-_=+[{]};:'\",<.>/?`~|\\ "

        for ch in new_password:
            # Check numeric
            if '0' <= ch <= '9':
                has_numeric = True
            # Check alphabet & uppercase
            if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z'):
                has_alphabet = True
                if 'A' <= ch <= 'Z':
                    has_uppercase = True
            # Check special characters
            if ch in special_characters:
                has_special = True

        if not has_numeric:
            errors.append("Password must contain at least one numeric digit (0-9).")
        if not has_alphabet:
            errors.append("Password must contain at least one alphabet character.")
        if not has_uppercase:
            errors.append("Password must contain at least one uppercase letter (A-Z).")
        if not has_special:
            errors.append("Password must contain at least one special character.")

        # If any validation rule failed, show errors
        if len(errors) > 0:
            print("\n[!] The password entered does not meet the requirements:")
            for err in errors:
                print(f"    - {err}")
            retry = input("\nDo you want to try again? (y/n): ").strip().lower()
            if retry != 'y':
                print("Password reset cancelled.")
                return
            continue

        # Requirement 3: Re-enter password to validate match
        re_entered_password = input("Re-enter new password to confirm: ")
        if new_password != re_entered_password:
            print("\n[!] Error: Re-entered password does not match new password.")
            retry = input("Do you want to try again? (y/n): ").strip().lower()
            if retry != 'y':
                print("Password reset cancelled.")
                return
            continue

        # Step 4: Store the new password in the same file
        file = open(file_name, "w")
        file.write(new_password)
        file.close()

        print("\n=============================================")
        print("[+] SUCCESS: Password updated successfully!")
        print(f"[+] New password has been saved to '{file_name}'.")
        print("=============================================")
        break


if __name__ == "__main__":
    main()
