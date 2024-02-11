# Equity NAV
# NOTE: IMPORTANT: Data order must be ascending (datewise)
class EquityNAV(PythonData):
    def __init__(self):
        self.header_tickers = None
    
    def GetSource(self, config, date, isLiveMode):
        return SubscriptionDataSource("data.quantpedia.com/backtesting_data/equity/equity_nav.csv", SubscriptionTransportMedium.RemoteFile, FileFormat.Csv)

    def Reader(self, config, line, date, isLiveMode):
        data = EquityNAV()
        data.Symbol = config.Symbol
        
        # Header
        # date;SPY;MDY;DIA;QQQ;IWM;VTI;DVY;PDP;MTUM;QUAL;IVW;IVW;IVE;IWN;SUSA;PBW;GDX
        if not line[0].isdigit():
            if not self.header_tickers:
                self.header_tickers = line.split(';')[1:] # date offset
            return None
        
        if not self.header_tickers:
            return None
            
        # parse value for every ticker
        split = line.split(';')
        data.Time = datetime.strptime(split[0], "%Y-%m-%d") + timedelta(days=1) # 1 day lag
        
        for i, ticker in enumerate(self.header_tickers):
            data[ticker] = float(split[i+1]) if (split[i+1] and len(split[i+1]) != 0 and split[i+1] != "") else None

        return data

# Custom fee model.
class CustomFeeModel(FeeModel):
    def GetOrderFee(self, parameters):
        fee = parameters.Security.Price * parameters.Order.AbsoluteQuantity * 0.00005
        return OrderFee(CashAmount(fee, "USD"))
