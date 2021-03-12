import requests
from bs4 import BeautifulSoup
import time

URL_LTC = 'https://pokur.su/ltc/rub/1/'
URL_DOGE = 'https://pokur.su/doge/rub/1/'
URL_BIT = 'https://pokur.su/btc/rub/1/'


def park(url):
    full_page = requests.get(url)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    factor = soup.findAll("span", {"class": "pretty-sum"})
    factor = factor[1].text
    factor = factor.replace(',', '.')
    factor = float(factor)
    time.sleep(0.5)
    return factor


doge_factor = park(URL_DOGE)
ltc_factor = park(URL_LTC)
bit_factor = park(URL_BIT)

Lite = {'name': 'LTC', 'currency': ' LTC', 'bot': 'LTC Click Bot', 'cb': 'Litecoin_click_bot',
        'l_minimum_withdraw': 0.0003, 'transfer': ltc_factor}
Doge = {'name': 'DOGE', 'currency': ' DOGE', 'bot': 'DOGE Click Bot', 'cb': 'Dogecoin_click_bot',
        'l_minimum_withdraw': 2, 'transfer': doge_factor}
Bit = {'name': 'BTC', 'currency': ' BTC', 'bot': 'BTC Click Bot', 'cb': 'BitcoinClick_bot',
       'l_minimum_withdraw': 0.00005, 'transfer': bit_factor}

coin = {'d': Doge, 'l': Lite, 'b': Bit}

b = 'b'
d = 'd'
l = 'l'
name = 'name'
currency = 'currency'
bot = 'bot'
cb = 'cb'
t = 'transfer'
l_minimum = 'l_minimum_withdraw'
