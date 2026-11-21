import mysql.connector as mysql
import pickle
import utils
import time

#####################################SETUP######################################

password = input("Enter password: ")

try:
    connection = mysql.connect(user="root", host="localhost", passwd=password)

except:
    raise Exception("Wrong Password")

cursor = connection.cursor()

try:
    cursor.execute("use budgetTracker")
    
except:
    cursor.execute("create database budgetTracker")
    cursor.execute("use budgetTracker")
    
    cursor.execute("""
        create table income (
        amount      int,
        category    text,
        date        date, 
        description text
    )""")
    
    cursor.execute("""
        create table expense (
        amount      int,
        category    text,
        date        date, 
        description text
    )""")

start_date = time.strftime("%Y-%m-01")
month_year = time.strftime("%b-%Y")
today      = time.strftime("%Y-%m-%d")
    
##################################FUNCTIONALITY#################################

def add_transaction(table):
    print("NOTE: Enter 'null' for fields to be left out")
    print("NOTE: Amount and category cannot be null\n")
    
    while True:
        try:
            amount = int(input("Enter amount: "))
            category = input("Enter category: ")
            
            if category.lower() != "null":
                break
                
            print("Category cannot be null")            
            
        except ValueError:
            print("Please enter a number")
            
    date = input("Enter date (YYYY-MM-DD): ")
    description = input("Enter short description: ")
    record = (amount, category, date, description)
            
    cursor.execute(f"insert into {table} values {str(record)}")
    cursor.execute("commit")
    print("\nTransaction added!\n")

##################################FUNCTIONALITY#################################
    
def review_transactions(table, start_date, end_date, threshold, location, category):
    start_date = "1970-01-01" if start_date.lower() == "all" else start_date
    end_date   = "2100-01-01" if end_date.lower()   == "all" else end_date
    category   = "category"   if category.lower()   == "all" else f"'{category}'"
    
    headers = [("amount", "category", "date", "description")]                    
    offset, choice = 0, "Y"
    
    while choice == "Y":
        try:
            cursor.execute(f"""
                select * from {table}
                where 
                amount >= {threshold}
                and date between '{start_date}' and '{end_date}'
                and category = {category}
                limit 15 offset {offset}
            """)
            
        except:
            print("Invalid date")
            break

        rows = cursor.fetchall()
        if len(rows) == 0:
            if offset == 0:
                print("Empty selection")
                
            break 
        
        if offset != 0:
            choice = input("Show more? [Y/N]: ").upper()

        utils.box_print2D(headers + rows, title=f"{table} Table", space=1)
        print()
        offset += 15
                
##################################FUNCTIONALITY#################################

def budget_overview():
    cursor.execute(f"""
        select sum(amount) from income
        where 
        date between '{start_date}' and current_date
    """)
    
    earned = cursor.fetchone()
    earned = earned[0] if len(earned) != 0 and earned[0] is not None else 0
        
    cursor.execute(f"""
        select sum(amount) from expense
        where 
        date between '{start_date}' and current_date
    """)
        
    spent = cursor.fetchone()
    spent = spent[0] if len(spent) != 0 and spent[0] is not None else 0
    
    saved = earned - spent
    
    try:
        file = open("budget.dat", "rb")
        budget_goal = pickle.load(file)
        
    except FileNotFoundError or EOFError:
        print("No budget plan found")
        return None
    
    text = (
        f"Budget : {budget_goal}",
        f"Spent  : {spent}",
        f"Saved  : {saved}",
        f"Status : {'Over' if saved < 0 else 'Under'} budget"
    )
    
    utils.box_print(text, title=f"Overview for {month_year}", space=2)
    print()
