import asyncio
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .client import OpenWeatherClient


@api_view()
def weather_view(request):
    """ Вывод информации о погоде по населенному пункту/координатам """
    method = 'coord' if request.path == reverse('coord') else 'name'
    client = OpenWeatherClient(query=request.query_params, method=method)
    response, status = asyncio.run(client.do_request())
    return Response(response, status)
