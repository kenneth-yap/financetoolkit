# Value and Momentum Factors across Asset Classes

The momentum strategy buys assets with the strongest past return (12-month or 1-month) and expects them to outperform assets with the lowest past return. Value strategy buys assets that are fundamentally cheap and intends to gain on the assets’ reversion to their long-term means. The combined long-short strategy allows the investor to secure market-neutral exposure to gains from both anomalies.

Several different approaches to this basic strategy exist. We present the Blitz and Vliet strategy as an example, and more strategies are mentioned in the “Other papers” section.

## Fundamental reason
Value and momentum strategies are very well documented by academics. These strong anomalies could be used together to enhance a portfolio’s profitability.

Using value and momentum on asset classes and not just inside one asset class can also increase strategy robustness.

## Simple trading strategy
Create an investment universe containing investable asset classes (could be US large-cap, mid-cap stocks, US REITS, UK, Japan, Emerging market stocks, US treasuries, US Investment grade bonds, US high yield bonds, Germany bonds, Japan bonds, US cash) and find a good tracking vehicle for each asset class (best vehicles are ETFs or index funds). Momentum ranking is done on price series. Valuation ranking is done on adjusted yield measure for each asset class. E/P (Earning/Price) measure is used for stocks, and YTM (Yield-to-maturity) is used for bonds. US, Japan, and Germany treasury yield are adjusted by -1%, US investment-grade bonds are adjusted by -2%, US High yield bonds are adjusted by -6%, emerging markets equities are adjusted by -1%, and US REITs are adjusted by -2% to get unbiased structural yields for each asset class. Rank each asset class by 12-month momentum, 1-month momentum, and by valuation and weight all three strategies (25% weight to 12m momentum, 25% weight to 1-month momentum, 50% weight to value strategy). Go long top quartile portfolio and go short bottom quartile portfolio.

## Hedge for stocks during bear markets
Yes - The strategy is fundamentally related to a class of trend-following CTA (managed futures) strategies which historically have a very good hedging/diversification abilities in times of market stress. For example, Exhibit 12 (and Figure 5) in a source research paper confirms this intuition and shows that strategy has positive performance even during times of the higher than average value of the VIX Index.

## Source paper
Blitz, Vliet: Global Tactical Cross-Asset Allocation: Applying Value and Momentum Across Asset Classes

http://papers.ssrn.com/sol3/papers.cfm?abstract_id=1079975

*Abstract*

In this paper we examine global tactical asset allocation (GTAA) strategies across a broad range of asset classes. Contrary to market timing for single asset classes and tactical allocation across similar assets, this topic has received little attention in the existing literature. Our main finding is that momentum and value strategies applied to GTAA across twelve asset classes deliver statistically and economically significant abnormal returns. For a long top-quartile and short bottom-quartile portfolio based on a combination of momentum and value signals we find a return exceeding 9% per annum over the 1986-2007 period. Performance is stable over time, also present in an out-of-sample period and sufficiently high to overcome transaction costs in practice. The return cannot be explained by implicit beta exposures or the Fama French and Carhart hedge factors. We argue that financial markets may be macro inefficient due to insufficient ‘smart money’ being available to arbitrage mispricing effects away.

## Other papers

Asness, Moskowitz, Pedersen: Value and Momentum Everywhere

http://papers.ssrn.com/sol3/papers.cfm?abstract_id=1363476

*Abstract*

Value and momentum ubiquitously generate abnormal returns for individual stocks within several countries, across country equity indices, government bonds, currencies, and commodities. We study jointly the global returns to value and momentum and explore their common factor structure. We find that value (momentum) in one asset class is positively correlated with value (momentum) in other asset classes, and value and momentum are negatively correlated within and across asset classes. Liquidity risk is positively related to value and negatively to momentum, and its importance increases over time, particularly following the liquidity crisis of 1998. These patterns emerge from the power of examining value and momentum everywhere simultaneously and are not easily detectable when examining each asset class in isolation.

Wang: Applying Value and Momentum Across Asset Classes in a Quantitative Tactical Asset Allocation Framework

http://papers.ssrn.com/sol3/papers.cfm?abstract_id=1726443

*Abstract*

We present a concise quantitative method for combining value and momentum strategies in a tactical asset allocation framework by directly comparing the attractiveness of valuations across a broad range of asset classes. Our broad and diverse publicly traded asset classes include public equity, investment grade and high yield bonds, cash, Treasury Inflation Protected Securities (TIPS), commodity and real estate. We refine the basic yield approach to valuation by standardizing the value signal using the Z-score. By tactically adjusting the weight of each asset class based on its perceived value and momentum signals, our model shows significant improvement in overall portfolio performance.

## Running the code
Copy the contents of `data_tools.py` and `exercise.py` into Quantconnect. Fill in the redacted part of the code (numbered TODO tasks with helper links) and run a backtest. Checking the [Quantconnect documentation](https://www.quantconnect.com/docs/v2/) is the best way to familiarise yourself with the syntax
