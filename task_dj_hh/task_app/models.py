from django.db import models


class Rate(models.Model):
    """
    Модель данных запроса get-current-usd. Содержит следующие поля:
        rate - числовое (с плавающей запятой) поле для хранения курса доллара к рублю.
        update_rate_datatime - текстовое поле для хранения времени последнего обновления курса.
        request_datatime - текстовое поле для хранения времени выполнения запроса.
    """
    rate = models.FloatField(max_length=7)
    update_rate_datatime = models.CharField(max_length=30)
    request_datatime = models.CharField(max_length=30)