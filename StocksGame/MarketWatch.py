from LongPosition import LongPosition
from ShortPosition import ShortPosition
from PortfolioRatios import *
from RiskyAssetAllocation import *
import math
import csv

asset_list = []
market_list = []

grid_sheet = []
with open("stocksgame.csv") as sheet:
    readSheet = csv.reader(sheet)
    for row in readSheet:
        grid_sheet.append(row)

i = 1
j = 1
count = len(grid_sheet[0])
while i < count:
    if i + 1 == count:
        asset_param_list = []
        for row in grid_sheet:
            asset_param_list.append(row[i])
        mrkt = MarketSIM(
            float(asset_param_list[1]), float(asset_param_list[2]), float(asset_param_list[4]),
            float(asset_param_list[3]), float(asset_param_list[5]))
        market_list.append(mrkt)
    else:
        asset_param_list = []
        for row in grid_sheet:
            asset_param_list.append(row[i])
        asset = AssetSIM(
            float(asset_param_list[1]), float(asset_param_list[2]),
            float(asset_param_list[4]), float(asset_param_list[3]))
        asset_list.append(asset)
    i += 1

market = market_list[0]

m_weight = single_index_model(asset_list, market, "market")
weights = single_index_model(asset_list, market, "adj_weights")
weights.append(m_weight)
value_list = value_weights(weights, 101000)
print("Value list:", value_list)
print(sum(value_list))





