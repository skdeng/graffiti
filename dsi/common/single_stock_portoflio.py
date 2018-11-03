from dsi.common.portfolio import Portfolio


class SingleStockPortfolio(Portfolio):
    def __init__(self, currency_symbol='usd', stock_symbol='stock', initial_currency=0, initial_stock=0):
        super().__init__()
        self.currency = currency_symbol
        self.stock = stock_symbol
        self.securities[self.currency] = initial_currency
        self.securities[self.stock] = initial_stock

    def get_currency(self):
        return self.securities[self.currency]

    def get_stock(self):
        return self.securities[self.stock]

    def buy(self, amount, price, flat_fee=0, ratio_fee=0):
        total_price = amount * price
        total_price = total_price * (1 + ratio_fee) + flat_fee

        if total_price > self.get_currency():
            raise "Not enough currency for buy order"

        self.add_security(self.currency, -total_price)
        self.add_security(self.stock, amount)

    def sell(self, amount, price, flat_fee=0, ratio_fee=0):
        if amount > self.get_stock():
            raise "Not enough stock for sell order"

        total_price = amount * price
        total_price = total_price / (1 + ratio_fee) - flat_fee

        self.add_security(self.currency, total_price)
        self.add_security(self.stock, -amount)

    def total_buyable_amount(self, price, flat_fee=0, ratio_fee=0):
        total_currency = self.get_currency()
        usable_currency = (total_currency - flat_fee) / (1 + ratio_fee)
        return usable_currency / price
