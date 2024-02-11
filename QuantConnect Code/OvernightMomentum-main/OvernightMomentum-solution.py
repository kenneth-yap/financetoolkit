# The investment universe consists of stocks listed at NYSE, AMEX, and NASDAQ, whose daily close-to-close price data are available at the
# CRSP database, and volume-weighted average price data are available at TAQ database. The open price is obtained as the volume-weighted 
# average price in the first half-hour of trading. The formula used to calculate overnight returns is on pages number 6 and 7 of the paper. 
# At the end of each month, the investor sorts stocks into deciles based on their month-1 one-month overnight returns. Then the investor goes
# long on the top decile (winner stocks) and short on the bottom decile (loser stocks). Stocks are held only during overnight session
# (positions are initiated each day at close and are closed during open) Stocks in the portfolios are value-weighted.  
#
# QC Implementation:
#   - The investment univese consists of 100 most liquid US stocks listed at NYSE, AMEX, and NASDAQ with price > 5$.

import numpy as np
from AlgorithmImports import *

class OvernightMomentumStrategy(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        # self.SetEndDate(2024, 1, 1)
        self.SetCash(100000)
        
        self.period = 21 # need n of ovenight returns

        self.symbol = self.AddEquity('SPY', Resolution.Minute).Symbol
        
        self.data = {} # storing objects of SymbolData under stocks symbols
        
        self.traded_quantity = {}
        
        self.coarse_count = 100
        self.selection_flag = False
        self.UniverseSettings.Resolution = Resolution.Minute
        self.AddUniverse(self.CoarseSelectionFunction, self.FineSelectionFunction)
        self.Schedule.On(self.DateRules.MonthStart(self.symbol), self.TimeRules.BeforeMarketClose(self.symbol, 1), self.Selection)
        self.Schedule.On(self.DateRules.EveryDay(self.symbol), self.TimeRules.BeforeMarketClose(self.symbol, 20), self.MarketClose)

    def OnSecuritiesChanged(self, changes):
        for security in changes.AddedSecurities:
            # security.SetFeeModel(CustomFeeModel(self))
            security.SetLeverage(10)

    def CoarseSelectionFunction(self, coarse):
        # update overnight prices on daily basis
        for stock in coarse:
            symbol = stock.Symbol
            
            if symbol in self.data:
                # store current stock price
                self.data[symbol].current_price = stock.AdjustedPrice
                
                # get history prices
                history = self.History(symbol, 1, Resolution.Daily)
                self.UpdateOvernightReturns(symbol, history)
        
        # monthly rebalance
        if not self.selection_flag:
            return Universe.Unchanged
        self.selection_flag = False
        
        selected = sorted([x for x in coarse if x.HasFundamentalData and x.Market == 'usa' and x.Price > 5],
            key=lambda x: x.DollarVolume, reverse=True)
        
        selected = [x.Symbol for x in selected[:self.coarse_count]]
        
        # warm up overnight returns
        for symbol in selected:
            if symbol in self.data and self.data[symbol].is_overnight_returns_ready():
                # get overnight returns from RollingWindow object and reverse it's list for simplier calculation of returns accumulation
                overnight_returns = [x for x in self.data[symbol].overnight_returns]
                overnight_returns.reverse()
                # calculate accumulated returns
                accumulated_returns = np.prod([(1 + x) for x in overnight_returns]) - 1
                # update returns accumulated for last month
                self.data[symbol].returns_accumulated_last_month = accumulated_returns
                
                # go to next iteration, because there is no need for warm up overnight returns
                continue
            
            # initialize SymbolData object for current symbol
            self.data[symbol] = SymbolData(self.period)
            # get history of n + 1 days
            history = self.History(symbol, self.period + 1, Resolution.Daily)
            # update overnight returns based on history prices
            self.UpdateOvernightReturns(symbol, history)
                
        return [x for x in selected if self.data[x].is_ready()]

    def FineSelectionFunction(self, fine):
        fine = [x for x in fine if x.MarketCap != 0 and ((x.SecurityReference.ExchangeId == "NYS") or (x.SecurityReference.ExchangeId == "NAS") or (x.SecurityReference.ExchangeId == "ASE"))]
        
        market_cap = {} # storing stocks market capitalization
        last_accumulated_returns = {} # storing stocks last accumuldated returns
        
        for stock in fine:
            symbol = stock.Symbol
            # store stock's market capitalization
            market_cap[symbol] = stock.MarketCap
            # store stock's last accumulated returns
            last_accumulated_returns[symbol] = self.data[symbol].returns_accumulated_last_month
        
        # not enough data for decile selection     
        if len(last_accumulated_returns) < 10:
            return Universe.Unchanged
        
        # overnight returns sorting
        decile = int(len(last_accumulated_returns) / 10)
        sorted_by_last_acc_ret = [x[0] for x in sorted(last_accumulated_returns.items(), key=lambda item: item[1])]
        
        # long winners 
        long = sorted_by_last_acc_ret[-decile:]
        # short losers
        short = sorted_by_last_acc_ret[:decile]

        # # long winners 
        # long = sorted_by_last_acc_ret[:decile]
        # # short losers
        # short = sorted_by_last_acc_ret[-decile:]
        
        # market cap weighting
        total_market_cap_long = sum([market_cap[x] for x in long])
        for symbol in long:
            if self.data[symbol].current_price != 0:
                current_price = self.data[symbol].current_price
                w = market_cap[symbol] / total_market_cap_long
                quantity = np.floor((self.Portfolio.TotalPortfolioValue * w) / current_price)
                self.traded_quantity[symbol] = quantity
        
        total_market_cap_short = sum([market_cap[x] for x in short])
        for symbol in short:
            if self.data[symbol].current_price != 0:
                current_price = self.data[symbol].current_price
                w = market_cap[symbol] / total_market_cap_short
                quantity = -np.floor((self.Portfolio.TotalPortfolioValue * w) / current_price)
                self.traded_quantity[symbol] = quantity

        return list(self.traded_quantity.keys())
    
    def MarketClose(self):
        # send market on open and on close orders before market closes
        for symbol, q in self.traded_quantity.items():
            self.MarketOnCloseOrder(symbol, -q)
            self.MarketOnOpenOrder(symbol, q)
        
    def UpdateOvernightReturns(self, symbol, history):
        # calculate overnight returns only if history isn't empty
        if history.empty:
            return
        
        # get open and close prices
        opens = history.loc[symbol].open
        closes = history.loc[symbol].close
        
        # calculate overnight return for each day
        for (_, close_price), (_, open_price) in zip(closes.iteritems(), opens.iteritems()):
            # check if previous close price isn't None
            if self.data[symbol].prev_close_price:
                # calculate overnight return
                overnight_return = (open_price / self.data[symbol].prev_close_price) - 1
                # store overnight return
                self.data[symbol].update(overnight_return)
            
            # change value of prev close price for next calculation
            self.data[symbol].prev_close_price = close_price
        
    def Selection(self):
        self.selection_flag = True
        self.traded_quantity.clear()
        
class SymbolData():
    def __init__(self, period):
        self.overnight_returns = RollingWindow[float](period)
        self.returns_accumulated_last_month = None
        self.prev_close_price = None
        self.current_price = 0
        
    def update(self, overnight_return):
        self.overnight_returns.Add(overnight_return)
        
    def is_ready(self):
        return self.returns_accumulated_last_month
        
    def is_overnight_returns_ready(self):
        return self.overnight_returns.IsReady
        
# Custom fee model
class CustomFeeModel(FeeModel):
    def GetOrderFee(self, parameters):
        fee = parameters.Security.Price * parameters.Order.AbsoluteQuantity * 0.00005
        return OrderFee(CashAmount(fee, "USD"))
