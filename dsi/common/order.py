class Order:
    def __init__(self, side, volume, price, base_currency, security):
        self.side = side
        self.volume = volume
        self.price = price
        self.base_currency = base_currency
        self.security = security
