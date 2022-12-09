import csv
from datetime import datetime

from trade_plate.tools.constants import PORTFOLIO

import matplotlib.pyplot as plt

# ['Date', 'Type', 'Buy Amount', 'Currency', 'Sell Amount', 'Currency',
# 'Fee Amount', 'Currency', 'Exchange', 'Comment', 'Deduct']


class CURRENCIES:
    BTC = "BTC"
    ETH = "ETH"
    NEAR = "NEAR"
    MINA = "MINA"
    GRT = "GRT"
    USD = "USD"


btc_portfolio = []
eth_portfolio = []
near_portfolio = []
mina_portfolio = []
grt_portfolio = []
with open(PORTFOLIO.PATH, newline="") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=",")

    for row in csv_reader:
        if (row[3] == CURRENCIES.BTC and row[5] == CURRENCIES.USD) or (
            row[3] == CURRENCIES.USD and row[5] == CURRENCIES.BTC
        ):
            btc_portfolio.append(row)
        if (row[3] == CURRENCIES.ETH and row[5] == CURRENCIES.USD) or (
            row[3] == CURRENCIES.USD and row[5] == CURRENCIES.ETH
        ):
            eth_portfolio.append(row)
        if (row[3] == CURRENCIES.NEAR and row[5] == CURRENCIES.USD) or (
            row[3] == CURRENCIES.USD and row[5] == CURRENCIES.NEAR
        ):
            near_portfolio.append(row)
        if (row[3] == CURRENCIES.MINA and row[5] == CURRENCIES.USD) or (
            row[3] == CURRENCIES.USD and row[5] == CURRENCIES.MINA
        ):
            mina_portfolio.append(row)
        if (row[3] == CURRENCIES.GRT and row[5] == CURRENCIES.USD) or (
            row[3] == CURRENCIES.USD and row[5] == CURRENCIES.GRT
        ):
            grt_portfolio.append(row)


def summary(portfolio: list):
    buy_cost: float = 0
    buy_amount: float = 0
    sell_cost: float = 0
    sell_amount: float = 0
    for row in portfolio:
        date_time = datetime.strptime(row[0], "%m/%d/%Y %H:%M:%S")
        if date_time > datetime(2022, 9, 13):
            if row[1] == "Buy":
                buy_amount += float(row[2])
                buy_cost += float(row[4])
            elif row[1] == "Sell":
                sell_amount += float(row[4])
                sell_cost += float(row[2])
            else:
                print(f"Unknown type: {row[1]}")

    return buy_cost, buy_amount


def show(cost, amount):
    print(f"Cost: {cost}\nAmount: {amount}\nAverage: {(cost) / (amount)}")


total_cost = 0
sizes = []

print("BTC")
cost, amount = summary(btc_portfolio)
total_cost += cost
sizes.append(cost)
show(cost, amount)
print("-------------------")
print("ETH")
cost, amount = summary(eth_portfolio)
total_cost += cost
sizes.append(cost)
show(cost, amount)
print("-------------------")
print("NEAR")
cost, amount = summary(near_portfolio)
total_cost += cost
sizes.append(cost)
show(cost, amount)
print("-------------------")
print("MINA")
cost, amount = summary(mina_portfolio)
total_cost += cost
sizes.append(cost)
show(cost, amount)
print("-------------------")
print("GRT")
cost, amount = summary(grt_portfolio)
total_cost += cost
sizes.append(cost)
show(cost, amount)
print("-------------------")
print(f"Total Cost: {total_cost}")

labels = (
    CURRENCIES.BTC,
    CURRENCIES.ETH,
    CURRENCIES.NEAR,
    CURRENCIES.MINA,
    CURRENCIES.GRT,
)
explode = (0, 0, 0, 0, 0)

fig1, ax1 = plt.subplots()
ax1.pie(
    sizes, explode=explode, labels=labels, autopct="%1.1f%%", shadow=True, startangle=90
)
ax1.axis("equal")

plt.show()
