from yahoo_fin import stock_info as si
from datetime import datetime
import pandas as pd  
import matplotlib.pyplot as plt


#Main Menu Function that displays main menu and return user input
def mainMenu():
    print("Welcome! Please select one of the following options by entering the corresponding menu number: \
           \n 1. Look up a stock \
           \n 2. View Watchlist \
           \n 3. Today's Top Gainers and Losers \
           \n 4. View The Top 10 Cryptocurrencies \
           \n 5. Quit \n")
    return input()


#Gets stock symbol. Validate symbol Give option to quit
def getStock():
    symbol = input("Please enter stock ticker symbol or enter 'Q' to return to the menu: ")
    while validate(symbol) == False:
        if symbol != 'Q':
            symbol = input("Stock symbol was not found it may have been delisted. Please try again: ")
        else:
            return symbol
    
    return symbol

#Validates the entered symbol
def validate(symbol):
        try: 
            si.get_live_price(symbol)
            return True
        
        except: 
            return False

#Submenu for option 1. 
def subMenu():
    print("Please select one of the following options by entering the corresponding menu number: \
                \n 1. Historical Price Chart \
                \n 2. Volume Chart \
                \n 3. Add to Watchlist \
                \n 4. Update current price \
                \n 5. Previous menu\n") 
    return input()

#Fetches Current Time
def currentTime():
    now = datetime.now()
    return str(now.strftime("%H:%M")) #programiz.com/python-programming/datetime/current-time
    
    
#Plot Function
def plot(stockData, x, y, yLabel):
    stockData = stockData.reset_index()
    plt.plot(stockData[x], stockData[y], 'b-')
    plt.xlabel("Date")
    plt.ylabel(yLabel)
    plt.xticks(rotation = 45)
    plt.grid(True, which = 'major', axis = 'both')
    plt.show()

#Pulls the stock data for given dates
def getStockData(symbol):
    fromDate = input("Please enter the starting date in the form 'yyyy-mm-dd': ")
    toDate = input("Please enter the end date in the form 'yyyy-mm-dd': ")
    return si.get_data(symbol, start_date= fromDate, end_date= toDate)

#Trims a data frame down to the first 10 entries. Also deletes columns based off of list of columns given
def dfTrimmer(dataFrame, deleteData):

    dataFrame = dataFrame.truncate(after = 9)
    for i in range(len(deleteData)):
        del dataFrame[deleteData[i]]
    dataFrame['Ranking'] = pd.Series(range(1,11))

    dataFrame = dataFrame.set_index("Ranking")

    print(dataFrame)


    








def main():
    #Initialize
    userInput = ''
    
    #Program will run until 5 is entered
    while userInput != "5":
        userInput = mainMenu()
        
        #Look up Stock
        if userInput == "1":
            #Initialize
            subSelect = ''
            
            #Get symbol, validate, print current price, opening price, previous close
            symbol = getStock()
            if symbol != 'Q':
                    quoteTable = si.get_quote_table(symbol)
                    print("Current price: $", round(si.get_live_price(symbol),3), " as of", currentTime())
                    print("Opening price: $", quoteTable['Open'], \
                        "\nPrevious closing price: $", quoteTable['Previous Close'])

            #Stay on submenu until 5 is entered 
            while subSelect != '5':
                subSelect = subMenu()
                
                #Get date range and plot historical price
                if subSelect == '1':
                    selection = 'Y'
                    while selection == 'Y':
                        plot(getStockData(symbol), "index" , "close", "Price ($)")
                        selection = input("Would you like to enter a new set of dates? (Y/N) ")       

                #Get date range and plot historical volume    
                if subSelect == '2':
                    selection = 'Y'
                    while selection == 'Y':
                        plot(getStockData(), "index" , "volume", "Volume ")
                        selection = input("Would you like to enter a new set of dates? (Y/N) ")

                #Add stock to a watchlist    
                if subSelect == '3': 
                    columns = ['Name']
                    
                    #Try to open existing watchlist and add stock to it
                    try: 
                        watchlist = pd.read_csv("watchlist.csv", header = 0, delim_whitespace=True)
                        add = pd.DataFrame([symbol], index = None, columns = columns)
                        watchlist = watchlist.append(add, True)
                        watchlist.to_csv('watchlist.csv', index = False)    
                   
                    #Create new watchlist file and add stock to it    
                    except:
                        add = pd.DataFrame([symbol], index = None, columns = columns)
                        add.to_csv('watchlist.csv', index = False)

                    print("This stock has been added to your watchlist\n")

                #Update the live price                
                if subSelect == '4':
                    print("Current price: $", round(si.get_live_price(symbol),3), " as of", currentTime())

        #Print Watchlist
        if userInput == "2":

            #Try to open watchlist. Look up live price for each stock on the list. print the resulting Dataframe
            try: 
                watchlist = pd.read_csv("watchlist.csv", header = 0, delim_whitespace=True)
                npWatchlist = watchlist.to_numpy()
                price = []
                for i in range(0,len(npWatchlist)):
                    price.append(round(si.get_live_price(npWatchlist[i][0]),3)) 
                
                watchlist['price'] = price
                watchlist = watchlist.set_index('Name')
                print(watchlist)
                
            #Error message if watchlist does not exist
            except:
                print("Watchlist is currently empty. Feel free to add stocks to your watchlist under the Look up Stock option in the main menu")

        
        #Prints top 10 gainers and losers
        if userInput == "3":  #Gainers Losers
            gainers = si.get_day_gainers()
            deleteData = ['Change','Volume', 'Avg Vol (3 month)', 'Market Cap', 'PE Ratio (TTM)']
            print("Top Gainers\n")
            dfTrimmer(gainers,deleteData)

            losers = si.get_day_losers()
            print("\nTop Losers\n")
            dfTrimmer(losers, deleteData)
        
        #Prints top 10 crypto by market cap
        if userInput == "4":
            crypto = si.get_top_crypto()
            delete = ["Market Cap", "Volume in Currency (Since 0:00 UTC)", 'Volume in Currency (24Hr)','Total Volume All Currencies (24Hr)', 'Circulating Supply']
            print("The top 10 Cryptocurrencies by Market Cap:")
            dfTrimmer(crypto,delete)

        #If user enters invalid input                                                                                                                 
        elif userInput != '5' and userInput != '1' and userInput != '2' and userInput != '3' and userInput != '4':
            print("Selection not recognized try again")

       

main()