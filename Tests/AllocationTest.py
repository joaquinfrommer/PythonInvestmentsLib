from LongPosition import LongPosition
from ShortPosition import ShortPosition
from PortfolioRatios import *
from RiskyAssetAllocation import *
import math
'''''''''
# Utility functions
utfunc = UtilityFunction("2*log(w)")
# print(utfunc.utility_output(200))
test_util_weight = utfunc.utility_output_weighted(2000, .4, 1000)
print(test_util_weight)
print(utfunc.certainty_equivalent(1500, test_util_weight))

# Markowitz 2 asset portfolio
# reta, retb, vara, varb, rf, covab
asset1 = AssetMwitz("a1", -.02, .28, 1)
asset2 = AssetMwitz("a1", .16, .41, 1)
print(eq713(asset1, asset2, .04, .83*.41*.28))

# return1, weight1, return2, std1, std2, beta1, beta2, correlation, tracking_error,market_return, risk_free, market_std
asset1 = Asset("one", .1355, .3156, 1)
asset2 = Asset("two", .0661, .3482, 1)
p = two_asset_weighted_portfolio(asset1, 1.8792, asset2, .0402, 1, 1,  .0359, 1)
print(p.market_return)
print(p.tracking_error)
print(p.mean_return)
print(p.variance)
# Risky with risk free optimization
asset = AssetMwitz("a", .147, math.sqrt(.0874), 1)
utl_func = UtilityFunction("rc-.5*4*stdc**2")
print(optimal_risky_to_riskfree_weights(utl_func.function, asset, .07))
'''''

