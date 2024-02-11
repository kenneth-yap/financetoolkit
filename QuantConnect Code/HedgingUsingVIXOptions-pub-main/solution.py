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

from AlgorithmImports import *

class PortfolioHedgingUsingVIXOptions(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetCash(1000000)
        
        data = self.AddEquity("SPY", Resolution.Minute)
        data.SetLeverage(5)
        self.spy = data.Symbol
        
        data = self.AddEquity("IEF", Resolution.Minute)
        data.SetLeverage(5)
        self.ief = data.Symbol
        
        data = self.AddEquity("VIXY", Resolution.Minute)
        data.SetLeverage(5)
        self.vix = data.Symbol
        
        option = self.AddOption('VIXY', Resolution.Minute)
        option.SetFilter(-20, 20, 25, 35)
        
    def OnData(self,slice):
        for i in slice.OptionChains:
            chains = i.Value

            # Max 2 positions - spy and ief are opened. That means option expired.
            invested = [x.Key for x in self.Portfolio if x.Value.Invested]
            if len(invested) <= 2:
                calls = list(filter(lambda x: x.Right == OptionRight.Call, chains))
                
                if not calls: return
            
                underlying_price = self.Securities[self.vix].Price
                expiries = [i.Expiry for i in calls]
                strikes = [i.Strike for i in calls]
                
                # Determine out-of-the-money strike.
                otm_strike = min(strikes, key = lambda x:abs(x - (float(1.35) * underlying_price)))

                # Option weighting.
                weight = 0.0
                options_q = 0
                    
                if underlying_price >= 15 and underlying_price <= 30:
                    weight = 0.01
                elif underlying_price > 30 and underlying_price <= 50:
                    weight = 0.005     
                if weight != 0: 
                    options_q = int((self.Portfolio.MarginRemaining * weight) / (underlying_price * 100))
                
                expiry = min(expiries, key=lambda x: abs((x.date() - self.Time.date()).days - 30))
                expiry2 = min(expiries, key=lambda x: abs((x.date() - self.Time.date()).days - 60))
                expiry3 = min(expiries, key=lambda x: abs((x.date() - self.Time.date()).days - 90))
                expiry4 = min(expiries, key=lambda x: abs((x.date() - self.Time.date()).days - 120))
                filtered_expiries = [expiry,expiry2,expiry3,expiry4]
                otm_calls = [[i for i in calls if i.Expiry == expiry and i.Strike == otm_strike] for expiry in filtered_expiries]
                for otm_call in otm_calls:
                    if otm_call:
                            # Set max leverage.
                            self.Securities[otm_call[0].Symbol].MarginModel = BuyingPowerModel(5)
                        
                            # Sell out-the-money call.
                            self.Buy(otm_call[0].Symbol, options_q)
                        
                self.SetHoldings(self.spy, 0.6)
                self.SetHoldings(self.ief, 0.4)
