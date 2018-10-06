class Transaction:
    def __init__(self, contents):
        self.contents = contents
        self.timestamp = contents[0]
        self.type = contents[1]
        self.asset = contents[2]
        self.amount = float(contents[3])
        self.price = float(contents[4])
        self.total_usd_price = float(contents[5])
        self.fee = self.total_usd_price - self.price * self.amount
        self.remaining = self.amount
        # if math.fabs(float(self.amount) * float(self.price) - float(self.total_usd_price)) > 0.01:
        #     raise Exception("Data Malform + " + str(contents))

    def use(self, amt):
        self.remaining -= amt

    def __str__(self):
        return str(self.contents)

    def is_buy(self):
        return (self.type.lower() == "buy") or (self.type.lower() == "receive")


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
        txn = Transaction(transaction_content)
        if not txn.is_buy():
            total_proceeds += txn.total_usd_price
        transactions.append(txn)
        print(txn)

    print(total_proceeds)

resolved = []
def resolve():

    wallet = []
    count = 0
    for txn in transactions:
        count += 1
        print(count)
        if txn.is_buy():
            wallet.append(txn)

        else:
            sell = txn
            remaining = sell.amount

            while remaining > 0:
                # print(remaining)
                buy = wallet[0]
                print (remaining)
                print(sell)
                print(buy)

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

    return wallet


file = open("./polo_ltc.csv", "r")
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