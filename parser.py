import requests
import json
from bs4 import BeautifulSoup

WeatherURL = "https://sinoptik.ua/погода-"
BtcURL = "https://blockchain.info/ru/ticker"
CurrencyUrl = "https://api.fixer.io/latest?base="
UahURL = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"

def get_html(url):
    html = requests.get(url).text
    return html


# Weather
def get_weather(html):
    soup = BeautifulSoup(html, "html.parser")
    data = []
    i = 8
    while i > 0:
        data.append(soup.select(".temperature .p{0}".format(i))[0].getText())
        i -= 1
    description = soup.select(".description")[0].getText().strip()
    pretty_data = {"night": [data[-1], data[-2]],
                   "morning": [data[-3], data[-4]],
                   "day": [data[-5], data[-6]],
                   "evening": [data[-7], data[-8]]}

    return [pretty_data, description]


def print_weather(weather_data):
    print("-Погода-")
    print("Ночь:  {0} {1}".format(weather_data[0]["night"][0], weather_data[0]["night"][1]))
    print("Утро:  {0} {1}".format(weather_data[0]["morning"][0], weather_data[0]["morning"][1]))
    print("День:  {0} {1}".format(weather_data[0]["day"][0], weather_data[0]["day"][1]))
    print("Вечер: {0} {1}".format(weather_data[0]["evening"][0], weather_data[0]["evening"][1]))
    print(weather_data[1])
    print()


# Bitcoin
def parse_bitcoin(raw_data):
    json_parsed = json.loads(raw_data)
    buy = json_parsed["USD"]["buy"]
    sell = json_parsed["USD"]["sell"]
    return [buy, sell]


def print_bitcoin(value):
    print("-Курс Bitcoin-")
    print("Покупка: $", value[0],)
    print("Продажа: $", value[1])
    print()


# Currency
def parse_currency(base_currency):
    if base_currency == "uah":
        raw_json = get_html(UahURL)
        data = json.loads(raw_json)
        exchange_rate_usd = [data[0]["buy"], data[0]["sale"]]
        exchange_rate_eur = [data[1]["buy"], data[1]["sale"]]
        exchange_rate_rur = [data[2]["buy"], data[2]["sale"]]
        return [exchange_rate_usd, exchange_rate_eur, exchange_rate_rur, base_currency]
    else:
        pass


def print_exchange_rate_currency(exchange_rate):
    print("\tПокупка \tПродажа")
    print("USD:\t{0}\t{1}".format(exchange_rate[0][0], exchange_rate[0][1]))
    print("EUR:\t{0}\t{1}".format(exchange_rate[1][0], exchange_rate[0][1]))
    print("RUR:\t{0}\t{1}".format(exchange_rate[2][0], exchange_rate[2][1]))
    print()


def main():
    base_currency = input("Введите базовую валюту: ")
    exchange_rate = parse_currency(base_currency)
    print_exchange_rate_currency(exchange_rate)

    btc_json = get_html(BtcURL)
    btc_value = parse_bitcoin(btc_json)
    print_bitcoin(btc_value)

    city = input("Введите город: ").lower()
    weather_city_url = WeatherURL + city
    weather_html = get_html(weather_city_url)
    weather_data = get_weather(weather_html)
    print_weather(weather_data)


if __name__ == '__main__':
    main()
