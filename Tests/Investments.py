from LongPosition import LongPosition
from ShortPosition import ShortPosition
from PortfolioRatios import *
from RiskyAssetAllocation import *
import math
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
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

# Short position
spos = ShortPosition(.45, .3, 1500, 37.08)
print(spos.cash)
spos.set_share_price(42)
print(spos.equity_ratio())
print(spos.is_margin_call())
spos.add_cash(1251)
spos.set_share_price(50)
print(spos.is_margin_call())

# Portfolio ratios
prs = Portfolio(.13, 1.4, .32, .19, .095, .03, 1)
print(prs.sharpe_ratio())
print(prs.treynor_measure())
print(prs.alpha())
print(prs.info_ratio())

# Utility functions
utfunc = UtilityFunction("2*log(w)")
print(utfunc.utility_output(200))
test_util_weight = utfunc.utility_output_weighted(2000, .4, 1000)
print(test_util_weight)
print(utfunc.certainty_equivalent(1500, test_util_weight))

# Markowitz 2 asset portfolio
# reta, retb, vara, varb, rf, covab
asset1 = Asset("a1", -.02, .28, 1)
asset2 = Asset("a1", .16, .41, 1)
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
asset = Asset("GuacCorp", .15, .22, 1.2)
utl_func = UtilityFunction("rc-.5*4*stdc**2")
print(optimal_risky_to_riskfree_weights(utl_func.function, asset, .07))

# Multiple risky asset optimization
A = AssetMwitz("a1", .15, math.sqrt(.35), 1)
B = AssetMwitz("a1", .22, math.sqrt(.5), 1)
# C = Asset("a1", .08, math.sqrt(.75), 1)
# D = Asset("a1", .17, math.sqrt(.4), 1)
# E = Asset("a1", .21, math.sqrt(.6), 1)
asset_list = [A, B]
covlist = [-.12]
# port = markowitz_optimal_weights(asset_list, covlist, .0352)
# print(port.mean_return, port.variance, port.sharpe_ratio())
port = markowitz_global_minimum(asset_list, covlist, .03)
print(port.mean_return, port.variance, port.sharpe_ratio())
# port = markowitz_given_return(asset_list, covlist, .25, .03)
# print(port.mean_return, port.variance, port.sharpe_ratio())
# Single index model
# alpha, beta, std, res_variance
assetA = AssetSIM(.01, 1.25, .09, .03)
assetB = AssetSIM(.02, 1.5, .15, .02)
assetC = AssetSIM(.03, .95, .12, .0324)
assetD = AssetSIM(-.02, 1.72, .11, .06)
assetE = AssetSIM(.002, 1.85, .14, .039)
assetF = AssetSIM(-.01, 2.1, .0806, .09)
market = MarketSIM(0, 1, .09, 0, .07)
asset_list = [assetA, assetB, assetC, assetD, assetE, assetF]
single_index_model(asset_list, market, "")
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


