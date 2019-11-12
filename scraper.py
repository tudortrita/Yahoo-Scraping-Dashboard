""" Program to scrape stocks from Yahoo Finance (Works as of 12/11/2019)
using selenium.
@author: Tudor Trita
@date: 12/11/2019
"""
from selenium import webdriver
from datetime import datetime
from urllib.parse import urlparse
from urllib.parse import parse_qs
import time
import os
import pandas as pd


class ScraperChrome():
    def __init__(self, timeout):
        self.timeout = timeout
        options = webdriver.ChromeOptions()
        self.data_path = os.path.join(os.getcwd(), "data")
        options.add_argument('headless')
        options.add_experimental_option("prefs", {
            "download.default_directory": self.data_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        self.browser = webdriver.Chrome(options=options)
        self.cookie = None
        try:
            print("Getting browser consent:")
            self.get_browser_consent()
            print("OK")
        except:
            "Browser consent could not be done at this time."

    def start(self, symbol):
        self.symbol = symbol
        print(f"Data for symbol {symbol}")
        self.grab_historical_data()
        self.grab_financials()

    def stop(self):
        self.browser.quit()

    def get_browser_consent(self):
        self.browser.get("https://consent.yahoo.com/consent")
        time.sleep(self.timeout)
        self.browser.get(self.browser.current_url)
        time.sleep(self.timeout)
        self.browser.find_element_by_xpath(".//*[@value='agree']").click()
        print("Got browser consent")

    def grab_historical_data(self):
        for i in range(10):
            if not self.cookie:
                print(f"Getting cookie: attempt {i + 1}")
                self.get_historical_cookie()
            else:
                break
        assert self.cookie, "Cookie not acquired"
        print("Got cookie, proceeding to download")
        file_name = f"{self.symbol}.csv"
        period_end = 2000000000
        url_history = f"https://query1.finance.yahoo.com/v7/finance/download/{self.symbol}?period1=0&period2={period_end}&interval=1d&events=history&crumb={self.cookie}"
        self.browser.get(url_history)
        print(f"Downloaded data for symbol {self.symbol}")
        time.sleep(self.timeout)

    def get_historical_cookie(self):
        cookie_url = f"https://finance.yahoo.com/quote/{self.symbol}/history?period1=0&period2=2000000000&interval=1d&filter=history&frequency=1d"
        self.browser.get(cookie_url)
        time.sleep(self.timeout)
        el = self.browser.find_element_by_xpath("// a[. // span[text() = 'Download Data']]")
        link = el.get_attribute("href")
        a = urlparse(link)
        self.cookie = parse_qs(a.query)["crumb"][0]

    def grab_financials(self):
        df = pd.DataFrame(columns=['Total Revenue', 'Gross Profit', 'Total Operating Expenses', 'Net Income', 'EBITDA'])
        url_financials = f"https://finance.yahoo.com/quote/{self.symbol}/financials?p={self.symbol}"
        self.browser.get(url_financials)
        time.sleep(self.timeout)

        # Begin scraping data
        print("Scraping Financials")
        dates = self.browser.find_element_by_xpath("""//*[@id="Col1-1-Financials-Proxy"]/section/div[4]/div[1]/div[1]/div[1]/div""").text

        if len(dates) == 53:
            dates = ["TTM", dates[13:23], dates[23:33], dates[33:43], dates[43:53]]
        elif len(dates) == 49:
            dates = ["TTM", dates[13:22], dates[22:31], dates[31:40], dates[40:49]]

        # Loading data
        total_revenue = self.browser.find_element_by_xpath(r"""//*[@id="Col1-1-Financials-Proxy"]/section/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]""").text.split(" ")[1:]
        gross_profit = self.browser.find_element_by_xpath(r"""//*[@id="Col1-1-Financials-Proxy"]/section/div[4]/div[1]/div[1]/div[2]/div[3]/div[1]""").text.split(" ")[1:]
        total_operating_expenses = self.browser.find_element_by_xpath(r"""//*[@id="Col1-1-Financials-Proxy"]/section/div[4]/div[1]/div[1]/div[2]/div[4]/div[2]/div[3]/div[1]""").text.split(" ")[2:]
        net_income = self.browser.find_element_by_xpath("""//*[@id="Col1-1-Financials-Proxy"]/section/div[4]/div[1]/div[1]/div[2]/div[11]/div[1]""").text.split(" ")[1:]
        EBITDA = self.browser.find_element_by_xpath("""//*[@id="Col1-1-Financials-Proxy"]/section/div[4]/div[1]/div[1]/div[2]/div[15]/div[1]""").text.split(" ")

        total_revenue[0] = total_revenue[0].split("\n")[-1]
        gross_profit[0] = gross_profit[0].split("\n")[-1]
        total_operating_expenses[0] = total_operating_expenses[0].split("\n")[-1]
        net_income[0] = net_income[0].split("\n")[-1]
        EBITDA[0] = EBITDA[0].split("\n")[-1]

        for i, d in enumerate(dates):
            df.loc[d] = [total_revenue[i], gross_profit[i], total_operating_expenses[i], net_income[i], EBITDA[i]]

        df.to_csv(os.path.join(self.data_path, f"{self.symbol}_financials.csv"))
        print("Finished scraping financials")


if __name__ == "__main__":
    symbol = input("Please Input the ticker:")
    timeout = 2
    scrape = ScraperChrome(timeout)
    scrape.start(symbol)
    scrape.stop()
