from utils import box_print, valid_choice
import dbtools
import pickle

#SUB MENUS
def review_transactions():
    table, id, start_date, end_date, threshold, category = "Income", "all", dbtools.start_date, dbtools.today, 0, "all"
    
    while True:
        dbtools.review_transactions(table, id, start_date, end_date, threshold, category)
        options = (
            "0. Back", 
            f"1. Table      - {table}",
            f"2. ID         - {id}",
            f"3. Start Date - {start_date}",
            f"4. End Date   - {end_date}",
            f"5. Threshold  - {threshold}",
            f"6. Category   - {category}"
        )
        
        box_print(options, title="Choose a filter")
        choice = valid_choice(6)
        
        if choice == "0":
            break
        
        elif choice == "1":
            choice = input("Choose (1) Income or (2) Expense: ") or "1"
                
            if choice.isdigit() and choice in ("1", "2"):
                table = ["Income", "Expense"][int(choice) - 1]
                
            else:
                print("Invalid selection.")
                
        elif choice == "2":
            choice = input("Enter transaction ID: ") or "all"
            
            if choice.isdigit() or choice == "all":
                id = choice
            
            else:
                print("ID must be number or 'all'.")
                
        elif choice == "3":
            start_date = input("Enter (YYYY-MM-DD): ") or "min"
        
        elif choice == "4":
            end_date = input("Enter (YYYY-MM-DD): ") or "max"
            
        elif choice == "5":
            try:
                threshold = int(input("Enter threshold: ") or 0)
            
            except ValueError:
                print("Threshold must be a number.")
            
        elif choice == "6":
            category = input("Enter category: ") or "all"
            
        print()

def manage_budget():
    options = ("0. Back", "1. Set Budget", "2. Budget Overview", "3. Delete Budget")
    
    while True:
        box_print(options, title="Choose an option")
        choice = valid_choice(3)
        
        if choice == "0":
            break
            
        elif choice == "1":
            try:
                budget = int(input(f"Enter budget: "))
                    
            except ValueError:
                print("Budget must be a number.\n")
                continue
                
            with open("budget.dat", "wb") as file:
                pickle.dump(budget, file)
                print("Your budget is now set.\n")
            
        elif choice == "2":
                dbtools.budget_overview()
                
        elif choice == "3":
            confirmation = input("Delete transaction? [Y/N]: ").upper()
            
            if confirmation == "Y":
                with open("budget.dat", "wb") as file:
                    print("Your budget plan was deleted.\n")
                    
            else:
                print("Deletion was cancelled.\n")
                
        else:
            print("Invalid selection.\n")
            
        
def make_changes(table, id):
    if not id.isdigit():
        print("Invalid ID.\n")
        return None
        
    dbtools.review_transactions(table, id, "min", "max", 0, "all")
    options = ("0. Back", "1. Edit Record", "2. Delete Record")
    
    while True:
        box_print(options, title="Choose an option")
        choice = valid_choice(6)
    
        if choice == "0":
            break
            
        elif choice == "1":
            dbtools.make_changes(table, id, "edit")
            break
            
        elif choice == "2":
            dbtools.make_changes(table, id, "delete")
            break
            
        else:
            print("Invalid selection.")
            
    print()
            
#MAIN MENU
options = (
    "0. Exit Program",
    "1. Add Income",
    "2. Add Expense",
    "3. Review Transactions", 
    "4. Manage Budget",
    "5. Make Changes"
)

while True:
    box_print(options, title="Choose an option")
    choice = valid_choice(6)
    
    if choice == "0":
        print("Program closed.")
        break
        
    elif choice == "1":
        dbtools.add_transaction("Income")
        
    elif choice == "2":
        dbtools.add_transaction("Expense")
        
    elif choice == "3":
        review_transactions()
        
    elif choice == "4":
        manage_budget()
        
    elif choice == "5":
        choice = input("Choose (1) Income or (2) Expense: ") or "1"
            
        if choice.isdigit() and choice in ("1", "2"):
            table = ["Income", "Expense"][int(choice) - 1]
            
        else:
            print("Invalid selection.")
            continue

        id = input("Enter transaction ID: ")
        make_changes(table, id)
        
    else:
        print("Invalid selection.")
