import csv
import json
from datetime import datetime

class TaxCalculator:
    """
    {'Date': '04/04/2021 01:30:43', 'Type': 'Buy', 'Buy Amount': '5', 'Buy Currency':
    '1INCH', 'Sell Amount': '21.5', 'Sell Currency': 'USD', 'Fee Amount': '', 'Currency':
    '', 'Exchange': '', 'Comment': '', 'Deduct': ''}

    {'Date': '04/09/2021 10:20:47', 'Type': 'Sell', 'Buy Amount': '12.895',
    'Buy Currency': 'USD', 'Sell Amount': '5', 'Sell Currency': 'JGN', 'Fee Amount': '',
    'Currency': '', 'Exchange': '', 'Comment': '', 'Deduct': ''}


    """
    
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S"
    
    def __init__(self):
        self.raw_data = []
        self.data = []
        field_names = ('Date', 'Type', 'Buy Amount', 'Buy Currency', 'Sell Amount', 'Sell Currency', 'Fee Amount', 'Currency', 'Exchange', 'Comment', 'Deduct')
        with open("/home/alper/Downloads/crypto-pro-main-copy.csv", "r") as f:
            csv_reader = csv.DictReader(f, field_names)
            for row in csv_reader:
                del row["Deduct"]
                del row["Comment"]
                del row["Exchange"]
                del row["Currency"]
                del row["Fee Amount"]
                try:
                    row["Buy Amount"] = float(row["Buy Amount"])
                    row["Sell Amount"] = float(row["Sell Amount"])
                except:
                    pass
                self.raw_data.append(json.dumps(row))
        # print(self.raw_data)

    def run_total(self):
        buy_amount = 0
        sell_amount = 0
        for line in self.raw_data:
            line = json.loads(line)
            if line["Type"] in ["Deposit", "Buy"]:
                if line["Sell Amount"] != "" and line["Sell Currency"] == "USD":
                    buy_amount += float(line["Sell Amount"])
            if line["Type"] in ["Withdraw", "Sell"]:
                if line["Buy Amount"] != "" and line["Buy Currency"] == "USD":
                    sell_amount += float(line["Buy Amount"])

        print(f"Buy amount: {buy_amount}")
        print(f"Sell amount: {sell_amount}")

    def total_cost_asset(self, asset):
        asset_amount = 0
        fiat_amount = 0
        for line in self.raw_data:
            line = json.loads(line)
            if asset in [line["Buy Currency"], line["Sell Currency"]]:
                print(line)
                if "USD" not in [line["Buy Currency"], line["Sell Currency"]]:
                    continue
                if line["Type"] == "Buy":
                    asset_amount += float(line["Buy Amount"])
                    fiat_amount -= float(line["Sell Amount"])
                elif line["Type"] == "Sell":
                    fiat_amount += float(line["Buy Amount"])
                    asset_amount -= float(line["Sell Amount"])
                else:
                    raise
        print(f"Asset amount: {asset_amount}")
        print(f"Fiat amount: {fiat_amount}")

    def run_asset(self, asset):
        buy_stack = []
        sell_stack = []
        for line in self.raw_data:
            line = json.loads(line)
            if asset in [line["Buy Currency"], line["Sell Currency"]]:
                if "USD" not in [line["Buy Currency"], line["Sell Currency"]]:
                    continue
                if line["Type"] == "Buy":
                    buy_stack.append(line)
                elif line["Type"] == "Sell":
                    sell_stack.append(line)
                else:
                    raise

        sorted_buy_stack = sorted(buy_stack, key=lambda i: datetime.strptime(i["Date"], self.DATE_FORMAT))
        sorted_sell_stack = sorted(sell_stack, key=lambda i: datetime.strptime(i["Date"], self.DATE_FORMAT))

        profit_loss = 0

        for sell in sorted_sell_stack:
            if sell["Sell Amount"] <= buy["Buy Amount"]:
                buy = sorted_buy_stack[0]
                profit_loss += sell["Buy Amount"] - (sell["Sell Amount"] * buy["Sell Amount"] / buy["Buy Amount"])
                buy["Buy Amount"] = buy["Buy Amount"] - sell["Sell Amount"]
                if buy["Buy Amount"] == 0.0:
                    sorted_buy_stack.pop(0)
            else:
                for buy in sorted_buy_stack:
                    if buy[""]





tax_calculator = TaxCalculator()
tax_calculator.run_asset("HNT")
