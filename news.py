import requests
import os


class News:
    """ Interface to the News API"""
    def __init__(self):
        self.api_key = os.environ.get("NEWS_API_KEY")
        self.url_base = "https://newsapi.org"
        self.search_url = self.url_base + "/v2/everything"

    def search(self, query_string):
        parameters = {
            "qInTitle": query_string,
            "apiKey": self.api_key,
        }
        search_result = requests.get(url=self.search_url, params=parameters)
        search_result.raise_for_status()
        return search_result.json()['articles']
