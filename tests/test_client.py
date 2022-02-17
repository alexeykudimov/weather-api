import asyncio
import os
import pytest
from weather.client import OpenWeatherClient


@pytest.mark.parametrize("query, method, expected_url",
                         [({"city": "Moscow", "units": "metric"}, "name",
                           f"http://api.openweathermap.org/data/2.5/weather"
                           f"?q=Moscow&units=metric&lang={os.environ.get('DEFAULT_LANG')}"
                           f"&appid={os.environ.get('OPENWEATHER_API_KEY')}"),
                          ({"city": "Vladimir", "lang": "en"}, "name",
                           f"http://api.openweathermap.org/data/2.5/weather"
                           f"?q=Vladimir&units={os.environ.get('DEFAULT_UNITS')}&lang=en"
                           f"&appid={os.environ.get('OPENWEATHER_API_KEY')}"),
                          ({"lat": 20, "lon": 50}, "coord",
                           f"http://api.openweathermap.org/data/2.5/weather"
                           f"?lat=20&lon=50&units={os.environ.get('DEFAULT_UNITS')}"
                           f"&lang={os.environ.get('DEFAULT_LANG')}"
                           f"&appid={os.environ.get('OPENWEATHER_API_KEY')}"),
                          ({"lat": 50, "lon": 40, "units": "imperial", "lang": "de"}, "coord",
                           f"http://api.openweathermap.org/data/2.5/weather"
                           f"?lat=50&lon=40&units=imperial&lang=de&appid={os.environ.get('OPENWEATHER_API_KEY')}")])
def test_good_generate_url(query, method, expected_url):
    """ тест на правильность генерации урла для запроса """
    client = OpenWeatherClient(query, method)
    url, _ = client.generate_request_url()
    assert url == expected_url


@pytest.mark.parametrize("query, method, expected_message",
                         [({"lat": 40, "lon": 40}, "name", "неверный запрос — укажите город"),
                          ({"lat": 40}, "coord", "неверный запрос — укажите обе координаты"),
                          ({"city": "Москва"}, "coord", "неверный запрос — укажите обе координаты")])
def test_fail_generate_url(query, method, expected_message):
    """ тест неверных запросов """
    client = OpenWeatherClient(query, method)
    _, message = client.generate_request_url()
    assert message == expected_message


def test_do_request(monkeypatch):
    """ проверка работоспособности функции выполнения запроса к OpenWeather (mock) """
    is_executed = False

    async def mock_do_request(*args, **kwargs):
        nonlocal is_executed
        is_executed = True

    monkeypatch.setattr("weather.client.OpenWeatherClient.do_request", mock_do_request)

    client = OpenWeatherClient({"city": "Moscow", "units": "metric"})
    asyncio.run(client.do_request())

    assert is_executed
