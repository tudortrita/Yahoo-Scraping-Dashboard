""" Script to download selected stocks from the dictionary.
@author: Tudor Trita
@date: 11/11/2019
"""

symbol_dict = {"GS": "Goldman Sachs",
               "JPM": "J.P. Morgan",
               "BAC": "Bank of America",
               "C": "CitiGroup",
               "MS": "Morgan Stanley"}


def start(symbol_list):
    from scraper import ScraperChrome

    scrape_this = ScraperChrome(2)

    for s in symbol_list:
        scrape_this.start(s)

    scrape_this.stop()
    return


if __name__ == "__main__":
    symbol_list = list(symbol_dict.keys())
    start(symbol_list)
