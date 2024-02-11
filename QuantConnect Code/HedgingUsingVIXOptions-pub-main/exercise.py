# The investment universe consists of a stock/bond portfolio with a proportion of 60-percent stocks and 40-percent bonds.
# Stocks are represented by the SPDR S&P 500 ETF Trust (SPY) and bonds by the iShares 7-10 Year Treasury Bond ETF (IEF). 
# The strategy firstly invests 0-100 basis points (bsp) in the desired VIX call option, then allocates 60 percent of the 
# portfolio to the SPY and the remaining 40 percent to the IEF. The option is bought at the level of 135% of the moneyness
# of the underlying VIX futures price. The strategy is systematically purchasing an equal amount in one-month, two-month, 
# three-month and four-month VIX call options on VIX futures. If the VIX Index is between 15 and 30, the weight of VIX calls 
# in the portfolio is 1%. If the VIX Index is between 30 and 50, the weight in the portfolio is 0,5%. If the VIX Index is over
# 50 or under 15, then the weight of options in the portfolio is 0%. Each month, on the day before expiration, the options are
# rolled to the appropriate expiry. VIX call options are purchased at the offer and sold at the bid to keep the assumptions
# conservative. The options are held to maturity and closed the Tuesday afternoon before the Wednesday morning of VIX futures
# and options expiration. If the contracts have any intrinsic value, they are sold at the bid price, and the cash is used at 
# the end of the month to rebalance the stock/bond portion of the portfolio.

# Advice:
#   - To view algorithm errors, toggle Console view below when in Backtesting
#   - To print out debugging messages (the difference is only in colours), use
#     `self.Debug(...)` or `self.Error(...)` - See LINK 1
#   - To stop backtesting, go to Organisation (tab #2) -> Resources -> Stop

from AlgorithmImports import *

class PortfolioHedgingUsingVIXOptions(QCAlgorithm):

    def Initialize(self):
        # TODO 1: (LINK 2)
        # Set up conditions:
        #   - cash (1000000)
        #   - start date (1/1/2010)
        
        self.SetStartDate(...)
        self.SetCash(...)
        
        # TODO 2: (API)
        # Set up holdings:
        #   - on S&P ("SPY")
        #   - with minutely resolution
        #   - with leverage of 5 (LINK 3)
        # Do the same for IEF(bond)
        # Links: _1_ _2_
        
        data = self.AddEquity(...)
        data.SetLeverage(...)
        self.spy = data.Symbol
        
        data = self.AddEquity(...)
        data.SetLeverage(...)
        self.ief = data.Symbol 
        
        # TODO 3: Add VIX options with option filter(LINK4, ~5 lines)
        #   - Use ticker 'VIXY' for both options and VIX
        #   - For VIX itself, set leverage for it to 5, and save it as self.vix.
        #   - Minute resolution
        #   - Option filter: minStrike = -20, maxStrike = 20, minExpiry = 25, maxExpiry = 35
        
        

        
    def OnData(self,slice):
        for i in slice.OptionChains:
            chains = i.Value

            # invested is a list of all instruments that the strategy is currently invested in.
            invested = [x.Key for x in self.Portfolio if x.Value.Invested]
            
            # TODO 4: Write a code to check if you hold options or not (~ 2 more lines)
            #   - hint: having a maximum of 2 positions means SPY and IEF are opened, which means options expired.
            #   - If you do not , this means the current option holdings have expired.
            #   - In this case, get the list of all eligible call options. If none, return.
            #   - LINK 5
            if len(invested) <= 2:
                
                # TODO 5: Execute strategy (~12 lines)
                #   (1) Gets options underlying price + expiries + strike price
                #   (2) Filter according to expiry date(closest to 1 month, 2 month, 3 month, 4 month)
                #   (3) Further filter out OTM options with level of moneyness closest to 135% of underlying(VIX)
                #   (4) Calculate weighting of the call options based on underlying:
                #           - 1% if underlying belongs to [15,30]
                #           - 0.5% if underlying belongs to [30,50]
                #           - 0 otherwise
                underlying_price = ...
                expiries = ...
                strikes = ...

                # Determine out-of-the-money strike.
                otm_strike = min(strikes, key = lambda x:abs(x - (float(1.35) * underlying_price)))

                # Option weighting.
                weight = 
                options_q = 
                if...
                elif...
                if...

                
                # TODO 6: Execute strategy (~10 lines)
                #   (1) Get options corresponding to each expiry date.
                #   (2) Loop through the options based on expiry date, and
                #   (3) Purchase accordingly. Set maximum leverage to 5(using BuyingPowerModel(), LINK 3).
                
                #Filter out the expiries

                for...
                    if ...
                    elif ...
                    if weight != 0:
                        options_q = ...
                        self.Securities[...] = ...
                        self.Buy(...)
                
                # TODO 7: Execute strategy (LINK 6, ~2 lines)
                # Buy spx and ief after buying options in 60:40 ratio of the left-over margin.
                    
                
                
          
#LINKS:
#1: https://www.quantconnect.com/docs/v2/cloud-platform/projects/debugging
#2: https://www.quantconnect.com/docs/v2/writing-algorithms/initialization?ref=v1
#3: https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/buying-power
#4: https://www.quantconnect.com/tutorials/introduction-to-options/quantconnect-options-api
#5: https://www.w3schools.com/python/ref_func_filter.asp
#6: https://www.quantconnect.com/docs/v2/writing-algorithms/trading-and-orders/position-sizing
