#!/usr/bin/python

import datetime as dt

import yfinance as yf
import plotext as plt

from colorama import Fore

"""

DATA INPUT AND ESSENTIAL FUNCTIONS

"""

def print_colors(color_value, color_text):
    return{
        'red'    : lambda: print(Fore.RED    + color_text, Fore.WHITE),
        'green'  : lambda: print(Fore.GREEN  + color_text, Fore.WHITE),
        'yellow' : lambda: print(Fore.YELLOW + color_text, Fore.WHITE)
    }.get(color_value)()

def ticker_input():
    print_colors("yellow", "IF USING A CRYPTO '-USD' MUST BE ADDED AT THE END OF THE TICKER (IE: BTC-USD).")
    ticker_input.ticker_value = input("Ticker:\n")
    ticker_input.ticker_value.lower()

"""

DATA GATHERING USING YAHOO FINANCE

"""

def ticker_info():
    stock = yf.Ticker(ticker_input.ticker_value).info
    #this is needed for the market price and the previous close price

    market = yf.Ticker(ticker_input.ticker_value)
    #this is needed for the quarterly financial data and the dividend data

    ticker_info.market_price = stock['regularMarketPrice']
    ticker_info.previous_close_price = stock['regularMarketPreviousClose']
    ticker_info.quarterly_financial_data = market.quarterly_financials
    ticker_info.dividend_data = market.dividends


"""

DISPLAY FINANCIAL DATA

"""


def print_quarterly_data():
    print_colors("red", "QUARTERLY FINANCIAL DATA FOR TICKER ")
    print_colors("green", ticker_input.ticker_value.upper())
    print(ticker_info.quarterly_financial_data, '\n')

def print_div_data():
    print_colors("red", "DIVIDEND DATA FOR TICKER ")
    print_colors("green", ticker_input.ticker_value.upper())
    print(ticker_info.dividend_data, '\n')

def show_values():
    print_colors("red", "VALUES PRINTED FOR TICKER ")
    print_colors("green", ticker_input.ticker_value.upper())
    
    print('market:', ticker_info.market_price)
    print('previous close:', ticker_info.previous_close_price, '\n')

    #i'm sure there's a more efficient way to do this...

    if (len(ticker_info.quarterly_financial_data) == 0 and len(ticker_info.dividend_data) == 0):
        print("NO QUARTERLY FINANCIAL DATA OR DIVIDEND DATA FOR THE GIVEN TICKER \n")

    if(len(ticker_info.quarterly_financial_data) == 0):
        print("NO QUARTERLY FINANCIAL DATA FOR THE GIVEN TICKER \n")
        print_div_data()
    elif(len(ticker_info.dividend_data) == 0):
        print("NO DIVIDEND DATA FOR THE GIVEN TICKER \n")
        print_quarterly_data()
    else:
        print_quarterly_data()
        print_div_data()
    

"""

DISPLAY A GRAPH OF THE GIVEN TICKER

"""


def make_plot():

    make_plot_yn = input("make plot (y/n)? \n")

    if (make_plot_yn == "y" or make_plot_yn == "yes"):

        # set plot date format and time variables
        plt.date_form('d/m/Y')
        current_date = dt.date.today()
        current_day = str(current_date.day)
        current_month = str(current_date.month)
        current_year = str(current_date.year)

        # set start and end dates for plot, grab data from web

        date_in = input("date to start from (dd/mm/yy)? if left blank the date will be the first of the year. \n")
        date_in_end = input("date to end from (dd/mm/yy)? if left blank the current day will be used. \n")

        if (len(date_in) == 0):
            date_in = '01/01/{}'.format(current_year)
        if (len(date_in_end) == 0):
            date_in_end = '{}/{}/{}'.format(current_day, current_month, current_year)

        start = plt.string_to_datetime(date_in)
        end = plt.string_to_datetime(date_in_end)
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
