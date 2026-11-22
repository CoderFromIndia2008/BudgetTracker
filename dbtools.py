from box_print import box_print, box_print2D
import mysql.connector as mysql
import pickle
import time

password = input("Enter password: ")
print()

try:
    connection = mysql.connect(user="root", host="localhost", passwd=password)
    cursor = connection.cursor()
except:
    raise Exception("Access Denied")
    
try:
    cursor.execute("use budgetTracker")
except:
    cursor.execute("create database budgetTracker")
    cursor.execute("use budgetTracker")
    cursor.execute("""
        create table income (
        id          integer      primary key auto increment,
        amount      integer      not null,
        category    varchar(20),
        date        date, 
        description varchar(50)
        )""")
        cursor.execute("""
        create table expense (
        id          integer      primary key auto increment,
        amount      integer      not null,
        category    varchar(20),
        date        date, 
        description varchar(50)
        )""")

start_date = time.strftime("%Y-%m-01")
month_year = time.strftime("%b-%Y")
today      = time.strftime("%Y-%m-%d")

def add_transaction(table):
    while True:
        try:
            amount = int(input("Enter amount: "))
            break
        except ValueError:
            print("Please enter a number")
            
    category = input("Enter category: ") or "null"
    date = input("Enter date (YYYY-MM-DD): ") or today
    description = input("Enter short description: ") or "null"
    record = (amount, category, date, description)
    cursor.execute(f"""
        insert into {table} 
        (amount, category, date, description) values 
        {str(record)}
    """)
    print("Transaction added!\n")
    cursor.execute("commit")
    
def review_transactions(table, id, start_date, end_date, threshold, category):
    id         = "ID"         if id                 == "all" else id
    start_date = "2000-01-01" if start_date.lower() == "min" else start_date
    end_date   = "3000-01-01" if end_date.lower()   == "max" else end_date
    category   = "category"   if category.lower()   == "all" else f"'{category}'"
    headers = [("id", "amount", "category", "date", "description")]                    
    offset, choice = 0, "Y"
    
    while choice == "Y":
        try:
            cursor.execute(f"""
                select * from {table}
                where 
                id = {id} and
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
                print("Empty selection\n")
            break 
        
        if offset != 0:
            choice = input("Show more? [Y/N]: ").upper() or "Y"
        box_print2D(headers + rows, title=f"{table} Table", space=1)
        print()
        offset += 15

def budget_overview():
    cursor.execute(f"""
        select sum(amount) from income
        where 
        date between '{start_date}' and current_date
    """)
    earned = cursor.fetchone()[0]
    if earned is None:
        earned = 0
        
    cursor.execute(f"""
        select sum(amount) from expense
        where 
        date between '{start_date}' and current_date
    """)
        
    spent = cursor.fetchone()[0]
    if spent is None:
        spent = 0
    saved = earned - spent
    
    try:
        with open("budget.dat", "rb") as file:
            budget_goal = pickle.load(file)
    except FileNotFoundError or EOFError:
        print("No budget plan found")
        return None
    
    text = (
        f"Budget - {budget_goal:,}",
        f"Earned - {earned:,}",
        f"Spent  - {spent:,}",
        f"Saved  - {saved:,}",
        f"Status - {'Over' if saved < 0 else 'Under'} budget"
    )
    box_print(text, title=f"Overview for {month_year}", space=2)
    
def make_changes(table, id, mode):
    if mode == "delete":
        confirmation = input("Delete transaction? [Y/N]: ").upper()
        if confirmation != "Y":
            print("Deletion cancelled\n")
            return None
        cursor.execute(f"""
            delete from {table}
            where id = {id}
        """)
        cursor.execute("commit")
        print(f"Transaction no. {id} was deleted\n")
        return None
    
    while True:
        try:
            amount = int(input("Enter amount: ") or 0)
            break
        except ValueError:
            print("Please enter a number")
    
    category = input("Enter category: ") 
    date = input("Enter date (YYYY-MM-DD): ")
    description = input("Enter short description: ")
    amount      = "amount"      if amount      == 0  else amount
    category    = "category"    if category    == "" else f"'{category}'"
    date        = "date"        if date        == "" else f"'{date}'"
    description = "description" if description == "" else f"'{description}'"
    cursor.execute(f"""
        update {table}
        set 
        amount = {amount},
        category = {category},
        date = {date},
        description = {description}
        where id = {id}
    """)
    cursor.execute("commit")
    print(f"Transaction no. {id} was edited\n")