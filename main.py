#!/usr/bin/python

# core import
import datetime as dt

# external import
import yfinance as yf
import plotext as plt

# from import
from colorama import Fore

def ticker_input():
    print('\n', Fore.YELLOW + 'IF USING A CRYPTO "-USD" MUST BE ADDED AT THE END OF THE TICKER (IE: BTC-USD).', Fore.WHITE, '\n')
    ticker_input.ticker_value = input("Ticker:\n")
    ticker_input.ticker_value.lower()

def ticker_info():
    stock = yf.Ticker(ticker_input.ticker_value).info
    #this is needed for the market price and the previous close price

    market = yf.Ticker(ticker_input.ticker_value)
    #this is needed for the quarterly financial data and the dividend data

    ticker_info.market_price = stock['regularMarketPrice']
    ticker_info.previous_close_price = stock['regularMarketPreviousClose']
    ticker_info.finance = market.quarterly_financials
    ticker_info.dividends = market.dividends

def show_values():
    print(Fore.RED + '\nVALUES PRINTED FOR TICKER', Fore.GREEN, ticker_input.ticker_value, Fore.WHITE)
    print('market:', ticker_info.market_price)
    print('previous close:', ticker_info.previous_close_price, '\n')

    if (len(ticker_info.finance) == 0 and len(ticker_info.dividends) == 0):
        print(Fore.RED + 'NO QUARTERLY FINANCIAL OR DIVIDEND DATA FOR', Fore.GREEN, ticker_input.ticker_value, Fore.WHITE, '\n')
    else:
        print(Fore.RED + 'QUARTERLY FINANCIAL DATA FOR', Fore.GREEN, ticker_input.ticker_value, Fore.WHITE)
        print(ticker_info.finance, '\n')
        print(Fore.RED + 'DIVIDEND DATA FOR', Fore.GREEN, ticker_input.ticker_value, Fore.WHITE)
        print(ticker_info.dividends, '\n')

def make_plot():

    make_plot_yn = input("make plot (y/n)? \n")

    if (make_plot_yn == "y" or make_plot_yn == "yes"):

        # set plot date format and time variables
        plt.date_form('d/m/Y')
        current_date = dt.date.today()
        current_year = current_date.year

        # I'm sure there's a much more efficient way to do this...
        str(current_year)

        # set start and end dates for plot, grab data from web

        date_in = input("date to start from (dd/mm/yy)? if left blank the date will be the first of the year.\n")

        if (len(date_in) == 0):
            date_in = '01/01/{}'.format(current_year)

        start = plt.string_to_datetime(date_in)
        end = plt.today_datetime()
        data = yf.download(ticker_input.ticker_value, start, end)

        # set pricing and date variables
        prices = list(data["Close"])
        dates = plt.datetimes_to_string(data.index)

        # generate the plot
        plt.plot(dates, prices)

        # set up cosmetics and display of the plot
        plt.title(ticker_input.ticker_value + " stock price")
        plt.ticks_color('red')
        plt.ticks_style('bold')
        plt.xlabel("Date")
        plt.plotsize(100, 30)
        plt.show()
    else:
        print("okay")

# the existence of this function is to make the code more easily readable to people who are deciding to edit the program
def main():
    ticker_input()
    ticker_info()
    show_values()
    make_plot()

main()
