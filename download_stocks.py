""" Script to download selected stocks from the dictionary.
@author: Tudor Trita
@date: 12/11/2019
"""
symbol_dict = {"Apple": "AAPL",
               "Microsoft": "MSFT",
               "Goldman Sachs": "GS",
               "HSBC Holdings": "HSBC",
               "Banco Santander": "SAN",
               "Barclays PLC": "BCS",
               "Standard Chartered PLC": "STAN.L",
               "J.P. Morgan": "JPM",
               "Bank of America": "BAC",
               "CitiGroup": "C",
               "Morgan Stanley": "MS"}


def start(symbol_list):
    from scraper import ScraperChrome

    scrape_this = ScraperChrome(2)
    for s in symbol_list:
        scrape_this.start(s)
    scrape_this.stop()
    return


if __name__ == "__main__":
    symbol_list = list(symbol_dict.values())
    start(symbol_list)
