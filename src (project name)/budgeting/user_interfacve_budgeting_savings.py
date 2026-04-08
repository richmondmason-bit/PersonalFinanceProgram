import savings_goals
import budgeting

def main_menu():
    while True:
        print("\n==============================")
        print("   PERSONAL FINANCE TRACKER   ")
        print("==============================")
        print("1. Set Savings Goal")
        print("2. Add to Savings")
        print("3. View Savings Progress")
        print("4. Set/Update Category Budget")
        print("5. Add Expense to Category")
        print("6. View Budget Status")
        print("7. Exit")
        
        choice = input("\nChoose an option (1-7): ")

        if choice == '1': 
            savings_goals.set_savings_goal()
        elif choice == '2': 
            savings_goals.add_savings()
        elif choice == '3': 
            savings_goals.view_progress()
        elif choice == '4': 
            budgeting.manage_budget()
        elif choice == '5': 
            budgeting.add_expense()
        elif choice == '6': 
            budgeting.view_budget_status()
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main_menu()