import math


# TODO: set tracking error, market return, and market std functions

#  Represents a portfolio. Used to find the key rations for the portfolio
class Portfolio:
    def __init__(self, mean_return, beta, std, tracking_error, market_return, risk_free, market_std):
        self.mean_return = mean_return
        self.beta = beta
        self.std = std
        self.variance = std ** 2
        self.tracking_error = tracking_error
        self.market_return = market_return
        self.market_std = market_std
        self.risk_free = risk_free

    # Sharpe ratio for the portfolio
    def sharpe_ratio(self):
        return sharpe(self.mean_return, self.risk_free, self.std)

    # Treynor measure for the portfolio
    def treynor_measure(self):
        return treynor(self.mean_return, self.risk_free, self.beta)

    # The alpha for the portfolio
    def alpha(self):
        return a(self.mean_return, self.risk_free, self.beta, self.market_return)

    # The information ratio for the portfolio
    def info_ratio(self):
        return self.alpha() / self.tracking_error

    # The M^2 measure for the portfolio
    def m_squared(self):
        return m_squared_measure(self.market_return, self.market_std, self.std, self.mean_return, self.risk_free)


# Represents an asset
class AssetMwitz:
    def __init__(self, name, ret, std, beta):
        self.name = name
        self.rtrn = ret
        self.std = std
        self.beta = beta
        self.variance = std ** 2

    def sharpe_ratio(self, rf):
        return sharpe(self.rtrn, rf, self.std)

    def treynor_measure(self, rf):
        return treynor(self.rtrn, rf, self.beta)

    def alpha(self, rf, market_return):
        return a(self.rtrn, rf, self.beta, market_return)

    def info_ratio(self, rf, market_return, tracking_error):
        return self.alpha(rf, market_return) / tracking_error

    def m_squares(self, market_return, market_std, rf):
        return m_squared_measure(market_return, market_std, self.std, self.rtrn, rf)


# Asset to make single index model computations
class AssetSIM:
    def __init__(self, alpha, beta, std, res_variance):
        self.alpha = alpha
        self.beta = beta
        self.std = std
        self.res_variance = res_variance


# The market in the single index model
class MarketSIM(AssetSIM):
    def __init__(self, alpha, beta, std, res_variance, market_risk_premium):
        self.mrp = market_risk_premium
        super().__init__(alpha, beta, std, res_variance)


# Takes two assets and creates a portfolio based on the weights of the investment
def two_asset_weighted_portfolio(asset1, weight1, asset2, correlation, tracking_error, market_return, rf, market_std):
    weighted_return = (asset1.rtrn * weight1) + (asset2.rtrn * (1 - weight1))
    weighted_variance = (weight1 ** 2) * (asset1.std ** 2) + ((1 - weight1) ** 2) * (asset2.std ** 2) + 2 * weight1 * (
            1 - weight1) * correlation * asset1.std * asset2.std
    weighted_std = math.sqrt(weighted_variance)
    weighted_beta = (asset1.beta * weight1) + (asset2.beta * (1 - weight1))
    return Portfolio(weighted_return, weighted_beta, weighted_std, tracking_error, market_return, rf, market_std)


# Sharpe ratio computation
def sharpe(mean_return, risk_free, std):
    return (mean_return - risk_free) / std


# Treynor measure computation
def treynor(mean_return, risk_free, beta):
    return (mean_return - risk_free) / beta


# Alpha computation
def a(mean_return, risk_free, beta, market_return):
    return mean_return - (risk_free + (beta * (market_return - risk_free)))


# Information ratio stand alone computation
def information_ratio(mean_return, risk_free, beta, market_return, tracking_error):
    return a(mean_return, risk_free, beta, market_return) / tracking_error


# M^2 measure computations
def m_squared_measure(market_return, market_std, std_p, mean_return, risk_free):
    y = market_std / std_p
    ycompliment = 1 - y
    adjusted_return = (mean_return * y) + (risk_free * ycompliment)
    return adjusted_return - market_return
