class Portfolio:
    def __init__(self):
        self.securities = {}

    def add_security(self, security_name, quantity):
        """
        Add a given amount of security to the portfolio
            :param self: self
            :param security_name: symbol of the security
            :param quantity: quantity to add, can be negative for amount to remove
            :raises Exception: exception when trying to remove more than what is available
        """
        if security_name in self.securities:
            new_quantity = self.securities[security_name] + quantity
            if new_quantity < 0:
                raise "Removing more than what's available"
            self.securities[security_name] = new_quantity
        else:
            if quantity < 0:
                raise "Removing from empty security"
            self.securities[security_name] = quantity

    def remove_security(self, security_name):
        """
        Remove a particular security from the portfolio. This will remove all the remaining amounts
            :return: quantity that was removed
        """
        quantity = self.securities[security_name]
        del self.securities[security_name]
        return quantity

    def get(self, security_name):
        """
        Get the current amount for a given security
        """
        if security_name in self.securities:
            return self.securities[security_name]
        else:
            return 0

    def __setitem__(self, security_name, quantity):
        """
        Set amount of security to the portfolio
            :param self: self
            :param security_name: symbol of the security
            :param quantity: quantity to set
            :raises Exception: exception when quantity is negative
        """
        if quantity < 0:
            raise "Setting negative quantity"

        self.securities[security_name] = quantity

    def __delitem__(self, security_name):
        """
        Remove a particular security from the portfolio. This will remove all the remaining amounts
            :return: quantity that was removed
        """
        quantity = self.securities[security_name]
        del self.securities[security_name]
        return quantity

    def __getitem__(self, security_name):
        """
        Overload for [] operator
        Get the current amount for a given security
        """
        if security_name in self.securities:
            return self.securities[security_name]
        else:
            return 0
