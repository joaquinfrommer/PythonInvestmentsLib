import math


# Represents creating a long position
class LongPosition:
    """Opening a long position on margin. If you only have the value of assets to find cash and debt, 0 out the amounts
       and use the "begin_with_voa" method"""

    def __init__(self, cash, init_margin, maint_margin, share_price):
        self.init_margin = init_margin
        self.maintain = maint_margin
        self.share_price = share_price
        self.cash = cash
        self.debt = (self.cash / self.init_margin) - self.cash
        self.shares = math.floor((self.cash + self.debt) / self.share_price)

    # set share price
    def set_share_price(self, price):
        self.share_price = price

    # set number of shares
    def set_shares(self, number):
        self.shares = number

    # set the debt amount
    def set_debt(self, debt_amount):
        self.debt = debt_amount

    # if you begin with the value of assets, 0 out the constructor and then run this method
    def begin_with_voa(self, shares, share_price):
        self.shares = shares
        self.share_price = share_price
        self.cash = self.voa() * self.init_margin
        self.debt = self.voa() - self.cash

    # finds the value of assets
    def voa(self):
        return self.shares * self.share_price

    # finds the equity of the position
    def equity(self):
        return self.voa() - self.debt

    # finds the equity ratio
    def equity_ratio(self):
        return self.equity()/self.voa()

    # finds the price at which there is a margin call
    def margin_call_price(self):
        return (0 - self.debt)/((self.maintain * self.shares)-self.shares)

    # checks if there should be a margin call in the position
    # if there is a margin call, it returns the amount needed to restore the margin and 0 otherwise
    def is_margin_call(self):
        if self.equity_ratio() > self.maintain:
            return 0
        else:
            return (self.maintain * self.voa()) - self.equity()

    # finds return on equity
    def roe(self):
        return (self.equity() - self.cash)/self.cash
