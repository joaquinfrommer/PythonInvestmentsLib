from sympy import *
from PortfolioRatios import *

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Section for the Markowitz way to find the optimal combination of assets
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Symbols and set functions
w = symbols('w')
return_c = symbols('rc')
return_q = symbols('rq')
sigma_c = symbols('stdc')
sigma_q = symbols('stdq')
risk_free = symbols('rf')
y = symbols('y')
return_expanded = risk_free + y * (return_q - risk_free)
sigma_expanded = y * sigma_q
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


# Represents a utility function, please use the variable w for wealth
class UtilityFunction:
    def __init__(self, function):
        self.function = sympify(function)

    # Output of a utility function based on wealth
    def utility_output(self, wealth):
        return self.function.subs(w, wealth).evalf()

    # Output for a utility function where the expected return must be calculated
    def utility_output_weighted(self, wealth1, weight1, wealth2):
        return ((self.function.subs(w, wealth1) * weight1) + (self.function.subs(w, wealth2) * (1 - weight1))).evalf()

    # The certainty equivalent for the risk free money vs the risky money
    def certainty_equivalent(self, rsf, risky_utility):
        utility_equation = Eq(risky_utility, self.function)
        answer = solveset(utility_equation, w)
        return rsf - answer.args[0]


# Markowitz solution for 2 assets
def eq713(asset1, asset2, rskfree, cov):
    Ra = asset1.rtrn - rskfree
    Rb = asset2.rtrn - rskfree
    return ((Ra * asset2.variance) - (Rb * cov)) / ((Ra * asset2.variance) + (Rb * asset1.variance) - ((Ra + Rb) * cov))


# Finds the optimal weights for risky and risk free asset combination
def optimal_risky_to_riskfree_weights(utl_func, asset, rskfree):
    utl_func = utl_func.subs([(return_c, return_expanded), (sigma_c, sigma_expanded)])
    utl_func = utl_func.subs([(risk_free, rskfree), (return_q, asset.rtrn), (sigma_q, asset.std)])
    max_eq = Eq(maximum(utl_func, y), utl_func)
    answer = solveset(max_eq, y)
    return round(answer.args[0], 6)


# fills the row of a variance co variance matrix
def make_matrix_row(buckets, row, n):
    ret_list = []
    count = 0
    while count < n - 1:
        if row == count:
            ret_list.extend(buckets[count])
            break
        else:
            ret_list.append(buckets[count][(row - 1) - count])
        count += 1
    return ret_list


# outputs the covariances in that row
def make_cov_matrix(cov_list, n, asset_list):
    breakdown_list = []
    count = n - 1
    tracker = 0
    for j in range(n - 1):
        i = 0
        buckets = []
        while i < count:
            buckets.append(cov_list[tracker])
            i += 1
            tracker += 1
        breakdown_list.append(buckets)
        count -= 1
    sigma_list = []
    for i in range(n):
        sigma_list.append([])
    for i, lst in enumerate(sigma_list):
        j = 0
        row_list = make_matrix_row(breakdown_list, i, n)
        cov_adder = iter(row_list)
        while j < n:
            if j == i:
                lst.append(asset_list[i].variance)
            else:
                lst.append(next(cov_adder))
            j += 1
    return Matrix(sigma_list)


# finds the optimal investment weights and portfolio for a list of assets
def markowitz_optimal_weights(asset_list, cov_list, rskfree):
    excess_returns_list = []
    returns_list = []
    betas_list = []
    for asset in asset_list:
        excess_returns_list.append([asset.rtrn - rskfree])
        returns_list.append([asset.rtrn])
        betas_list.append([asset.beta])
    excess_returns = Matrix(excess_returns_list)
    returns = Matrix(returns_list)
    betas = Matrix(betas_list)
    ones_transpose = ones(1, len(asset_list))
    cov_matrix = make_cov_matrix(cov_list, len(asset_list), asset_list)
    numerator = (cov_matrix ** -1) * excess_returns
    denominator = ones_transpose * (cov_matrix ** -1 * excess_returns)
    optimal_weights_matrix = numerator / denominator[0, 0]
    portfolio_variance = (optimal_weights_matrix.T * cov_matrix * optimal_weights_matrix)[0, 0]
    portfolio_return = (optimal_weights_matrix.T * returns)[0, 0]
    portfolio_beta = (optimal_weights_matrix.T * betas)[0, 0]
    portfolio = Portfolio(portfolio_return, portfolio_beta, math.sqrt(portfolio_variance), 1, 1, rskfree, 1)
    print(optimal_weights_matrix)
    return portfolio


# The weights and portfolio for the global minimum variance protfolio
def markowitz_global_minimum(asset_list, cov_list, rskfree):
    returns_list = []
    betas_list = []
    col_to_add = []
    c_list = []
    for asset in asset_list:
        returns_list.append([asset.rtrn])
        betas_list.append([asset.beta])
        col_to_add.append(1)
        c_list.append(0)
    returns = Matrix(returns_list)
    betas = Matrix(betas_list)
    cov_matrix = make_cov_matrix(cov_list, len(asset_list), asset_list)
    A = cov_matrix
    A = A.row_insert(len(asset_list), ones(1, len(asset_list)))
    col_to_add.append(0)
    A = A.col_insert(len(asset_list), Matrix(col_to_add))
    c_list.append(1)
    C = Matrix(c_list)
    optimal_weights_matrix = (A ** -1) * C
    print(optimal_weights_matrix)
    weights_list = []
    for i in range(len(asset_list)):
        weights_list.append(optimal_weights_matrix[i, 0])
    weights_matrix = Matrix(weights_list)
    portfolio_variance = (weights_matrix.T * cov_matrix * weights_matrix)[0, 0]
    portfolio_return = (weights_matrix.T * returns)[0, 0]
    portfolio_beta = (weights_matrix.T * betas)[0, 0]
    portfolio = Portfolio(portfolio_return, portfolio_beta, math.sqrt(portfolio_variance), 1, 1, rskfree, 1)
    return portfolio


# finds the optimal weights and portfolio for the least risk at a given return
def markowitz_given_return(asset_list, cov_list, rtrn, rskfree):
    returns_list = []
    betas_list = []
    col_to_add = []
    c_list = []
    transposed_returns_list = []
    for asset in asset_list:
        returns_list.append([asset.rtrn])
        transposed_returns_list.append(asset.rtrn)
        betas_list.append([asset.beta])
        col_to_add.append(1)
        c_list.append(0)
    returns = Matrix(returns_list)
    transposed_returns_list.append(0)
    betas = Matrix(betas_list)
    cov_matrix = make_cov_matrix(cov_list, len(asset_list), asset_list)
    A = cov_matrix
    A = A.row_insert(len(asset_list), ones(1, len(asset_list)))
    col_to_add.append(0)
    A = A.col_insert(len(asset_list), Matrix(col_to_add))
    A = A.row_insert(len(asset_list) + 1, Matrix([transposed_returns_list]))
    transposed_returns_list.append(0)
    A = A.col_insert(len(asset_list) + 1, Matrix(transposed_returns_list))
    c_list.append(1)
    c_list.append(rtrn)
    C = Matrix(c_list)
    optimal_weights_matrix = (A ** -1) * C
    print(optimal_weights_matrix)
    weights_list = []
    for i in range(len(asset_list)):
        weights_list.append(optimal_weights_matrix[i, 0])
    weights_matrix = Matrix(weights_list)
    portfolio_variance = (weights_matrix.T * cov_matrix * weights_matrix)[0, 0]
    portfolio_return = (weights_matrix.T * returns)[0, 0]
    portfolio_beta = (weights_matrix.T * betas)[0, 0]
    portfolio = Portfolio(portfolio_return, portfolio_beta, math.sqrt(portfolio_variance), 1, 1, rskfree, 1)
    return portfolio


# Single index model portfolio computations
def single_index_model(asset_list, market, step):
    alpha_var_list = [[asset.alpha, asset.res_variance] for asset in asset_list]
    info_list = [info[0] / info[1] for info in alpha_var_list]
    sum_unadj_weights = sum(info_list)
    print("Info ratios and unadjusted weights: ", info_list, sum_unadj_weights)
    if step == "proportions":
        return info_list
    adjusted_weight_list = [weight / sum_unadj_weights for weight in info_list]
    sum_weighted = sum(adjusted_weight_list)
    print("Adjusted weights: ", adjusted_weight_list, sum_weighted)
    if step == "weights":
        return adjusted_weight_list
    alphas = [alpha[0] for alpha in alpha_var_list]
    weighted_alpha_list = [alphas[i] * adjusted_weight_list[i] for i in range(len(alphas))]
    adjusted_alpha = sum(weighted_alpha_list)
    print("Alphas: ", weighted_alpha_list, adjusted_alpha)
    if step == "alpha":
        return adjusted_alpha
    variances = [vari[1] for vari in alpha_var_list]
    weighted_variance_list = [variances[i] * adjusted_weight_list[i] ** 2 for i in range(len(variances))]
    adjusted_variance = sum(weighted_variance_list)
    print("Variances: ", weighted_variance_list, adjusted_variance)
    if step == "a_variance":
        return adjusted_variance
    active_portfolio_weight = (adjusted_alpha / adjusted_variance) / (market.mrp / (market.std ** 2))
    print("Active portfolio weights: ", active_portfolio_weight)
    if step == "init_pos":
        return active_portfolio_weight
    beta_list = [adjusted_weight_list[i] * asset_list[i].beta for i in range(len(asset_list))]
    portfolio_beta = sum(beta_list)
    print("Betas: ", beta_list, portfolio_beta)
    if step == "beta":
        return portfolio_beta
    adjusted_active_portfolio_weight = active_portfolio_weight / (1 + (1 - portfolio_beta) * active_portfolio_weight)
    print("Adjusted portfolio weight: ", adjusted_active_portfolio_weight)
    if step == "adj_port":
        return adjusted_active_portfolio_weight
    total_weighted_asset_list = [adjusted_active_portfolio_weight * weight for weight in adjusted_weight_list]
    market_weight = 1 - adjusted_active_portfolio_weight
    print("Total asset weights: ", total_weighted_asset_list)
    if step == "adj_weights":
        return total_weighted_asset_list
    print("Market portfolio weight: ", market_weight)
    if step == "market":
        return market_weight
    portfolio_risk_premium = (market_weight + adjusted_active_portfolio_weight * portfolio_beta) * market.mrp + \
                             adjusted_active_portfolio_weight * adjusted_alpha
    print("Portfolio risk premium: ", portfolio_risk_premium)
    if step == "rp":
        return portfolio_risk_premium
    portfolio_variance = (market_weight + adjusted_active_portfolio_weight * portfolio_beta) ** 2 * market.std ** 2 + \
                         (adjusted_active_portfolio_weight ** 2 * adjusted_variance)
    print("Portfolio variance: ", portfolio_variance)
    if step == "variance":
        return portfolio_variance
    sharpe_ratio = portfolio_risk_premium/math.sqrt(portfolio_variance)
    print("Sharpe ratio: ", sharpe_ratio)
    if step == "sr":
        return sharpe_ratio
    market_sr = market.mrp/market.std
    print("Sharpe ratio market: ", market_sr)
    if step == "msr":
        return market_sr


# Create a sympi equation to find the weighted amount of cash needed
def create_cash_eq(weight_list, cash):
    eqstringlist = []
    for weight in weight_list:
        eq_seg = "(" + str(math.fabs(weight)) + " * x)"
        eqstringlist.append(eq_seg)
    eqs = "+".join(eqstringlist)
    func = sympify(eqs)
    eq = Eq(func, cash)
    return eq


# Takes a list of asset weights and values them
def value_weights(weight_list, cash):
    x = symbols('x')
    cash_eq = create_cash_eq(weight_list, cash)
    weighted_cash = solveset(cash_eq, x).args[0]
    value_list = [weighted_cash * math.fabs(weight) for weight in weight_list]
    return value_list


