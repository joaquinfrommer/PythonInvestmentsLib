from LongPosition import LongPosition
from ShortPosition import ShortPosition
from PortfolioRatios import *
from RiskyAssetAllocation import *
import math
'''''''''
# Long position
position = LongPosition(10, .45, .30, 10)
position.begin_with_voa(8000, 30)
print(position.cash)
position.set_share_price(33)
print(position.roe())
position.set_share_price(27)
print(position.is_margin_call())
position.set_share_price(23.57)
print(position.is_margin_call())
'''''''''
position = LongPosition(8883, .51, .26, 30)
print(position.debt)