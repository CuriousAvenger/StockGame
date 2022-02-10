import _sqlite3

with _sqlite3.connect("Accounts.db") as database:
            cursor = database.cursor()
cursor.execute("SELECT * FROM User")
printingInfo = cursor.fetchall()

for i in printingInfo:
    print(i)

print("\n")

with _sqlite3.connect("StocksDB.db") as database:
            cursor = database.cursor()
cursor.execute("SELECT * FROM Info")
printingInfo = cursor.fetchall()

for i in printingInfo:
    print(i)
