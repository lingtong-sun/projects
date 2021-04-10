class Transaction:
    def __init__(self, contents, count):
        self.contents = contents
        self.timestamp = contents[0]
        self.is_buy = int(contents[3]) == 1
        self.count = count
        self.remaining = float(contents[1])
        self.amount = float(contents[1])
        self.price = float(contents[2])
        self.set_total()
        self.fee = 0
        # if math.fabs(float(self.amount) * float(self.price) - float(self.total_usd_price)) > 0.01:
        #     raise Exception("Data Malform + " + str(contents))

    def set_total(self):
        self.total_usd_price = self.amount * self.price
        if self.is_buy:
            self.total_usd_price *= -1

    def use(self, amt):
        self.remaining -= amt

    def __str__(self):
        return str(self.contents)


class ResolvedTransaction:
    def __init__(self, buy_date, sell_date, amount, buy_price, sell_price, fee):
        self.buy_date = buy_date
        self.sell_date = sell_date
        self.amount = float(amount)
        self.buy_price = float(buy_price)
        self.fee = fee
        self.sell_price = float(sell_price)

        self.gain = self.amount * (self.sell_price - self.buy_price) - self.fee
        # self.gain = self.amount * (self.sell_price - self.buy_price)

    def __str__(self):
        return self.buy_date + " B " + " @ $" + str(self.buy_price) + "=====> " \
               + self.sell_date + " S " + " @ $" + str(self.sell_price) + " Amount: " + str(self.amount) + "Total Gain: " + \
               str(self.gain)


transactions = []
def parse(content):
    total_proceeds = 0

    lines = content.split("\n")
    count = 0
    for line in lines:
        line = line.strip()
        count += 1
        if not (count >= 1 and count <= 42): #btc and ltc together, lines 1-42
        # if not (count >= 81 and count <= 84): # ltc
        # if not (count >= 1 and count <= 61):
        # if not (count >= and count <= ): # eth
            continue
        transaction_content = line.split(",")
        txn = Transaction(transaction_content, count)
        total_proceeds += txn.total_usd_price


        transactions.append(txn)
#         print(txn)

    print(total_proceeds)

resolved = []
def resolve():

    wallet = []
    count = 0
    ctotal = 0.0

    for txn in transactions:
        count += 1
        print(str(count) + ": " + txn.__str__())
        if txn.is_buy:
            wallet.append(txn)
            ctotal += txn.amount

        else:
            sell = txn
            ctotal -= sell.amount

            remaining = sell.amount

            while remaining > 0:
                print(remaining)
                buy = wallet[0]
#                 print (remaining)
#                 print(sell)
#                 print(buy)

                if buy.remaining > remaining:
                    used = remaining
                    buy.use(used)
                    remaining = 0
                    resolved.append(ResolvedTransaction(buy.timestamp, sell.timestamp, used, buy.price, sell.price, buy.fee*used/buy.amount))
                else:
                    used = buy.remaining
                    remaining -= used
                    buy.use(used)
                    wallet.pop(0)
                    resolved.append(ResolvedTransaction(buy.timestamp, sell.timestamp, used, buy.price, sell.price, buy.fee*used/buy.amount))
        print("Total: " + str(ctotal))
    return wallet


file = open("./btc2020_sorted.csv", "r")
# file = open("./tax-txns1.csv", "r")
parse(file.read())


wallet = resolve()
total_gain = 0

for rtxn in resolved:
    total_gain += rtxn.gain
    print(str(rtxn) + "\n")

print(total_gain)
acct_bal = 0
for w in wallet:
    acct_bal+=w.remaining

print(acct_bal)
for w in wallet:
    print(w)