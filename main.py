from addMethods import add_customer, add_policy
from removeMethods import remove_customer, remove_policy
from searchMethods import search_customer, search_policy
from displayMethods import display_customers, display_policies, display_home_policies, display_car_policies, display_life_policies
# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------

def display_menu():
    while True:
        print("\n--- Display Tables ---")
        print("1. All customers")
        print("2. All insurance policies")
        print("3. All home policy details")
        print("4. All car policy details")
        print("5. All life policy details")
        print("0. Back")

        choice = input("Select an option: ").strip()

        if choice == "1":
            display_customers()
        elif choice == "2":
            display_policies()
        elif choice == "3":
            display_home_policies()
        elif choice == "4":
            display_car_policies()
        elif choice == "5":
            display_life_policies()
        elif choice == "0":
            break
        else:
            print("Invalid option, try again.")


def main():
    while True:
        print("\n=== Insurance Management System ===")
        print("1. Add customer")
        print("2. Add policy to existing customer")
        print("3. Remove customer")
        print("4. Remove policy")
        print("5. Search for customer")
        print("6. Search policy by ID")
        print("7. Display tables")
        print("0. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            add_customer()
        elif choice == "2":
            add_policy()
        elif choice == "3":
            remove_customer()
        elif choice == "4":
            remove_policy()
        elif choice == "5":
            search_customer()
        elif choice == "6":
            search_policy()
        elif choice == "7":
            display_menu()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()
