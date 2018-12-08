import quandl


class QuandlDataSource:
    def __init__(self, api_key):
        quandl.ApiConfig.api_key = api_key

    def get_wti_daily(self):
        data = quandl.get("EIA/PET_RWTC_D", returns='numpy')
        return data

    def get_cpi_usa(self):
        data = quandl.get("RATEINF/CPI_USA", returns='numpy')
        return data

    def get_us_stock_daily(self, ticker):
        """
        Return daily stock data as a pandas DataFrame
        """
        data = quandl.get_table('WIKI/PRICES', ticker=[ticker], paginate=True)
        # quandl data is from most recent to least recent, invert it
        data = data.reindex(index=data.index[::-1])
        data = data.reset_index()
        return data

    def get_bitfinex_btcusd_daily(self):
        data = quandl.get('BITFINEX/BTCUSD', returns='numpy')
        return data

    def get_bitstamp_btcusd_daily(self):
        data = quandl.get('BITSTAMP/USD', returns='numpy')
        return data
