import pandas as pd
import requests


class YahooFinance:
    def __init__(self, symbol):
        self.end_point = "https://query1.finance.yahoo.com/v7/finance/chart"
        self.symbol = symbol


    def _fetch_short_ohlc(self, range, interval):
        url = self.end_point + "/" + self.symbol
        params = {"range": range, "interval": interval, "indicators": "quote", "includeTimestamps": True}

        r = requests.get(url, params=params, headers={"User-agent": "Mozilla/5.0"})

        return r.json()

    def generate_ohlc(self, range="7d", interval="5m"):
        r = self._fetch_short_ohlc(self.symbol, range, interval)

        bars = pd.DataFrame()

        bars["Open"]  = r["chart"]["result"][0]["indicators"]["quote"][0]["open"]
        bars["High"]  = r["chart"]["result"][0]["indicators"]["quote"][0]["high"]
        bars["Low"]   = r["chart"]["result"][0]["indicators"]["quote"][0]["low"]
        bars["Close"] = r["chart"]["result"][0]["indicators"]["quote"][0]["close"]

        bars.index = pd.to_datetime(r["chart"]["result"][0]["timestamp"], unit="s", utc=True)
        bars.index = bars.index.tz_convert("Asia/Tokyo")

        return bars.dropna()
