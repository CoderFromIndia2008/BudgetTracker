import utils
import dbtools
import pickle

###################################SUB_MENU_1###################################

def review_transactions():
    table      = "Income"
    start_date = dbtools.start_date
    end_date   = dbtools.today
    threshold  = "0"
    location   = "All"
    category   = "All"
    
    while True:
        dbtools.review_transactions(table, start_date, end_date, threshold, location, category)

        options = (
            "0. Back",
            f"1. Table      : {table}",
            f"2. Start Date : {start_date}",
            f"3. End Date   : {end_date}",
            f"4. Threshold  : {threshold}",
            f"5. Category   : {category}"
        )
        
        utils.box_print(options, title="Choose a filter")
        choice = input("~ ")
        print()
        
        if choice == "0":
            break
        
        if choice == "1":
            table = input("Enter (i) income or (e) expense: ").lower()
            table = "Income" if table == "i" else "Expense"
                
        elif choice == "2":
            start_date = input("Enter (YYYY-MM-DD or 'all'): ")
        
        elif choice == "3":
            end_date = input("Enter (YYYY-MM-DD or 'all'): ")
            
        elif choice == "4":
            try:
                threshold = int(input("Enter a threshold: "))
            
            except:
                print("Threshold must be a number")
            
        elif choice == "5":
            category = input("Enter a category: ")
            
        else:
            print("Invalid Input\n")
    
###################################SUB_MENU_2###################################

def manage_budget():
    options = (
        "0. Back", 
        "1. Set Budget", 
        "2. Budget Overview",
        "3. Delete Budget"
    )
    
    while True:
        utils.box_print(options, title="Choose an option")
        choice = input("~ ")
        print()
        
        if choice == "0":
            break
            
        if choice == "1":
            budget = input(f"Enter budget: ")
            print("Your budget is set!\n")
            
            with open("budget.dat", "wb") as file:
                pickle.dump(budget, file)
                break
                
        elif choice == "2":
                dbtools.budget_overview()
                break
                
        elif choice == "3":
            with open("budget.dat", "wb") as file:
                print("Your budget plan was deleted\n")
                break
        
        else:
            print("Invalid Input\n")
            
####################################MAIN_MENU###################################
        
options = (
    "0. Exit Program",
    "1. Add Income",
    "2. Add Expense",
    "3. Review Transactions", 
    "4. Manage Budget",
)

while True:
    utils.box_print(options, title="Choose an option")
    choice = input("~ ")
    print()
    
    if choice == "0":
        print("Program Closed")
        break
        
    elif choice == "1":
        dbtools.add_transaction("income")
        
    elif choice == "2":
        dbtools.add_transaction("expense")
        
    elif choice == "3":
        review_transactions()
        
    elif choice == "4":
        manage_budget()
        
    else:
        print("Invalid Input\n")