import _sqlite3

with _sqlite3.connect("Accounts.db") as database:
    cursor = database.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS User(
    UserID INTEGER PRIMARY KEY,
    Username VARCHAR(20) NOT NULL,
    FirstName VARCHAR(20) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    Password VARCHAR(20) NOT NULL
);
''')

with _sqlite3.connect("StocksDB.db") as database:
    cursor = database.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Info(
    UserID INTEGER PRIMARY KEY,
    Username VARCHAR(20) NOT NULL,
    PortValue VARCHAR(20) NOT NULL,
    BuyingPower VARCHAR(20) NOT NULL,
    Stocks LONGBLOB
);
''')