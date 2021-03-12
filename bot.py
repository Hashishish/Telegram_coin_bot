# v2.1.1 (by v1a0, edited by Hashishish)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telethon import sync, events
import requests
import json
import hashlib
import time
import re
from telethon import TelegramClient
import webbrowser
import urllib.request
import os
import sqlite3
import logging
import dictionary as d
from threading import Thread



logging.basicConfig(filename='coinbot1.log', filemode='a', format='%(asctime)s :: %(lineno)d :: %(message)s', level=logging.WARNING)
# logging.basicConfig(format='%(asctime)s :: %(lineno)d :: %(message)s', level=logging.WARNING)

# sqlite3.connect('Account.db') -> sqlite3.connect('Accounts.db')

log_phrases = {
    'get_accs_list':            'Getting accounts list from DB...',
    'acc_initialization':       'Initializing new account...',
    'mining':                   'Mining started...',
    'stat_upd_for_notify_bot':  'Updating status for notify_bot...',
    'get_main_dialog':          'Looking for a main dialog...',
    'start_message':            'Sending start message...',
    'get_last_msg_str':         'Getting last message as str...',
    'make_tasks':               'Starting tasks making...',
    'select_reactor':           'Selecting reactor...',
}


def autolog(func):
    phrase = log_phrases.get(f'{func.__name__}')
    if phrase is None:
        phrase = f'Function {func.__name__} in process...'

    def wrapper(*args, **kwargs):
        print(f'{phrase} ({func.__name__})')
        func(*args, **kwargs)
        print(f'Done. ({func.__name__})')

    return wrapper

def main():
    class Controller:
        def __init__(self):
            self.accounts_list = []
            self.done_counter = 0
            self.sorry_counter = 0
            self.main_dialog = False
            self.account_id = ''
            self.phone = ''
            self.api_id = 0
            self.api_hash = ''
            self.session = ''
            self.main_dialog = False
            self.sleep_after_start = 20

        @autolog
        def get_accounts_list(self):
            db = sqlite3.connect('account.db')
            cursor = db.cursor()
            cursor.execute("SELECT * FROM account")
            rows = cursor.fetchall()
            _list = []

            for row in rows:
                _list.append(
                    {
                        'id': row[0],
                        'phone': row[1],
                        'pass': row[2],
                        'api_id': row[3],
                        'api_hash': row[4],
                    }
                )

            #            self.accounts_list = _list[42:]
            self.accounts_list = _list

        @autolog
        def account_initialization(self, account):
            self.done_counter = 0
            self.sorry_counter = 0
            self.main_dialog = False
            self.account_id = account.get('id')
            self.phone = account.get('phone')
            self.api_id = account.get('api_id')
            self.api_hash = account.get('api_hash')
            self.session = f"anon{self.account_id}"

        @autolog
        def stat_upd_for_notify_bot(self):
            status_file = open('queue.tmp', 'w')
            status_file.write(f"{self.account_id}")
            status_file.close()

        def login_bot(self):
            print(f"\n\n\nLogging as: {self.phone} (bot {self.account_id})\n")
            self.client = TelegramClient(self.session, self.api_id, self.api_hash)
            self.client.start()

        @autolog
        def get_main_dialog(self, bot_name):
            # ?????????????????????????
            self.main_dialog = False
            for dialog in self.client.get_dialogs():
                if dialog.title == bot_name:
                    self.main_dialog = dialog

        @autolog
        def start_message(self, bot_name):
            print("Time to sleep: {time_set}+2 ({realtime}) sec".format(
                time_set=self.sleep_after_start,
                realtime=self.sleep_after_start+2
            ))

            self.client.send_message(bot_name, "/menu")
            time.sleep(2)
            self.client.send_message(bot_name, "🖥 Visit sites")
            time.sleep(self.sleep_after_start)

        @autolog
        def get_last_msg_str(self, cb):
            #self.last_msg_str = self.client.get_messages(self.main_dialog)[0].message
            time.sleep(3)
            self.last_msg_str = self.client.get_messages(cb, limit=2)[0].message
            print(f'Message is: \n{self.last_msg_str}')

        @autolog
        def get_previous_msg_str(self, cb):
            try:
                time.sleep(3)
                self.previous_msg_str = self.client.get_messages(cb, limit=2)[1].message
                print(f'PRE-Message is: \n{self.previous_msg_str}')

            except Exception as e:
                print(e)
                self.previous_msg_str = ''

        @autolog
        def sorry_reactor(self, bot_name):
            self.start_message(bot_name)
            self.sorry_counter += 1

        @autolog
        def skip_task(self, bot_name, cb):
            self.client.send_message(bot_name, "/visit")
            time.sleep(3)
            msgs_2 = self.client.get_messages(cb)
            self.skip_message_id = msgs_2[0].id
            self.skip_button_data = msgs_2[0].reply_markup.rows[1].buttons[1].data

            from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
            self.client(GetBotCallbackAnswerRequest(
                bot_name,
                self.skip_message_id,
                data=self.skip_button_data
            ))
            time.sleep(2)

        @autolog
        def get_time_to_wait(self):
            try:
                if re.search(r'seconds to get your reward', self.last_msg_str):
                    self.time_to_wait = int(re.search(r'\d+', self.last_msg_str).group())
                else:
                    self.time_to_wait = 4

            except Exception as e:
                self.time_to_wait = 30
                print(e)

        @autolog
        def calculate_profit(self):
            try:
                profit = 0
                with open('profit_', 'r') as profit_file:
                    for line in profit_file.readlines():
                        profit = float(line)

                new_money = float(re.search(r'\d+.\d+', self.previous_msg_str[:45]).group())
                new_profit = float(profit + new_money)

                print('\n'
                      f'money: {"{0:.8f}".format(new_money)}\n'
                      f'had__: {"{0:.8f}".format(profit)}\n'
                      f'itog_: {"{0:.8f}".format(new_profit)}\n')

                with open('profit_', 'w') as profit_file:
                    profit_file.write(f'{"{0:.8f}".format(new_profit)}')



            except Exception as e:
                print(e)

        @autolog
        def chrome_test(self):
            print(f'Time to wait: {self.time_to_wait}')
            selenium_url = "http://localhost:4444/wd/hub"
            caps = {'browserName': 'chrome'}
            driver = webdriver.Remote(command_executor=selenium_url, desired_capabilities=caps)
            driver.maximize_window()
            driver.get(self.adw_url)
            time.sleep(self.time_to_wait + 10 if self.time_to_wait > 4 else 4)
            driver.close()
            driver.quit()

        @autolog
        def chrome_reactor(self, bot_name):
            self.client.send_message(bot_name, "/visit")
            time.sleep(3)

            try_counter = 0

            while try_counter < 2:
                try:
                    self.chrome_test()
                    break
                except Exception as e:
                    print('\n         Chrome crushed (' + str(try_counter) + ')')
                    print(e)
                    try_counter += 1


        @autolog
        def req_reactor(self, bot_name, cb):
            self.previous_msg_str = ''
            self.client.send_message(bot_name, "/visit")
            time.sleep(3)

            self.get_last_msg_str(cb)
            msgs_2 = self.client.get_messages(cb, limit=2)
            self.adw_url = msgs_2[0].reply_markup.rows[0].buttons[0].url

            self.get_time_to_wait()
            self.chrome_reactor(bot_name)

            print('\nWaiting for an answer...')

            self.get_last_msg_str(cb)
            if re.search(r'stay on the site for at', self.last_msg_str):
                temp_req = requests.get(self.adw_url).json
                time.sleep(5)
                self.get_last_msg_str(cb)

            if re.search(r'seconds to get your reward', self.last_msg_str):
                self.get_time_to_wait()
                self.chrome_reactor(bot_name)

            self.get_previous_msg_str(cb)
            if re.search(r'You earned', self.previous_msg_str):
                self.done_counter += 1
                self.calculate_profit()
                return print('Task done! Ez-pz!')

            if re.search(r'Sorry, there are no new ads available', self.last_msg_str):
                self.done_counter += 1
                return print('Task done! Ez-pz!')

            else:
                self.skip_task(bot_name, cb)
                return print('Task skipped')


        @autolog
        def select_reactor(self, bot_name, cb):
            self.get_last_msg_str(cb)

            if re.search(r'Sorry, there are no new ads available.', self.last_msg_str):
                self.sorry_reactor(bot_name)

            # elif re.search(r'\bseconds to get your reward\b', self.last_msg_str):
            #    self.chrome_reactor()

            else:
                self.req_reactor(bot_name, cb)

        @autolog
        def make_tasks(self, bot_name, cb):
            while True:
                print(f"Bot {self.account_id} has DONE {self.done_counter} tasks")

                if self.sorry_counter == 2:
                    print("Have no ads 2 times")
                    print("Moving to the next account")
                    break

                elif self.done_counter == 16:
                    print("Moving to the next account")
                    break

                else:
                    self.select_reactor(bot_name, cb)

        @autolog
        def mining(self, bot_name, cb):
            self.get_accounts_list()

            if self.accounts_list:
                for account in self.accounts_list:
                    try:
                        self.account_initialization(account)
                        time.sleep(0.2)
                        self.stat_upd_for_notify_bot()
                        time.sleep(0.2)
                        self.login_bot()
                        time.sleep(0.2)
                        self.get_main_dialog(bot_name)
                        time.sleep(0.2)
                        if not bool(self.main_dialog):
                            print(f'{self.phone} (bot {self.account_id}) HAVE NO LITECOIN BOT!!!')
                            break

                        else:
                            self.start_message(bot_name)
                            time.sleep(0.2)
                            self.get_last_msg_str(cb)

                            if self.last_msg_str != "🖥 Visit sites":
                                self.make_tasks(bot_name, cb)

                            else:
                                print("Didn't get an answer for a start_message()")

                    except Exception as e:
                        print(f'\n\n WE ARE DOWN \nError: {e}')
                        pass

                time.sleep(3)
            else:
                print('No accounts list is empty')




    DOGE = Controller()
    DOGE_t = Thread(target=DOGE.mining(d.coin[d.d][d.bot], d.coin[d.d][d.cb]))
    LTC = Controller()
    LTC_t = Thread(target=LTC.mining(d.coin[d.l][d.bot], d.coin[d.l][d.cb]))
    BTC = Controller()
    # BTC_t = Thread(target=BTC.mining(d.coin[d.b][d.bot], d.coin[d.b][d.cb]))
    DOGE_t.start()
    LTC_t.start()
    DOGE_t.join()
    LTC_t.join()
    # for i in range(3):
    #     # DOGE.mining(d.coin[d.d][d.bot], d.coin[d.d][d.cb])
    #     # LTC.mining(d.coin[d.l][d.bot], d.coin[d.l][d.cb])
    #     # BTC.mining(d.coin[d.b][d.bot], d.coin[d.b][d.cb])
    #
    #     time.sleep(30)

if __name__ == '__main__':
    print('''
    #===================================#
    #===================================#
    #===================================#
    ''')
    main()
