# Represents a short position
class ShortPosition:
    def __init__(self, init_margin, maintain, shares, share_price):
        self.init_margin = init_margin
        self.maintain = maintain
        self.shares = shares
        self.share_price = share_price
        self.init_voa = self.voa()
        self.cash = self.init_margin * self.init_voa

    # Sets the share price
    def set_share_price(self, price):
        self.share_price = price

    # sets the number of shares
    def set_number_of_shares(self, number):
        self.shares = number

    # adds equity to the position
    def add_cash(self, cash):
        self.cash += cash

    # value of assets of the position
    def voa(self):
        return self.share_price * self.shares

    # equity of the position
    def equity(self):
        return self.init_voa + self.cash - self.voa()

    # equity ratio for the position
    def equity_ratio(self):
        return self.equity() / self.voa()

    # The price which will yeild a margin call for the position
    def margin_call_price(self):
        return (self.init_voa + self.cash) / ((self.maintain * self.shares) + self.shares)

    # Tells you if there is a margin call in the position or not
    # Returns 0 if there is no margin call and returns the price t restore the margin if there is
    def is_margin_call(self):
        if self.equity_ratio() > self.maintain:
            return 0
        else:
            return (self.maintain * self.voa()) - self.equity()

    # The return on equity of the position
    def roe(self):
        return (self.equity() - self.cash) / self.cash
