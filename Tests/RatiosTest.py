from LongPosition import LongPosition
from ShortPosition import ShortPosition
from PortfolioRatios import *
from RiskyAssetAllocation import *
import math

# Portfolio ratios mean_return, beta, std, tracking_error, market_return, risk_free, market_std
# prs = Portfolio(.07, -.18, math.sqrt(.03), .08, 1, .02, 1)
# print(prs.sharpe_ratio())
# print(prs.treynor_measure())
# print(prs.alpha())
# print(prs.info_ratio())
asseta = AssetMwitz("a", .0978, .3651, 1)
assetb = AssetMwitz("b", .0955, .5234, 1)
# asset1, weight1, asset2, correlation, tracking_error, market_return, rf, market_std
port = two_asset_weighted_portfolio(asseta, .2944, assetb, .0114, 1, 1, .0309, 1)
assettouse = AssetMwitz("touse", port.mean_return, port.std, 1)
utl_func = UtilityFunction("9.8 * sqrt(rc) - 7.48 * stdc")
print(optimal_risky_to_riskfree_weights(utl_func.function, assettouse, .0309))
