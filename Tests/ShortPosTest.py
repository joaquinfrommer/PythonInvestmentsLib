from LongPosition import LongPosition
from ShortPosition import ShortPosition
from PortfolioRatios import *
from RiskyAssetAllocation import *
import math
''''''''''
# Short position
spos = ShortPosition(.45, .3, 1500, 37.08)
print(spos.cash)
spos.set_share_price(42)
print(spos.equity_ratio())
print(spos.is_margin_call())
spos.add_cash(1251)
spos.set_share_price(50)
print(spos.is_margin_call())
'''''''''
position = ShortPosition(.52, .4, 190, 207)
print(position.cash)
