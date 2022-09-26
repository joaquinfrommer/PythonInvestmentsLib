from LongPosition import LongPosition
from ShortPosition import ShortPosition
from PortfolioRatios import *
from RiskyAssetAllocation import *
import math

# Multiple risky asset optimization
A = AssetMwitz("a1", 0.15, math.sqrt(0.35), 1)
B = AssetMwitz("a2", 0.22, math.sqrt(.5), 1)
# C = AssetMwitz("a3", .08, math.sqrt(.6), 1)
# D = Asset("a1", .17, math.sqrt(.4), 1)
# E = Asset("a1", .21, math.sqrt(.6), 1)
# asset_list = [A, B]
# covlist = [-.12]
# port = markowitz_optimal_weights(asset_list, covlist, .03)
# print(port.mean_return, port.variance, port.sharpe_ratio())
# port = markowitz_global_minimum(asset_list, covlist, .03)
# print(port.mean_return, port.variance, port.sharpe_ratio())
# port = markowitz_given_return(asset_list, covlist, .25, .03)
# print(port.mean_return, port.variance, port.sharpe_ratio())

# Single index model
# alpha, beta, std, res_variance
assetA = AssetSIM(.01, 2, .09, .01)
assetB = AssetSIM(.02, 1.5, .15, .02)
assetC = AssetSIM(.03, .5, .12, .009)
assetD = AssetSIM(-.02, 2, .11, .0085)
# assetE = AssetSIM(.002, 1.85, .14, .039)
# assetF = AssetSIM(-.01, 2.1, .0806, .09)
market = MarketSIM(0, 1, .08, 0, .06)
asset_list = [assetA, assetB, assetC, assetD]
single_index_model(asset_list, market)