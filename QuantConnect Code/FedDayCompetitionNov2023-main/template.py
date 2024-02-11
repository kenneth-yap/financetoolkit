# Template for the CUATS Fed Day Social Algorithmic Trading Competition
# Start and end date: you may change these. Your algorithm will be run live on the day of the Fed Day announcement, starting at 17:00 and ending at 21:00 at market close. You may use any tradeable instrument across all assets of the US markets available on QuantConnect in constructing your trading strategy.  Starting with a cash balance of $100,000, develop a trading algorithm that achieves the maximum profit with a maximum drawdown of 10%; the strategy should be benchmarked against the S&P500 Index. 
# Cash: do not change this
# fee and execution models: do not add a fee/execution model. Quantconnect defaults to using their standard fee/execution model
# leverage: you can use up to 10x leverage. You can set leverage globally as in this template with SetLeverage(x) or you can specify it for specific trades with SetHoldings("SPY", x)
# Do make use of the algorithmic trading strategies (EMA, Pairs Trading, Statistical Arbitrage in ETFs) and indicators (Bollinger Bands, RSI, MACD) we have covered in the Coding Sessions on constructing your algorithm, taking particular note of the high volatility typically experienced on Fed Days around the announcement and press conference periods and exploring ways to capture this market behaviour to make a profitable intraday trading strategy.
# backest: you may wish to backtest your algorithm on prior Fed Days (2023: 20 Sep, 26 Jul, 14 Jun, 3 May, 22 Mar, 1 Feb) both this year and in previous years to test its performance.
# Got questions? Put them on the discussion page of this repo (https://github.com/CUATS/FedDayCompetitionNov2023/discussions)


from AlgorithmImports import *

class MyTradingAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2023, 9, 20)    #Set Start Date
        self.SetEndDate(2023, 9, 21)    #Set End Date
        self.SetCash(100000)             #Set Strategy Cash

    def OnSecuritiesChanged(self, changes):
        for security in changes.AddedSecurities:
            security.SetLeverage(10)

    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. 
        Each new data point will be pumped in here.'''
        pass 
