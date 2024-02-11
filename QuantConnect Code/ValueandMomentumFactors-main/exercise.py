# Create an investment universe containing investable asset classes (could be US large-cap, mid-cap stocks, US REITS, UK, Japan, Emerging market stocks, US treasuries, US Investment grade bonds,
# US high yield bonds, Germany bonds, Japan bonds, US cash) and find a good tracking vehicle for each asset class (best vehicles are ETFs or index funds). Momentum ranking is done on price series.
# Valuation ranking is done on adjusted yield measure for each asset class. E/P (Earning/Price) measure is used for stocks, and YTM (Yield-to-maturity) is used for bonds. US, Japan, and Germany 
# treasury yield are adjusted by -1%, US investment-grade bonds are adjusted by -2%, US High yield bonds are adjusted by -6%, emerging markets equities are adjusted by -1%, and US REITs are 
# adjusted by -2% to get unbiased structural yields for each asset class. Rank each asset class by 12-month momentum, 1-month momentum, and by valuation and weight all three strategies (25% weight
# to 12m momentum, 25% weight to 1-month momentum, 50% weight to value strategy). Go long top quartile portfolio and go short bottom quartile portfolio.
#
# QC implementation changes:
#   - Country PB data ends in 2019. Last known value is used for further years calculations for the sake of backtest.'

GENERAL ADVICE:
#   - To view algorithm errors, toggle Console view below when in Backtesting
#   - To print out debugging messages (the difference is only in colours), use
#     'self.Debug(...)' or 'self.Error(...)' - See LINK 1
#   - To stop backtesting, go to Organisation (tab #2) -> Resources -> Stop

### TODO 1: Imports and Set Date
#region imports
# ... (Import AlgorithmImports)
# ... (Import data_tools)
#endregion

class ValueandMomentumFactorsacrossAssetClasses(QCAlgorithm):

    def Initialize(self): # LINK 2
        self.SetStartDate(...) # Set Start Date to 1st January 2013
        self.SetCash(100000)
        
        # investable asset, yield symbol, yield data access function, yield adjustment, reverse flag(PE -> EP)
        self.assets = [
            ('SPY', 'MULTPL/SP500_EARNINGS_YIELD_MONTH', data_tools.QuandlValue, 0, True),  # US large-cap
            ('MDY', 'MID_CAP_PE', data_tools.QuantpediaPERatio, 0, True),                   # US mid-cap stocks
            ('IYR', 'REITS_DIVIDEND_YIELD', data_tools.QuantpediaPERatio, -2, False),       # US REITS - same csv data format as PERatio files
            ('EWU', 'United Kingdom', None, 0, True),                                       # UK
            ('EWJ', 'Japan', None, 0, True),                                                # Japan
            ('EEM', 'EMERGING_MARKET_PE', data_tools.QuantpediaPERatio, -1, True),          # Emerging market stocks
            
            ('LQD', 'ML/AAAEY', data_tools.QuandlAAAYield, -2, False),                      # US Investment grade bonds
            ('HYG', 'ML/USTRI', data_tools.QuandlHighYield, -6, False),                     # US high yield bonds
            
            ('CME_TY1', 'US10YT', data_tools.QuantpediaBondYield, -1, False),               # US bonds
            ('EUREX_FGBL1', 'DE10YT', data_tools.QuantpediaBondYield, -1, False),           # Germany bonds
            ('SGX_JB1', 'JP10YT', data_tools.QuantpediaBondYield, -1, False),               # Japan bonds
            
            ('BIL', 'OECD/KEI_IRSTCI01_USA_ST_M', data_tools.QuandlValue, 0, False)         # US cash
        ]
        
        # country pe data
        self.country_pe_data = self.AddData(data_tools.CountryPE, 'CountryData').Symbol
        
	### TODO 2
        ...  # Create a dictionary called data
        ... # Set a variable called period to the number of months in 21 years
        ... # Warmup for a duration period

	### TODO 3
        for symbol, yield_symbol, yield_access, _, _ in self.assets:
            # investable asset
            if ... : # check if yield access is the same as QuantpediaBondYield from data_tools
                ... # Add data from QuantpediaFutures in data_tools, with our given symbol, at a Daily Resolution, and store it in the data variable
            else:
                ... # Add the equity with our given symbol at a Daily Resolution, and store it in the data variable

            # yield
            if ... : # check if yield access is different to None type
		... # Add data with parameters of yield access and the yield's symbol, at a Daily Resolution

            self.data[symbol] = RollingWindow[float](self.period)
            
	    ... # Set the Fee Model to CustomFeeModel
	    ... # Set the leverage to 5
		# LINK 3
        
	... # Set the variable recent_month to -1
    
    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        # store investable asset price data
        for symbol, yield_symbol, _, _, _ in self.assets:
            symbol_obj = self.Symbol(symbol)
            if symbol_obj in data and data[symbol_obj]:
                self.data[symbol].Add(data[symbol_obj].Value)
        
	### TODO 4: If the variable recent_month is the same month as currently, then we don't need to execute this function. Otherwise, set recent_month to our current month
	...
	...
	...
        
	### TODO 5: Create dictionnaries performance_1M, performance_12M and valuation
	...
	...
	...
        
        # performance and valuation calculation
        if self.Securities[self.country_pe_data].GetLastData() and (self.Time.date() - self.Securities[self.country_pe_data].GetLastData().Time.date()).days <= 365:
            for symbol, yield_symbol, yield_access, bond_adjustment, reverse_flag in self.assets:
                if self.Securities[symbol].GetLastData() and (self.Time.date() - self.Securities[symbol].GetLastData().Time.date()).days < 3:
                    if self.data[symbol].IsReady:
                        closes = [x for x in self.data[symbol]]
                        performance_1M[symbol] = closes[0] / closes[21] - 1
                        performance_12M[symbol] = closes[0] / closes[len(closes) - 1] - 1
                        
                        if yield_access == None:
                            country_pb_data = self.Securities['CountryData'].GetLastData()
                            if country_pb_data:
                                pe = country_pb_data[yield_symbol]
                                yield_value = pe
                        else:
                            yield_value = self.Securities[self.Symbol(yield_symbol)].Price
                        
                        # reverse if needed, EP->PE
			### TODO 6: if the variable reverse_flag is true, then set yield_value to the inverse of itself
			...
			...
                        
			### TODO 7: If the yield value is different to 0, set the valuation for a given symbol to the sum the yield value and bond adjustment
                        ...
			...

        long = []
        short = []
        
        if len(valuation) != 0:
            # sort assets by metrics
	    ### TODO 8: sort both performances and valuations by metrics into sorted_by_p1, sorted_by_p12 and sorted_by_value
	    # LINK 4
	    ... 
	    ...
	    ...
            
            # rank assets
	    ### TODO 9: Create a dictionary called score. For each symbol, set the score to be a quarter of its rank for 1-month momentum, 12-month momentum and value. 
	    ... #
	    ... #
	    ... # 
	    ... #
	    ... #
	    ... # 
	    ... #
            
            # sort by rank
	    ### TODO 10: Sort score by rank, and create lists of symbols to long and short
	    ... #
	    ... #
	    ... # 
	    ... #
        
        # trade execution
        invested = [x.Key.Value for x in self.Portfolio if x.Value.Invested]
	### TODO 11: Liquidate symbol if the symbol is invested but it doesn't feature in either long or short.
	# LINK 5
	    ... #
	    ... # 
	    ... #

	### TODO 12: Long and Short holdings equally for all symbols in long and short lists.
	# LINK 6

	    ... #
	    ... #

	    ... #
	    ... #
	    ... # 
	    ... #

# Custom fee model.
class CustomFeeModel(FeeModel):
    def GetOrderFee(self, parameters):
        fee = parameters.Security.Price * parameters.Order.AbsoluteQuantity * 0.00005
        return OrderFee(CashAmount(fee, "USD"))

### LINKS
1) https://www.quantconnect.com/docs/v2/cloud-platform/projects/debugging
2) https://www.quantconnect.com/docs/v2/writing-algorithms/initialization?ref=v1
3) https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/buying-power
4) https://www.w3schools.com/python/ref_func_sorted.asp
5) https://www.quantconnect.com/docs/v2/writing-algorithms/trading-and-orders/liquidating-positions
6) https://www.quantconnect.com/docs/v2/writing-algorithms/trading-and-orders/position-sizing
