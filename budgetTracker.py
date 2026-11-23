from utils import box_print, box_print2D, bar_graph, format
import mysql.connector as connector
import pickle

################################################################################

passwd = input("Enter Password: ")
    
try:
    database = connector.connect("budgetTracker.db")
    
    '''user="root", 
    host="localhost", 
    passwd=passwd,
    charset="utf8")'''

    cursor = database.cursor()
        
except: #access denied
    print("ERROR: Wrong Password!")
    exit()

################################################################################

current_category = None

def category(action):
    """make categories to manage different types of transactions separately.
        
    For example, 
    a Hobby category or entertainment category for games and movies,
    a person category to divide expenses for each person in a family,
    a Food category to track your eating habits,
    etc.

    global current_category
    cursor.execute("show databases")
    databases, options = [], []
    idx = 1
        
    for database, _ in cursor:
        idx += 1
        databases.append(database)
        options.append(str(idx) + ". " + database)
        
    if action == "Change Current Category":
        box_print(options, title="databases")
        choice = input("choose an option: ")
        
        if choice.isdigit() and int(choice) in range(1, idx+1):
            database = databases[int(choice)-1]
            cursor.execute("use " + database)
            
            current_category = database
            return database
        
        else:
            print("ERROR: Invalid Input!")
        
    elif action == "Make New Category":
        while True:
            name = input("Enter category name: ").strip().lower()
    
            if name == "0":
                return None
                
            elif name not in databases:
                cursor.execute("create database" + name)
                break
    
            else:
                print("ERROR: Category exists!")
        """
        
    cursor.execute('''
        create table income (
        label text,
        amount decimal(10, 2),
        date date,
        time time default=null,
        location text default=null,
        short_desc text default=null)
        ''')
    
    cursor.execute('''
        create table expense (
        label text,
        amount decimal(10, 2),
        date date,
        time time default=null,
        location text default=null,
        short_desc text default=null)
        ''')
        
    """elif action == "Rename Category":
        box_print(options, title="databases")
        choice = input("choose an option: ")
        
        if choice.isdigit() and int(choice) in range(1, idx+1):
            original = databases[int(choice)-1]
            renamed = input("choose a new name: ")
            cursor.execute("rename database " + original + " " + renamed)
            
            if original == current_category:
                current_category = renamed
            
        else:
            print("ERROR: Invalid Input!")
        
    elif action == "Delete Category":
        box_print(options, title="databases")
        choice = input("choose an option: ")
        
        if choice.isdigit() and int(choice) in range(1, idx+1):
            database = databases[int(choice)-1]
            choice = input("Are you sure you want to delete" + database + " ? [Y/N]")
            
            if choice == "Y":
                given_passwd = input("Password required: ")
                
                if given_passwd != passwd:
                    return print("Incorrect Password!")
                    
            else:
                return print("Action Cancelled!")
                
            cursor.execute("delete database " + database)
            
            if database == current_category:
                #⚠️what happens when currenr database is deleted
                current_category = renamed
            
        else:
            print("ERROR: Invalid Input!")
            
    """
    
################################################################################

def add_income_expense(table, label, amount, date, time=None, location=None, short_desc=None):
    """you may add regular incomes/expenses so BudgetTracker modifies the tables on a regular specified basis.
        
    Regular income includes your Job salary or business income
    Regular expenses include electricity bill and water bill"""
        
    #appending new row⚠️
    row = format(label, amount, date, time, location, short_desc)
    cursor.execute("insert into " + table + " values (" + row + ")")

################################################################################

filepath = "reminder.dat"

def reminder(action, filepath=filepath):
    """display a reminder next time you open BudgetTracker
    plan upcoming expenses"""
    
    if action in ("Check Reminder", "Check Savings"):
        messages = []
        file_exists = False
        
        try:
            file = open(filepath, "rb")
            file_exists = True
        
        except FileNotFoundError:
            messages = ["Nothing to see here..."]
        
        while file_exists:
            try:
                message = pickle.load(file)
                messages.append(message)
                
            except EndOfFileError:
                break
            
        return box_print(messages, action)
    
    choice = input("Delete old message? [Y/N]").strip()
    if choice == "Y":
        file = open(filepath, "wb")
    
    else:
        return print("Action cancelled!")
        
    if action in ("Delete Reminder", "Delete Savings Goal"):
        return None
        
    print("Enter new message below (enter 0 to stop)")
    
    messages = []
    while True:
        message = input(">> ")
        
        if message == "0":
            break
            
        messages.append(message+"\n")
    
    pickle.dump(messages, file)
    file.close()
    
################################################################################

def savings(action):
    if action == "Set Savings Goal":
        return reminder("set", "Savings Goal", "savings_goal.dat")
        
    elif action in ("Check Savings", "Delete Savings Goal"):
        return reminder(action, category + "savings_goal.dat")
        
    cursor.execute("select A - B from income A, expense B")
    
    rows = []
    for row in cursor:
        rows.append(row)
        
    box_print2D(rows)
    
    cursor.execute("select sum(A - B) from income A, expense B")
    
    for savings in cursor:
        print("You have saved ₹", savings)

################################################################################

def checkup(table):
    """table of all income, expenses, savings"""
        
    cursor.execute("select * from" + table.lower())
    
    rows = []
    for row in cursor:
        rows.append(row)
        
    box_print2D(rows)

################################################################################

def visualisation(target):
    cursor.execute("select label, amount from " + target.lower())
    
    labels, amounts = [], []
    for row in cursor:
        label, amount = row
        labels.append(label)
        amounts.append(amount)
        
    bar_graph(labels, amounts)

################################################################################


    