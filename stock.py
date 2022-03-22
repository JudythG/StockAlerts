import requests
from datetime import date, timedelta
import os

ONE_DAY_DELTA = timedelta(hours=24)


def get_prev_day(day, time_series):
    """ returns the previous day the stock market was open in date format """
    prev_day = day - ONE_DAY_DELTA
    while time_series.get(prev_day.isoformat()) is None:
        prev_day = prev_day - ONE_DAY_DELTA
    return prev_day


class Stock:
    """ Interface to for Alpha Vantage's stock data API """
    def __init__(self):
        self.api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
        self.url = "https://www.alphavantage.co/query"

    def get_two_day_close(self, stock_code):
        """ Returns date and close value for the last two days in a list with end_data preceding start_data.
            End and start data are a dictionary with these fields:
                "day" the date
                "daily_close" that date's daily close value as a float
            """
        stock_parameters = {
            "function": "TIME_SERIES_DAILY",
            "symbol": stock_code,
            "apikey": self.api_key
        }
        daily_data = requests.get(url=self.url, params=stock_parameters)
        daily_data.raise_for_status()
        time_series_daily = daily_data.json()["Time Series (Daily)"]

        # end data -> workday before today's date and daily close
        end_data = {
            "day": get_prev_day(date.today(), time_series_daily)
        }
        end_data["daily_close"] = float(time_series_daily[end_data["day"].isoformat()]["4. close"])

        # start data -> workday before end_data.day's date and daily close
        start_data = {
            "day": get_prev_day(end_data["day"], time_series_daily)
        }
        start_data["daily_close"] = float(time_series_daily[start_data["day"].isoformat()]["4. close"])
        return [end_data, start_data]
