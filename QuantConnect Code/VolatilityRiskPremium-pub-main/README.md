# Volatility Risk Premium Strategy
The implied volatility from stock options is usually bigger than the actual historical volatility. The research, therefore, suggests the possibility to earn a systematic risk premium by selling at-the-money options short-term. Numerous papers show that this premium is quite substantial – selling put options gives average returns ranging from 0.5% to 1.5% per day.

However, strong caution is needed in implementing these short volatility strategies (strategies that exploit the volatility premium by selling volatility – usually selling put options or straddles) as the return distribution is very abnormal (put sellers historically could incur losses up to -800%). There is also a strong serial correlation in large negative days (from the put seller’s point of view); therefore, substantial margin reserves are needed when implementing these strategies, and returns are then much lower. We present a simple options strategy exploiting the option premium, with a backtested period, which includes the 1987 crash.

## Fundamental reason

Most researchers speculate that the volatility premium is caused by investors who strongly dislike negative returns and the high volatility on equity indexes and are therefore willing to pay a premium for portfolio insurance offered by puts.
Other researchers explain the volatility premium with the Peso problem (Black Swan event) – a situation when a rare but influential event could have reasonably happened (and removed the premium) but did not happen in the sample; this explanation is, however, highly unlikely as other researchers show that huge market crashes would have to occur every few years to remove the volatility premium altogether.

## Simple trading strategy

Each month, at-the-money straddle, with one month until maturity, is sold at the bid price with a 5% option premium, and an offsetting 15% out-of-the-money puts are bought (at the ask price) as insurance against a market crash. The remaining cash and received option premium are invested in the index. The strategy is rebalanced monthly.

## Source paper

https://papers.ssrn.com/sol3/papers.cfm?abstract_id=189840
