from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page
from .models import Rate
import requests
import datetime


def index(request):
    """
    Начальная страница; содержит запись с командой для перехода на страницу получения курса доллара к рублю.
    Возвращает HttpResponse
    """
    return HttpResponse('Call "/get-current-usd" to get the current dollar to ruble exchange rate.')


@cache_page(10)
def get_current_usd(request):
    """
    Страница вывода курса доллара к рублю, выводится по запросу "/get-current-usd";
    содержит json структуру с записями:
        Rate_USD - текущий курс доллара к рублю
        Update_Rate_DataTime - время последнего обновления курса
        Request_DataTime - время выполнения запроса,
    а также содержит 10 последних запросов. Между каждым запросом предусмотрена пауза 10 секунд.
    Возвращает JsonResponse
    """
    rate_list = Rate.objects.all()
    rate_list = rate_list[len(rate_list)-10:]
    rate_list = [{'Rate_USD': item.rate,
                  'Update_Rate_DataTime': item.update_rate_datatime,
                  'Request_DataTime': item.request_datatime} for item in rate_list]

    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()

    current_rate = data['Valute']['USD']['Value']
    update_datatime = data['Date']
    current_request_datetime = datetime.datetime.now()

    rate = {'Rate_USD': current_rate, 'Update_Rate_DataTime': update_datatime,
            'Request_DataTime': current_request_datetime, 'last_requests': rate_list}

    current_request = Rate(rate=current_rate,
                           update_rate_datatime=update_datatime,
                           request_datatime=current_request_datetime)
    current_request.save()
    return JsonResponse(rate)

