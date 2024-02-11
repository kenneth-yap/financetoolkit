# Description:
#
# Each month, at-the-money straddle, with one month until maturity, is sold at
# the bid price with a 5% option premium, and an offsetting 15%
# out-of-the-money puts are bought (at the ask price) as insurance against a
# market crash. The remaining cash and received option premium are invested in
# the index. The strategy is rebalanced monthly.
#
# Advice:
#   - To view algorithm errors, toggle Console view below when in Backtesting
#   - To print out debugging messages (the difference is only in colours), use
#     `self.Debug(...)` or `self.Error(...)`
#   - To stop backtesting, go to Organisation (tab #2) -> Resources -> Stop

class VolatilityRiskPremiumEffect(QCAlgorithm):

    def Initialize(self):

        # To debug, print logs and errors (the difference is only in colours),
        # use self.Debug(...), self.Info(...), self.Error(...)

        # TODO:1 (Strategy)
        # Set up conditions:
        #   - cash (e.g 10000)
        #   - time period (e.g 1/5/2010 to 1/5/2011)
        # Links: _8_
        self.SetCash(...)
        self.SetStartDate(...)
        self.SetEndDate(...)

        # TODO:2 (API)
        # Set up an option:
        #   - on S&P ("SPY")
        #   - with daily resolution
        #   - with filter on +-20 price relative to strike price, 30+-5 days expiry date
        # Links: _1_ _2_
        data = self.AddEquity(...)
        option = self.AddOption(...)

        # TODO:3 (Python)
        # Save necessary information that you intend to use in the strategy
        ...

        # Benchmark
        self.benchmarkTicker = self.symbol
        self.SetBenchmark(self.symbol)
        self.initBenchmarkPrice = None


    def OnData(self,data):

        self.UpdateBenchmarkValue()
        self.Plot('Strategy Equity', self.benchmarkTicker, self.benchmarkValue)

        # Go through options chains _3_ (expect one or zero option chains here)
        for chains in data.OptionChains.Values:

            if not self.Portfolio.Invested:

                # TODO:4 (Python)
                # Divide option chains into call and put options and require
                # both to be non-empty, otherwise exit
                # Links: _5_
                calls = list(...)
                puts = list(...)

                # TODO:5 (API)
                # Get security price for the selected ticker
                # Links: _4_
                underlying_price = ...

                # TODO:6 (Python)
                # Given the list of puts, select:
                #   (1) the closest expiry date to the predefined period (e.g 30 days)
                #   (2) at the money strike price (i.e closest to the `underlying_price`)
                #   (3) 15% out-of-money strike price for the hedging put option
                # Links: _2_
                expiry = ...
                atm_strike = ...
                otm_strike = ...

                # TODO:7 (Python)
                # Collect the strategy prescribed options that match selected parameters
                atm_calls = list(...)
                atm_puts = list(...)
                otm_puts = list(...)

                # When all relevant options are available
                if atm_calls and atm_puts and otm_puts:

                    # TODO:8 (API)
                    # Use "remaining margin" to determine quantity of options to trade
                    # Hint: options contain 100 shares
                    # Links: _6_
                    options_quantity = ...

                    # TODO:9 (Strategy)
                    # Perform trades:
                    # (1) sell at-the-money straddle
                    # (2) buy 15% out-of-the-money put
                    # (3) buy index with remaining funds
                    # Links: _0_ _7_
                    self.Sell(...)
                    self.Buy(...)
                    self.SetHoldings(...)

            # Liquidate assets if not holding options (they are expired or not bought)
            invested = [x.Key for x in self.Portfolio if x.Value.Invested]
            if len(invested) == 1:
                self.Liquidate(self.symbol)


    # Benchmark
    def UpdateBenchmarkValue(self):
        ''' Simulate investing in the Benchmark '''

        self.benchmarkExposure = 1

        if self.initBenchmarkPrice == None:
            self.initBenchmarkCash = self.Portfolio.Cash
            self.initBenchmarkPrice = self.Benchmark.Evaluate(self.Time)
            self.benchmarkValue = self.initBenchmarkCash
        else:
            currentBenchmarkPrice = self.Benchmark.Evaluate(self.Time)
            lastReturn = ((currentBenchmarkPrice / self.initBenchmarkPrice) - 1) * self.benchmarkExposure
            self.benchmarkValue = (1 + lastReturn) * self.initBenchmarkCash


# Links:
# _0_ https://www.quantconnect.com/docs/algorithm-reference/overview#Overview-Introduction
# _1_ https://www.quantconnect.com/docs/data-library/options#Options-Requesting-Options-Data---Universe
# _2_ https://www.quantconnect.com/tutorials/api-tutorials/using-options-in-quantconnect#Using-Options-in-QuantConnect-Filter-Contracts
# _3_ https://www.quantconnect.com/docs/data-library/options#Options-Using-Options-Data
# _4_ https://www.quantconnect.com/docs/algorithm-reference/securities-and-portfolio#Securities-and-Portfolio-Introduction
# _5_ https://www.quantconnect.com/tutorials/api-tutorials/using-options-in-quantconnect#Using-Options-in-QuantConnect-Select-Contracts
# _6_ https://www.quantconnect.com/docs/algorithm-reference/securities-and-portfolio#Securities-and-Portfolio-Introduction
# _7_ https://www.quantconnect.com/docs/algorithm-reference/trading-and-orders#Trading-and-Orders-Automatic-Position-Sizing-SetHoldings
# _8_ https://www.quantconnect.com/docs/algorithm-reference/initializing-algorithms#Initializing-Algorithms-Setting-Dates

