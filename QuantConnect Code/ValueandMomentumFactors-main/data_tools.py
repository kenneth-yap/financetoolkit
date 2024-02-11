#region imports
from AlgorithmImports import *
#endregion
# Bond yields
class QuandlAAAYield(PythonQuandl):
    def __init__(self):
        self.ValueColumnName = 'BAMLC0A1CAAAEY'

class QuandlHighYield(PythonQuandl):
    def __init__(self):
        self.ValueColumnName = 'BAMLH0A0HYM2EY'

# Quantpedia bond yield data.
# NOTE: IMPORTANT: Data order must be ascending (datewise)
class QuantpediaBondYield(PythonData):
    def GetSource(self, config, date, isLiveMode):
        return SubscriptionDataSource("data.quantpedia.com/backtesting_data/bond_yield/{0}.csv".format(config.Symbol.Value), SubscriptionTransportMedium.RemoteFile, FileFormat.Csv)

    def Reader(self, config, line, date, isLiveMode):
        data = QuantpediaBondYield()
        data.Symbol = config.Symbol
        
        if not line[0].isdigit(): return None
        split = line.split(',')
        
        data.Time = datetime.strptime(split[0], "%Y-%m-%d") + timedelta(days=1)
        data['yield'] = float(split[1])
        data.Value = float(split[1])

        return data
        
# Country PE data
# NOTE: IMPORTANT: Data order must be ascending (date-wise)
from dateutil.relativedelta import relativedelta

class CountryPE(PythonData):
    def GetSource(self, config, date, isLiveMode):
        return SubscriptionDataSource("data.quantpedia.com/backtesting_data/economic/country_pe.csv", SubscriptionTransportMedium.RemoteFile, FileFormat.Csv)

    def Reader(self, config, line, date, isLiveMode):
        data = CountryPE()
        data.Symbol = config.Symbol
        
        if not line[0].isdigit(): return None
        split = line.split(';')
        
        data.Time = datetime.strptime(split[0], "%Y") + relativedelta(years=1)
        self.symbols = ['Argentina','Australia','Austria','Belgium','Brazil','Canada','Chile','China','Egypt','France','Germany','Hong Kong','India','Indonesia','Ireland','Israel','Italy','Japan','Malaysia','Mexico','Netherlands','New Zealand','Norway','Philippines','Poland','Russia','Saudi Arabia','Singapore','South Africa','South Korea','Spain','Sweden','Switzerland','Taiwan','Thailand','Turkey','United Kingdom','United States']
        index = 1
        for symbol in self.symbols:
            data[symbol] = float(split[index])
            index += 1
            
        data.Value = float(split[1])
        return data

# Quandl "value" data
class QuandlValue(PythonQuandl):
    def __init__(self):
        self.ValueColumnName = 'Value'
        
# Quantpedia PE ratio data.
# NOTE: IMPORTANT: Data order must be ascending (datewise)
class QuantpediaPERatio(PythonData):
    def GetSource(self, config, date, isLiveMode):
        return SubscriptionDataSource("data.quantpedia.com/backtesting_data/economic/{0}.csv".format(config.Symbol.Value), SubscriptionTransportMedium.RemoteFile, FileFormat.Csv)

    def Reader(self, config, line, date, isLiveMode):
        data = QuantpediaPERatio()
        data.Symbol = config.Symbol
        
        if not line[0].isdigit(): return None
        split = line.split(';')
        
        data.Time = datetime.strptime(split[0], "%Y-%m-%d") + timedelta(days=1)
        data['pe_ratio'] = float(split[1])
        data.Value = float(split[1])

        return data

# Quantpedia bond yield data.
# NOTE: IMPORTANT: Data order must be ascending (datewise)
class QuantpediaBondYield(PythonData):
    def GetSource(self, config, date, isLiveMode):
        return SubscriptionDataSource("data.quantpedia.com/backtesting_data/bond_yield/{0}.csv".format(config.Symbol.Value), SubscriptionTransportMedium.RemoteFile, FileFormat.Csv)

    def Reader(self, config, line, date, isLiveMode):
        data = QuantpediaBondYield()
        data.Symbol = config.Symbol
        
        if not line[0].isdigit(): return None
        split = line.split(',')
        
        data.Time = datetime.strptime(split[0], "%Y-%m-%d") + timedelta(days=1)
        data['yield'] = float(split[1])
        data.Value = float(split[1])

        return data
        
# Quantpedia data.
# NOTE: IMPORTANT: Data order must be ascending (datewise)
class QuantpediaFutures(PythonData):
    def GetSource(self, config, date, isLiveMode):
        return SubscriptionDataSource("data.quantpedia.com/backtesting_data/futures/{0}.csv".format(config.Symbol.Value), SubscriptionTransportMedium.RemoteFile, FileFormat.Csv)

    def Reader(self, config, line, date, isLiveMode):
        data = QuantpediaFutures()
        data.Symbol = config.Symbol
        
        if not line[0].isdigit(): return None
        split = line.split(';')
        
        data.Time = datetime.strptime(split[0], "%d.%m.%Y") + timedelta(days=1)
        data['back_adjusted'] = float(split[1])
        data['spliced'] = float(split[2])
        data.Value = float(split[1])

        return data
