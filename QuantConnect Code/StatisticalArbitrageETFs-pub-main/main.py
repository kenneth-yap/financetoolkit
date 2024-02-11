# Description: Statistical Arbitrage with ETFs 
#
# The investment universe consists of all ETFs traded on the market. The investor uses data about historical End of 
# Day premium/discounts from data providers (Bloomberg, Yahoo, etc.) or from ETF issuers to compute the average 
# premium/discount and its standard deviation for each ETF. He/she then uses the “Intraday Value” of the ETF to 
# compare the current premium/discount for each ETF and buys ETF at close if its discount at a close move away 
# from its mean historical value by more than two standard deviations. He/she closes the trade if the ETF premium 
# at the close of future trading days move away from its mean historical value by more than one standard deviation. 
# The portfolio of current ETFs held is equally weighted.


# import ETF NAV data sourced from Quantepdia in data_tools.py  
import data_tools
from collections import deque

class StatisticalArbitragewithETFs(QCAlgorithm):

    def Initialize(self):
        
        #TASK 1 (Set conditions)
        self.SetStartDate(...) # set start date (e.g. 2005, 1, 1)
        self.SetEndDate(...) # set dnd date (if not included, end date will be automatically be today's date) 
        self.SetCash(...) # set strategy cash (e.g. 100000)
        
        #TASK 2 (Define variables and data lists)
        # Request the symbols of the EquityNAV data from data_tools in csv format with daily resolution and store in a variable called nav_data
        self.nav_data = ...

        self.premia = {}            # create a dictionary of premium values by symbol
        self.discounts = {}         # create a dictionary of discount values by symbol
        self.min_period = 6*21      # define the minimum period for historical price-nav difference
        self.SetWarmUp(self.min_period*2)   # require at least 12 months of NAV data before trading, i.e. warm up algorithm
        
        self.universe_etfs = []     # subscribed ETFs
        
        self.opened_pos_max_cnt = 5 # set the maximum number of open positions at any given time to 5 

    def OnData(self, data):
        #TASK 3 (Subscribe to ETF data)
        if len(self.universe_etfs) == 0: # check universe_etfs is empty first
        # extract upper values of nav_data using keys and store in the variable universe_etfs
            if self.nav_data in data and data[self.nav_data]:
                self.universe_etfs = ...
                
                # add data
                for etf in self.universe_etfs:
                    etf_data = self.AddEquity(etf, Resolution.Daily)
                    etf_data.SetLeverage(10) # set leverage to 10
                    etf_data.SetFeeModel(data_tools.CustomFeeModel(self))
                    
                    # define premia and discounts
                    self.premia[etf] = deque()
                    self.discounts[etf] = deque()

        #TASK 4 (Store daily premium/discount data)
        # NAV data is available
        if self.nav_data in data and data[self.nav_data]:
            invested_cnt = len([x.Key.Value for x in self.Portfolio if x.Value.Invested])
            
            for etf in self.universe_etfs:
                # price data is available
                if etf in data and data[etf]:
                    nav = data[self.nav_data].GetProperty(etf)
                    price = data[etf].Value
                    diff = price - nav
                    
                    premium_flag = False    # last premium/discount flag
                    if ...
                        # note when premium occured
                        ...
                        ...
                    else:
                        # note when discount occured
                        ...
                    
                    if self.IsWarmingUp: # check if warm up is complete or not
                        continue
                    
        #TASK 5 (Check that at least one year of historical data is ready)
                    if len(self.premia[etf]) >= self.min_period and len(self.discounts[etf]) >= self.min_period:
                        
                        # etf is invested in and was traded at premium recently
                        if self.Portfolio[etf].Invested and premium_flag:
        #TASK 6 (Calculate premium mean and premium std)
                            premium_mean = ...
                            premium_std = ...

        #TASK 7 (Close the trade if the ETF premium at the close of future trading days move
        #away from its mean historical value by more than one standard deviation)
                            if ...
                                self.Liquidate()
                                
        #TASK 8 (etf is not invested in and was traded at discount recently)
                        elif ...
                            discount_mean = ...
                            discount_std = ...

        #TASK 9 (Discount at a close move away from its mean historical value by more than two standard deviations)
                            if ...
                                if invested_cnt < self.opened_pos_max_cnt and not self.Portfolio[etf].Invested:
                                    # there's a place for additional position and security if not held already
                                    self.SetHoldings(etf, 1/self.opened_pos_max_cnt)
