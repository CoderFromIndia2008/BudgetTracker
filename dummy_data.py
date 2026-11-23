import mysql.connector as mysql

password = input("Enter password: ")
connection = mysql.connect(user="root", host="localhost", passwd=password, charset="utf8")
cursor = connection.cursor()

cursor.execute("""
    insert into income (amount, category, date, description) values
    (1000, "freelance", "2026-11-01", "made budget tracker software for client"),
    (2000, "item sale", "2026-11-10", "sold old furniture"),
    (5000, "freelance", "2026-11-15", "made attendance software for client"),
    (2500, "freelance", "2026-11-17", "made data management software for client"),
    (10000, "part time", "2026-11-20", "part time work at xyz.inc")
    """)
        
cursor.execute("""
    insert into expense (amount, category, date, description) values
    (500, "snacks", "2026-11-03", "birthday party!"),
    (1500, "repairs", "2026-11-10", "broken sink"),
    (700, "hobby", "2026-11-14", "bought a fantasy novel"),
    (2000, "health", "2026-11-17", "sprained ankle"),
    (3000, "snacks", "2026-11-20", "brother's wedding anniversary!")
    """)

cursor.execute("commit")