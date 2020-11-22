from django.db import models

class Result(models.Model):
    address = models.CharField("Адрес", max_length=300, null=True)
    word = models.CharField("Адрес", max_length=12, null=True)
    words_count = models.SmallIntegerField("Количество слов", default=0)
    http_status_code = models.SmallIntegerField("Код статуса", default=0)

    def __str__(self):
        return "{} {}".format(self.address, self.http_status_code)

    class Meta:
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"


class Task(models.Model):
    STATUS = [
        (1,"NOT_STARTED"),
        (2,"PENDING"),
        (3,"FINISHED"),
        (4,"FAIL")
    ]
    address = models.CharField("Адрес", max_length=300, null=False, default="")
    word = models.CharField("Слово", max_length=12, null=False, default="Python")
    http_status_code = models.SmallIntegerField("HTML статус", default=0)
    timestamp = models.DateTimeField("Время создания", auto_now_add=True)
    task_status = models.SmallIntegerField("Статус задачи", choices=STATUS, default=1)

    def __str__(self):
        return "{} {}".format(self.address, self.task_status)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"