from stock import Stock
import math
from news import News
from message_controller import MessageController

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
NOTABLE_PERCENTAGE_DIFF = 5.0


def get_percentage_diff(end_value, start_value):
    return (end_value - start_value) / start_value * 100


def get_stock_msg(stock_articles):
    stock_dir_img = "🔺"
    if percentage_diff < 0:
        stock_dir_img = "🔻"
    stock_base = f"{STOCK}: {stock_dir_img}{'%.2f' % percentage_diff}%\n"
    msg = [f"{stock_base}Headline: {article['title']}\nBrief: {article['description']}\n\n" if article['description']
           else f"{stock_base}Headline: {article['title']}\n\n"
           for article in stock_articles]
    return ''.join(msg)


stock_api = Stock()
two_day_close = stock_api.get_two_day_close(STOCK)
end_data = two_day_close[0]
start_data = two_day_close[1]
percentage_diff = get_percentage_diff(end_data["daily_close"], start_data["daily_close"])
if math.fabs(percentage_diff) > NOTABLE_PERCENTAGE_DIFF:
    news_api = News()
    stock_msg = get_stock_msg(news_api.search(COMPANY_NAME)[:3])
    messenger = MessageController()
    messenger.send_sms(stock_msg)
