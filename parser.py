import requests
from bs4 import BeautifulSoup

WeatherURL = "https://sinoptik.ua/погода-"


def get_html(url):
    html = requests.get(url).text
    return html


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
    print("Ночь:  {0} {1}".format(weather_data[0]["night"][0], weather_data[0]["night"][1]))
    print("Утро:  {0} {1}".format(weather_data[0]["morning"][0], weather_data[0]["morning"][1]))
    print("День:  {0} {1}".format(weather_data[0]["day"][0], weather_data[0]["day"][1]))
    print("Вечер: {0} {1}".format(weather_data[0]["evening"][0], weather_data[0]["evening"][1]))
    print(weather_data[1])


def main():
    city = input("Введите город: ").lower()
    weather_city_url = WeatherURL + city
    weather_html = get_html(weather_city_url)
    weather_data = get_weather(weather_html)
    print_weather(weather_data)

if __name__ == '__main__':
    main()
