import sqlite3
import time
from telethon import TelegramClient
from telethon import sync, events
import re
import json
import dictionary as d


def check_float(some):
    try:
        some = float(some)
        return some
    except:
        print('Нужно ввести число')


def login(x):
    cur.execute(f"SELECT PHONE FROM account WHERE ID = '{x}'")
    time.sleep(0.1)
    global Phone
    Phone = str(cur.fetchone()[0])
    print("Входим в аккаунт: " + Phone)
    cur.execute(f"SELECT API_ID FROM account WHERE ID = '{x}'")
    time.sleep(0.1)
    api_id = str(cur.fetchone()[0])
    cur.execute(f"SELECT API_HASH FROM account WHERE ID = '{x}'")
    time.sleep(0.1)
    api_hash = str(cur.fetchone()[0])
    session = str("anon" + str(x))
    global client
    client = TelegramClient(session, api_id, api_hash)
    client.start()


def withdraw(bot, client):
    result = 'Произвести вывод c ' + d.coin[bot][d.name] + ' невозможно.'
    dlgs = client.get_dialogs()
    for dlg in dlgs:
        if dlg.title == d.coin[bot][d.bot]:
            tegmo = dlg

    client.send_message(d.coin[bot][d.bot], "/balance")
    time.sleep(3)
    msgs = client.get_messages(tegmo, limit=1)

    currency = d.coin[bot][d.currency]

    for mes in msgs:
        str_a = str(mes.message)
        zz = str_a.replace('Available balance: ', '')
        print(zz)
        if bot == d.b:
            n = zz.find(d.coin[d.b][d.currency])
            zz = zz[0:n]
        else:
            zz = zz.replace(currency, '')
        waitin = float(zz)

        if (bot == 'l' and waitin >= d.coin['l'][d.l_minimum])\
                or (bot == 'd' and waitin >= d.coin['d'][d.l_minimum])\
                or (bot == 'b' and waitin >= d.coin['b'][d.l_minimum]):
            client.send_message(d.coin[bot][d.bot], "💵 Withdraw")
            time.sleep(3)
            if bot == 'l':
                cur.execute(f"SELECT LITECOIN FROM account WHERE ID = '{x}'")
            elif bot == 'd':
                cur.execute(f"SELECT DOGECOIN FROM account WHERE ID = '{x}'")
            time.sleep(0.4)
            purse = str(cur.fetchone()[0])
            client.send_message(d.coin[bot][d.bot], purse)
            ans = input('Нажмите Enter, чтобы снять всё, или введите сумму для вывода...\n')
            ans = check_float(ans)
            if ans != '':
                waitin = ans

            trans = round(float(waitin), 5)
            # Eva = float(Adolf) - 0.00001
            print("Выводим: " + str(trans))
            time.sleep(3)
            client.send_message(d.coin[bot][d.bot], str(trans))
            time.sleep(3)
            client.send_message(d.coin[bot][d.bot], "✅ Confirm")
            time.sleep(3)
            client.send_message(d.coin[bot][d.bot], "🏠 Menu")
            time.sleep(3)
            result = 'Успех!'
        else:
            print('Средств для вывода не хватает!')
    print(result)
    return result


db = sqlite3.connect('account.db')
cur = db.cursor()

cur.execute(f"SELECT COUNT(*) FROM account")
time.sleep(0.1)
h = int(cur.fetchone()[0])
x = h - (h - 1)

ltc = 'l'
doge = 'd'
btc = 'b'

while True:
    login(x)

    withdraw1 = withdraw(ltc, client)
    withdraw2 = withdraw(doge, client)
    withdraw3 = withdraw(btc, client)


    # cur.execute(f"SELECT PHONE FROM Account WHERE ID = '{x}'")
    # time.sleep(0.1)
    # Phone = str(cur.fetchone()[0])
    # print("Входим в аккаунт: " + Phone)
    # cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{x}'")
    # time.sleep(0.1)
    # api_id = str(cur.fetchone()[0])
    # cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{x}'")
    # time.sleep(0.1)
    # api_hash = str(cur.fetchone()[0])
    # session = str("anon" + str(x))
    # client = TelegramClient(session, api_id, api_hash)
    # client.start()

    # dlgs = client.get_dialogs()
    # for dlg in dlgs:
    #     if dlg.title == 'LTC Click Bot':
    #         tegmo = dlg
    #
    # client.send_message('LTC Click Bot', "/balance")
    # time.sleep(3)
    # msgs = client.get_messages(tegmo, limit=1)
    #
    # for mes in msgs:
    #     str_a = str(mes.message)
    #     zz = str_a.replace('Available balance: ', '')
    #     qq = zz.replace(' LTC', '')
    #     print(qq)
    #     waitin = float(qq)
    #
    #     if waitin >= 0.0004:
    #         client.send_message('LTC Click Bot', "💵 Withdraw")
    #         time.sleep(3)
    #         cur.execute(f"SELECT LITECOIN FROM Account WHERE ID = '{x}'")
    #         time.sleep(0.4)
    #         litecoin = str(cur.fetchone()[0])
    #         client.send_message('LTC Click Bot', litecoin)
    #         Adolf = round(waitin, 5)
    #         Eva = float(Adolf) - 0.00001
    #         vivod = float(Eva)
    #         print("Выводим: " + str(vivod))
    #         time.sleep(3)
    #         client.send_message('LTC Click Bot', str(vivod))
    #         time.sleep(3)
    #         client.send_message('LTC Click Bot', "✅ Confirm")
    #         time.sleep(3)
    #         client.send_message('LTC Click Bot', "🏠 Menu")
    #         time.sleep(3)
    if x == h:
        print("Конец")
        break
    x = x + 1
    time.sleep(1)
