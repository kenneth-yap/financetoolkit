# Statistical Arbitrage with ETFs

Exchange-traded Funds (ETFs) are very popular trading and investment vehicles. An ETF is an investment fund traded on stock exchanges, much like stocks. An ETF holds assets such as stocks, commodities, or bonds, and trades close to its net asset value over the course of the trading day. ETFs track NAV very closely but cannot track it perfectly; therefore, they often trade at a small premium or discount to their NAV. These variations in discounts are predictive of future returns. A simple trading strategy could be constructed, which buys ETFs at high discounts and sells them after other market participants (arbitrageurs) close their discounts.

## Theory of Costly Arbitrage

Sophisticated traders might not always be able to profitably eliminate mispricing between an ETF’s NAV and its price. The theory of costly arbitrage says that mispricing could persist because noise traders can cause arbitrage to be prohibitively risky, and arbitrageurs don’t have unlimited resources and indefinite risk appetite to continue in arbitrage if prices shift too far away from fundamental values. Therefore, ETFs could trade at premium/discount to fund NAV, and it is possible to find profitable arbitrage opportunities as presented in this simple trading strategy.

## Simple Trading Strategy

The investment universe consists of all ETFs traded on the market. The investor uses data on historical End of Day premium/discounts from data providers (Bloomberg, Yahoo, etc.) or from ETF issuers to compute the average premium/discount and its standard deviation for each ETF. He/she then uses the “Intraday Value” of the ETF to compare the current premium/discount for each ETF and buys ETF at close if its discount at a close moves away from its mean historical value by more than two standard deviations. He/she closes the trade if the ETF premium at the close of future trading days moves away from its mean historical value by more than one standard deviation. The portfolio of current ETFs held is equally weighted.

Statistical Arbitrage with ETFs is related to other arbitrage/reversal strategies – it is also a type of “liquidity providing” strategy. As such, it usually benefits from increased volatility or a drop in liquidity and performs well during market crises.

### Reference Paper

http://papers.ssrn.com/sol3/papers.cfm?abstract_id=628061
