# The investment universe consists of global large-cap stocks (or US large-cap stocks). At the end of each month, the investor constructs 
# equally weighted decile portfolios by ranking the stocks on the past three-year volatility of weekly returns. The investor goes long 
# stocks in the top decile (stocks with the lowest volatility).
#
# QC implementation changes
#   - Top quartile (stocks with the lowest volatility) is fundamental instead of decile.

# Advice:
#   - To view algorithm errors, toggle Console view below when in Backtesting
#   - To print out debugging messages (the difference is only in colours), use
#     `self.Debug(...)` or `self.Error(...)` - See LINK 1
#   - To stop backtesting, go to Organisation (tab #2) -> Resources -> Stop

... # TODO 1: import numpy, AlgorithmImports, as well as List and Dict from the typing library
#region imports
...
...
...
#endregion

class LowVolatilityFactorEffectStocks(QCAlgorithm):

    def Initialize(self) -> None:
	# TODO 2: Initialize method (LINK 2)
        self.SetStartDate(...) # set start date to 1st January 2000.  
        self.SetCash(...) # set starting cash to 100k

        self.symbol: Symbol = self.AddEquity('SPY', Resolution.Daily).Symbol
        
        self.period: int = ... # number of working days in a year
        
        self.fundamental_count: int = 3000
        self.quantile: int = 4
        self.leverage: int = 10
        self.data: Dict[Symbol, SymbolData] = {}
        
        self.long: List[Symbol] = []

        self.selection_flag: bool = ... # set selection flag to True
        self.UniverseSettings.Resolution = ... # set Resolution to Daily
        self.Settings.MinimumOrderMarginPortfolioPercentage = ... # set percentage to 0
        self.AddUniverse(self.FundamentalSelectionFunction)
        self.Schedule.On(self.DateRules.MonthEnd(self.symbol), self.TimeRules.AfterMarketOpen(self.symbol), self.Selection)

    def OnSecuritiesChanged(self, changes: SecurityChanges) -> None:
	# TODO 3: OnSecuritiesChanged method
        for security in changes.AddedSecurities:
            ... # set Fee model to CustomFeeModel() (LINK 3)
            ... # set leverage (LINK 4)
            
    def FundamentalSelectionFunction(self, fundamental: List[Fundamental]) -> List[Symbol]:
        # Update the rolling window every day.
        for stock in fundamental:
            symbol: Symbol = stock.Symbol

            # TODO 4: Store daily price
            if symbol in self.data:
                ... # use the update method from the SymbolData class to set the stored data for the symbol equal to the stock's adjusted price, stock.AdjustedPrice

        if not self.selection_flag:
            return Universe.Unchanged

        # TODO 5: update and clean fundamental list
	fundamental: List[Fundamental] = [
            x for x in fundamental if ... and x.Market == ... and x.MarketCap != ...
        ] # only keep the elements in fundamental if they: 1) have fundamental data, 2) are traded in the USA and 3) have a non-negative market cap
        if len(fundamental) > self.fundamental_count:
            ... # sort fundamental by the 3000 stocks with largest market cap (LINK 5)

        # Warmup price rolling windows.
        weekly_vol: Dict[Symbol, float] = {}

        for stock in fundamental:
            symbol: Symbol = stock.Symbol

	    # TODO 6: when stock isn't in data
            if symbol not in self.data:
                self.data[symbol] = SymbolData(self.period)
                history: DataFrame = self.History(symbol, self.period, Resolution.Daily)
                if ...: # if the history dataframe is empty, log that the symbol doesn't have enough data before continuing (LINK 1)
                    ...
                    ...
                closes: pd.Series = history.loc[symbol].close
                for time, close in closes.items():
                    ... # update our data for this symbol with the close price 
            
            if self.data[symbol].is_ready():
                weekly_vol[symbol] = self.data[symbol].volatility()

        if len(weekly_vol) >= self.quantile:
            # TODO 7: volatility sorting
            sorted_by_vol: List[Tuple] = ... # sort weekly volatility from highest to lowest (LINK 5)
            quantile: int = int(len(sorted_by_vol) / self.quantile)
            self.long = [x[0] for x in ...] # take the last quantile stocks with the lowest volatility
        
        return self.long
        
    def OnData(self, data: Slice) -> None:
        if not self.selection_flag:
            return
        self.selection_flag = False

        # TODO 8: trade execution
        invested: List[Symbol] = [x.Key for x in self.Portfolio if x.Value.Invested]
        for symbol in invested:
            if symbol not in self.long:
                ... # Liquidate symbol (LINK 6)

        for symbol in self.long:
            if symbol in data and data[symbol]:
                ... # set equal weight portfolio of our holdings (LINK 7)

        self.long.clear()
        
    def Selection(self) -> None:
        self.selection_flag = True

class SymbolData():
    def __init__(self, period: int) -> None:
        self.price: RollingWindow = RollingWindow[float](period)
    
    def update(self, value: float) -> None:
        self.price.Add(value)
    
    def is_ready(self) -> bool:
        return self.price.IsReady
        
    def volatility(self) -> float:
        closes: List[float] = [x for x in self.price]
        
        # Weekly volatility calc.
        separete_weeks: List[float] = [closes[x:x+5] for x in range(0, len(closes), 5)]
        weekly_returns: List[float] = [(x[0] - x[-1]) / x[-1] for x in separete_weeks]

        return np.std(weekly_returns)   

# Custom fee model.
class CustomFeeModel(FeeModel):
    def GetOrderFee(self, parameters: OrderFeeParameters) -> OrderFee:
	TODO 9: find corresponding fee
        fee: float = ... # fee corresponds to 0.005% of total transaction volume
        return OrderFee(CashAmount(fee, USD))

#LINKS:
#1: https://www.quantconnect.com/docs/v2/cloud-platform/projects/debugging
#2: https://www.quantconnect.com/docs/v2/writing-algorithms/initialization?ref=v1
#3: https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/transaction-fees/key-concepts#:~:text=To%20manually%20set%20the%20fee,method%20on%20the%20Security%20object.&text=You%20can%20also%20set%20the,use%20the%20security%20initializer%20technique.
#4: https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/buying-power#:~:text=To%20set%20the%20leverage%20when,pass%20in%20a%20leverage%20argument.&text=You%20can%20also%20set%20the%20asset%20leverage%20in%20a%20security%20initializer.
#5: https://www.w3schools.com/python/ref_func_sorted.asp
#6: https://www.quantconnect.com/docs/v2/writing-algorithms/trading-and-orders/liquidating-positions
#7: https://www.quantconnect.com/docs/v2/writing-algorithms/trading-and-orders/position-sizing#:~:text=If%20you%20already%20have%20holdings,to%20free%20up%20buying%20power.&text=If%20the%20percentage%20you%20provide,and%20doesn't%20log%20anything.
