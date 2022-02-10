import yfinance as yf
import _sqlite3
import hashlib
import sys
import getpass
import os
import json

def passHasher(Passwd2Hash):
    resultHash = hashlib.md5(Passwd2Hash.encode())
    return resultHash.hexdigest()

def stockGame(username, user):
    while True:
        os.system('cls')
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        print(f'         [+] Welcome {user}')
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        print("1. View Portfolio")
        print("2. Make A Trade")
        print("3. Game Ranking")
        print("4. Exit Stock Game\n")
        
        userChoice = input("[*] Enter Your Choice: ")
        if userChoice == '1':
            os.system('cls')
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')

            try:
                with _sqlite3.connect("StocksDB.db") as database:
                            cursor = database.cursor()
                findVal = ("SELECT BuyingPower FROM Info WHERE Username = ?")
                cursor.execute(findVal, [(username)])
                buyingpower = cursor.fetchall()[0][0]

                findVal = ("SELECT Stocks FROM Info WHERE Username = ?")
                cursor.execute(findVal, [(username)])
                stock_dict = cursor.fetchall()[0][0]
                stock_dict = json.loads(stock_dict.decode('utf-8'))

                portval = 0
                for key in stock_dict:
                    portval += stock_dict[key][1] * yf.Ticker(key).info['currentPrice']
                portval += float(buyingpower)
                returnval = ((portval - 100000.0)/100000.0)*100.0

                print(f"[+] User: {username} Portfolio's Statistics")
                print(f"     Portfolio Val: ${portval}")
                print(f"     Buying Power: ${buyingpower}")
                print(f"     Return Value: {round(returnval,2)}%")

                print("\n[+] Each Stock's Contributions: ")
                for key in stock_dict:
                    market = round(yf.Ticker(key).info['currentPrice']*stock_dict[key][1],4)
                    pro_los = market - (stock_dict[key][1]*stock_dict[key][0])
                    print(f"     Stock: {key} No: {stock_dict[key][1]} Paid: ${stock_dict[key][0]}")
                    print(f"     Market Val: {market} Profit/Loss: ${round(pro_los,4)}\n")

                insertDatabase = '''UPDATE Info SET PortValue = ? WHERE Username = ?'''
                cursor.execute(insertDatabase,[(portval),(username)])
                database.commit() #update the database completely
                input("[*] Press Any Key To Continue")
            except:
                print("[!] Error: Try Buying Stocks First!")
                input("[*] Press Any Key To Continue")

        elif userChoice == '2':
            os.system('cls')
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
            print("1. Buy Stocks")
            print("2. Sell Stocks\n")
            
            userChoice = input("[*] Enter Your Choice: ")
            if userChoice == '1':
                os.system('cls')
                print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
                print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')

                while True:
                    try:
                        stock = input("[*] Enter The Stock's Ticker: ").upper()
                        ticker = yf.Ticker(stock)
                        ticker.info['currentPrice']
                        break
                    except KeyError:
                        print("[!] Error: Choose A Valid Ticker!\n")

                gain = round(float(ticker.info['currentPrice'])-float(ticker.info['open']),4)
                if gain > 0:
                    gain = "+"+str(abs(gain))
                elif gain < 0:
                    gain = "-"+str(abs(gain))
                highlow = f"{ticker.info['dayLow']}-{ticker.info['dayHigh']}"

                print('\n')
                print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
                print(f"{stock}: {ticker.info['currentPrice']}{gain} Volume: {ticker.info['volume']}")
                print(f"Bid: {ticker.info['bid']} Ask: {ticker.info['ask']}")
                print(f"Day's Change: {highlow}")
                print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n')

                noStocks = int(input("[*] Enter The Number Of Stocks To Buy: "))
                totalvalue = round(float(ticker.info['currentPrice'])*noStocks, 4)
                print(f"[*] Estimated Stock Cost for {stock}: {totalvalue}")

                confirm = input("[*] Do You Want To Confirm Purchase: (Y/N)")
                if confirm.lower() == 'y':
                    with _sqlite3.connect("StocksDB.db") as database:
                        cursor = database.cursor()

                    findVal = ("SELECT BuyingPower FROM Info WHERE Username = ?")
                    cursor.execute(findVal, [(username)])
                    results = cursor.fetchall()
                    buyingpower = float(results[0][0]) - float(totalvalue)
                    buyingpower = round(buyingpower, 4)

                    if buyingpower <= 0:
                        print("[!] Buying Power Too Low To Make Transaction")
                        print(f"[+] Current Buying Power: {results[0][0]}")
                        input("[*] Press Any Key To Continue")
                    else:
                        print(f"[+] Current Buying Power: {round(buyingpower,4)}")
                        try:
                            findstocks = ("SELECT Stocks FROM Info WHERE Username = ?")
                            cursor.execute(findstocks, [(username)])
                            results = cursor.fetchall() # results exist if the user exists
                            results = results[0][0]
                            stock_dict = json.loads(results.decode('utf-8'))
                        except AttributeError:
                            stock_dict = {}

                        if stock in stock_dict.keys():
                            pastPrice = stock_dict[stock][0]
                            pastNum = stock_dict[stock][1]
                            currentNum = ((pastPrice*pastNum) + (ticker.info['currentPrice']*noStocks))/(pastNum+noStocks)
                            array = [currentNum, (pastNum+noStocks)]
                            stock_dict[stock] = array
                        else:
                            array = [ticker.info['currentPrice'], noStocks]
                            stock_dict[stock] = array

                        dict_byte = json.dumps(stock_dict).encode('utf-8')
                        insertDatabase = '''UPDATE Info SET BuyingPower = ?, Stocks = ? WHERE Username = ?'''
                        cursor.execute(insertDatabase,[(buyingpower),(dict_byte),(username)])
                        database.commit() #update the database completely

                        print("[+] Transaction Successful Completed!")
                        input("[*] Press Any Key To Continue")
                else:
                    continue
            elif userChoice == '2':
                os.system('cls')
                print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
                print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')

                with _sqlite3.connect("StocksDB.db") as database:
                    cursor = database.cursor()
                findstocks = ("SELECT Stocks FROM Info WHERE Username = ?")
                cursor.execute(findstocks, [(username)])
                results = cursor.fetchall() # results exist if the user exists
                results = results[0][0]
                stock_dict = json.loads(results.decode('utf-8'))

                print("[+] Here Are Your Stock Holdings: ")
                for key in stock_dict:
                    print(f"     Stock: {key} No: {stock_dict[key][1]}")
                
                stock = ''
                while stock not in stock_dict.keys():
                    stock = input("\n[*] Enter The Stock's Ticker: ").upper()
                    if stock not in stock_dict.keys():
                        print("[!] Error: Not Found Try Again!")

                ticker = yf.Ticker(stock)
                numSell = input("[*] How Many Stocks To Sell: ")

                findVal = ("SELECT BuyingPower FROM Info WHERE Username = ?")
                cursor.execute(findVal, [(username)])
                results = cursor.fetchall()
                buyingpower = round(float(results[0][0]),4)

                choice = input("[*] Do You Confirm Your Transaction: (Y/N)\n")
                if choice.lower() == "y":
                    currentNum = int(stock_dict[stock][1]) - int(numSell)
                    if currentNum <= 0:
                        numSell = stock_dict[stock][1]
                        del stock_dict[stock]
                    else:
                        stock_dict[stock][1] = currentNum
                    buyingpower = (float(ticker.info['currentPrice'])*float(numSell)) + buyingpower

                    dict_byte = json.dumps(stock_dict).encode('utf-8')
                    insertDatabase = '''UPDATE Info SET BuyingPower = ?, Stocks = ? WHERE Username = ?'''
                    cursor.execute(insertDatabase,[(buyingpower),(dict_byte),(username)])
                    database.commit() #update the database completely

                    print(f"[+] Current Buying Power: {round(buyingpower,4)}")
                    print("[+] Transaction Successful Completed!")
                    input("[*] Press Any Key To Continue")
                elif choice.lower() == "n":
                    continue
                else:
                    print("[!] Error: Enter value from given list")
                    input("[*] Press Any Key To Continue")
            else:
                print("[!] Error: Enter value from given list")
                input("[*] Press Any Key To Continue")

        elif userChoice == '3':
            os.system('cls')
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
            print("             Stock Game Rankings")
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
            with _sqlite3.connect("StocksDB.db") as database:
                cursor = database.cursor()
            findstocks = ("SELECT PortValue,Username FROM Info")
            cursor.execute(findstocks)

            ranking = {}
            for vals in cursor.fetchall():
                ranking[vals[1]] = float(vals[0])
            ranking = sorted(ranking.items(), key=lambda kv: kv[1], reverse=True)
            
            for i in range(len(ranking)):
                print(f"{i+1}. {ranking[i][0]} Port Val: {ranking[i][1]}")

            print("\n[+] Note: Update Ranking By Opening Portfolio")
            input("[*] Press Any Key To Continue")
        elif userChoice == '4':
            print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            print("           Thanks For Passing By!!")
            print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            return 0
        else:
            print("[!] Error: Enter value from given list")
            input("[*] Press Any Key To Continue")

def loginAndGame():
    while True:
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')

        username = input("[*] Enter Your Username: ")
        password = getpass.getpass(prompt="[*] Enter Your Password: ")
        password = passHasher(password) #hashed password

        with _sqlite3.connect("Accounts.db") as database:
            cursor = database.cursor() #connect to the server
        findUser = ("SELECT * FROM User WHERE Username = ? AND Password = ?")
        cursor.execute(findUser, [(username),(password)])
        results = cursor.fetchall() # results exist if the user exists

        if results:
            os.system('cls')
            for i in results:
                stockGame(username, i[2])
            break
        else:
            print("[!] Error: Username Or Password Incorrect")
            choice = input("[*] Do You Want To Try Again? (Y/N)")
            if choice.lower() == "n":
                print("\n")
                print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                print("           Thanks For Passing By!!")
                print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                return 0

def newUser():
    os.system('cls')
    found = 0
    while found == 0:
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        username = input('[*] Enter Your Username: ')

        with _sqlite3.connect("Accounts.db") as database:
            cursor = database.cursor()
        findUser = ("SELECT * FROM User WHERE Username = ?")
        cursor.execute(findUser,[(username)])
        
        if cursor.fetchall():
            print("[!] Error: Username Already Taken")
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        else:
            found = 1

    firstname = input("[*] Enter Your Firstname: ")
    email = input('[*] Enter Your Email: ')
    password = getpass.getpass(prompt="[*] Enter Your Password: ")
    passwd1 = getpass.getpass(prompt="[*] Re-Enter Your Password: ")

    while passwd1 != password:
        print("[!] Error: Your Passwords Didn't Match")
        password = getpass.getpass(prompt="[*] Enter Your Password: ")
        passwd1 = getpass.getpass(prompt="[*] Re-Enter Your Password: ")
    password = passHasher(password)

    insertDatabase = '''INSERT INTO User(Username, FirstName, Email, Password) VALUES(?,?,?,?)'''
    cursor.execute(insertDatabase,[(username),(firstname),(email),(password)])
    database.commit() #update the database completely
    print("[+] Your Account Has Been Set.")
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    input("[*] Press Any Key To Continue")

    with _sqlite3.connect("StocksDB.db") as database:
        cursor = database.cursor()
    insertDatabase = '''INSERT INTO Info(Username, PortValue, BuyingPower) VALUES(?,?,?)'''
    cursor.execute(insertDatabase,[(username),(100000.00),(100000.00)])
    database.commit() #update the database completely

while True:
    os.system('cls')
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print("         Welcome To My Application")
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print("1. Login Account")
    print("2. Create Account")
    print("3. Remove Account")
    print("4. Exit or Quit\n")

    userChoice = input("[*] Enter Your Choice : ")
    if userChoice == '1':
        loginAndGame()
    elif userChoice == '2':
        newUser()
    elif userChoice == '4' or userChoice == '3':
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        print("           Thanks For Passing By!!")
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        sys.exit()
    else:
        print("[!] Error: Enter value from given list")
        input("[*] Press Any Key To Continue")