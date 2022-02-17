import os
import aiohttp


class OpenWeatherClient:
    def __init__(self, query, method='name'):
        self.key = os.environ.get("OPENWEATHER_API_KEY")
        self.query = query
        self.method = method

    def generate_request_url(self):
        """ Функция генерации урла запроса к OpenWeather """
        url = 'http://api.openweathermap.org/data/2.5/weather'
        if self.method == 'name':
            if self.query.get("city"):
                url += f"?q={self.query.get('city')}"
            else:
                return None, "неверный запрос — укажите город"
        elif self.method == 'coord':
            if all((self.query.get("lat"), self.query.get("lon"))):
                url += f"?lat={self.query.get('lat')}&lon={self.query.get('lon')}"
            else:
                return None, "неверный запрос — укажите обе координаты"
        else:
            return None, "неверный метод"

        if self.query.get('units') in ('standard', 'imperial', 'metric'):
            url += f"&units={self.query.get('units')}"
        else:
            url += f"&units={os.environ.get('DEFAULT_UNITS')}"

        url += f"&lang={self.query.get('lang') if self.query.get('lang') else os.environ.get('DEFAULT_LANG')}"
        url += f"&appid={self.key}"

        return url, "good"

    async def do_request(self):
        """ Функция выполнения запроса """
        url, message = self.generate_request_url()
        if message == 'good':
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url) as response:
                    r = await response.json()
                    if response.status == 200:
                        return {
                            "city": {
                                "country": r["sys"].get("country", "не определено"),
                                "name": r["name"] if r["name"] else "не определено"
                            },
                            "weather": {
                                "temp": r["main"]["temp"],
                                "temp_min": r["main"]["temp_min"],
                                "temp_max": r["main"]["temp_max"],
                                "description": r["weather"][0]["description"]
                            }
                        }, response.status
                    else:
                        return {"message": r.get('message')}, response.status
        else:
            return {"message": message}, 400
