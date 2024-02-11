
from QuantConnect.Indicators import *
import decimal as d

### <summary>
### In this example we are looking for price to breakout above the bollinger bands
### and look to buy when we see that. We hold our position until price touches the 
### middle band of the bollinger bands.
###

class BollingerBreakoutAlgorithm(QCAlgorithm):

    def Initialize(self):

        self.SetStartDate(2016, 6, 1)  #Set Start Date
        self.SetEndDate(2017, 7, 1)    #Set End Date
        self.SetCash(10000)             #Set Strategy Cash
        
        # define crypto we want to trade on
        # ETHUSD, LTCUSD or BTCUSD
        self.target_crypto = "ETHUSD"
        
        self.AddCrypto(self.target_crypto, Resolution.Daily)
        
        # create a bollinger band
        self.Bolband = self.BB(self.target_crypto, 20, 2, MovingAverageType.Simple, Resolution.Daily)

        # Plot Bollinger band
        self.PlotIndicator(
            "Indicators",
            self.Bolband.LowerBand,
            self.Bolband.MiddleBand,
            self.Bolband.UpperBand,
        )
 
        # create a momentum indicator over 3 days
        self.mom = self.MOM(self.target_crypto, 5)
        
        # Plot Momentum
        self.PlotIndicator(
            "Indicators",
            self.mom
        )

        # set warmup period
        self.SetWarmUp(20)
        

    def OnData(self, data):
        
        holdings = self.Portfolio[self.target_crypto].Quantity
        price = self.Securities[self.target_crypto].Close
        mom = self.mom.Current.Value
        
        # buy if price closes above upper bollinger band
        if holdings <= 0 and price > self.Bolband.UpperBand.Current.Value:
                    self.SetHoldings(self.target_crypto, 1.0)
        
        # sell if price closes below middle bollinger band
        if holdings > 0 and price < self.Bolband.MiddleBand.Current.Value:
                self.Liquidate()


