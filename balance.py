import sqlite3
import time
from telethon import TelegramClient
from telethon import sync, events
import re
import json
import dictionary as d


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


def balance(bot, client):
    global num
    COIN_name = d.coin[bot]['bot']
    dlgs = client.get_dialogs()
    for dlg in dlgs:
        if dlg.title == COIN_name:
            tegmo = dlg

    try:
        client.send_message(COIN_name, "/balance")
        time.sleep(1)
        msgs = client.get_messages(tegmo, limit=1)

        currency = d.coin[bot][d.currency]

        for mes in msgs:
            str_a = str(mes.message)
            qq = str_a.replace('Available balance: ', '')
            print(qq)
            if bot == d.b:
                n = qq.find(d.coin[d.b][d.currency])
                qq = qq[0:n]
            else:
                qq = qq.replace(currency, '')
            num = float(qq)
    except Exception as e:
        print(e)
        num = 0

    return num


num = 0

db = sqlite3.connect('account.db')
cur = db.cursor()

cur.execute(f"SELECT COUNT(*) FROM account")
h = int(cur.fetchone()[0])  # получаем кол-во записей в БД (на всякий случай обозначил тип)

x = h - (h - 1)
m = 0

SUM_LTC = 0
SUM_DOGE = 0
SUM_BTC = 0
SUM_RUB = 0

while True:
    login(x)  # логинимся и далее действуем от этого логина
    time.sleep(0.1)
    LTC = balance(d.l, client)
    time.sleep(0.5)
    DOGE = balance(d.d, client)
    time.sleep(0.5)
    BTC = balance(d.b, client)
    RUB = (LTC * d.coin[d.l][d.t]) + (DOGE * d.coin[d.d][d.t] + (BTC * d.coin[d.b][d.t]))
    print(str(RUB) + " RUB\n")

    SUM_BTC = SUM_BTC + BTC
    SUM_LTC = SUM_LTC + LTC
    SUM_DOGE = SUM_DOGE + DOGE
    SUM_RUB = SUM_RUB + RUB

    time.sleep(0.5)

    if x == h:
        break
    x = x + 1


# SUM_RUB = (SUM_LTC * d.coin[d.l][d.t]) + (SUM_DOGE * d.coin[d.d][d.t] + (SUM_BTC * d.coin[d.b][d.t]))
time.sleep(0.1)
print("Всего на всех аккаунтах при нынешнем курсе ("
      + str(d.coin[d.l][d.t]) + ' RUB за 1' + d.coin[d.l][d.currency] + ', '
      + str(d.coin[d.d][d.t]) + ' RUB за 1' + d.coin[d.d][d.currency] + ', '
      + str(d.coin[d.b][d.t]) + ' RUB за 1' + d.coin[d.b][d.currency] +
      ") имеется:\n" + str(round(SUM_RUB, 2)) + " Рублей")
