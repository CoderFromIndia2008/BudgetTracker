from box_print import box_print
import dbtools2 as dbtools
import pickle

#SUB MENUS
def review_transactions():
    table      = "Income"
    id         = "all"
    start_date = dbtools.start_date
    end_date   = dbtools.today
    threshold  = 0
    category   = "all"
    
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
        choice = input("~ ")
        print()
        
        if choice == "0": break
        
        if choice == "1":
            try:
                table_choice = int(input("Enter (1) Income or (2) Expense: ") or 1)
                table = ["Income", "Expense"][table_choice - 1]
            except:
                print("Invalid Input")
                
        elif choice == "2":
            try:
                id = int(input("Enter transaction ID: ") or 0)
                id = id if id != 0 else "all"
            except ValueError:
                print("Transaction ID must be a number or 'all'")
                
        elif choice == "3":
            start_date = input("Enter (YYYY-MM-DD): ") or "min"
        
        elif choice == "4":
            end_date = input("Enter (YYYY-MM-DD): ") or "max"
            
        elif choice == "5":
            try:
                threshold = int(input("Enter threshold: ") or 0)
            except ValueError:
                print("Threshold must be a number")
            
        elif choice == "6":
            category = input("Enter category: ") or "all"
            
        else:
            print("Invalid Input")
        print()            

def manage_budget():
    options = (
        "0. Back", 
        "1. Set Budget", 
        "2. Budget Overview",
        "3. Delete Budget"
    )
    
    while True:
        box_print(options, title="Choose an option")
        choice = input("~ ")
        print()
        
        if choice == "0": break
            
        if choice == "1":
            try:
                budget = int(input(f"Enter budget: "))
                print("Your budget is set!")
                with open("budget.dat", "wb") as file:
                    pickle.dump(budget, file)
            except ValueError:
                print("Budget must be a number")
            
        elif choice == "2":
                dbtools.budget_overview()
                
        elif choice == "3":
            confirmation = input("Delete transaction? [Y/N]: ").upper()
            if confirmation == "Y":
                with open("budget.dat", "wb") as file:
                    print("Your budget plan was deleted")
                    
            else:
                print("Deletion cancelled")
    
        else:
            print("Invalid Input")
        print()
            
            
def make_changes(table, id):
    dbtools.review_transactions(table, id, "min", "max", 0, "all")
    options = (
        "0. Back",
        "1. Edit Record",
        "2. Delete Record"
    )
    
    while True:
        box_print(options, title="Choose an option")
        choice = input("~ ")
        print()
    
        if choice == "0": break
        
        elif choice == "1":
            dbtools.make_changes(table, id, "edit")
            break
            
        elif choice == "2":
            dbtools.make_changes(table, id, "delete")
            break
            
        else:
            print("Invalid Input\n")
        
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
    choice = input("~ ")
    print()
    
    if choice == "0":
        print("Program Closed")
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
        try:
            table_choice = int(input("Enter (1) Income or (2) Expense: ") or 1)
            table = ["Income", "Expense"][table_choice - 1]
            id = int(input("Enter transaction ID: "))
            print()
            make_changes(table, id)
        except:
            print("Invalid Input\n")
        
    else:
        print("Invalid Input\n")