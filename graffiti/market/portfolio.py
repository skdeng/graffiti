class Portfolio:
    default_currency = 'USD'
    default_asset = 'asset'

    def __init__(self, overdraw=False, base_currency='USD'):
        self.securities = {}
        self.overdraw = overdraw
        self.base_currency = base_currency

    @classmethod
    def from_config(cls, config: dict):
        p = cls(config.get('overdraw', False))
        for s in config:
            if s.lower() != 'overdraw':
                p.add_security(s, config[s])
        return p

    def add_security(self, security_name: str, quantity: float):
        """
        Add a given amount of security to the portfolio
            :param self: self
            :param security_name: symbol of the security
            :param quantity: quantity to add, can be negative for amount to remove
            :raises Exception: exception when trying to remove more than what is available
        """
        security_name = security_name.upper()
        if security_name in self.securities:
            new_quantity = self.securities[security_name] + quantity
            if not self.overdraw and new_quantity < 0:
                raise "Removing more than what's available"
            self.securities[security_name] = new_quantity
        else:
            if not self.overdraw and quantity < 0:
                raise "Removing from empty security"
            self.securities[security_name] = quantity

    def remove_security(self, security_name: str):
        """
        Remove a particular security from the portfolio. This will remove all the remaining amounts
            :return: quantity that was removed
        """
        security_name = security_name.upper()
        quantity = self.securities[security_name]
        del self.securities[security_name]
        return quantity

    def get(self, security_name: str):
        """
        Get the current amount for a given security
        """
        security_name = security_name.upper()
        if security_name in self.securities:
            return self.securities[security_name]
        else:
            return 0

    def __setitem__(self, security_name: str, quantity: float):
        """
        Set amount of security to the portfolio
            :param self: self
            :param security_name: symbol of the security
            :param quantity: quantity to set
            :raises Exception: exception when quantity is negative
        """
        if not self.overdraw and quantity < 0:
            raise "Setting negative quantity"

        security_name = security_name.upper()
        self.securities[security_name] = quantity

    def __delitem__(self, security_name: str):
        """
        Remove a particular security from the portfolio. This will remove all the remaining amounts
            :return: quantity that was removed
        """
        return self.remove_security(security_name)

    def __getitem__(self, security_name: str):
        """
        Overload for [] operator
        Get the current amount for a given security
        """
        return self.get(security_name)

    def __str__(self):
        return str(self.securities)
