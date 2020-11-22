import time
import requests
from web_word_parse.celery import app
from .models import Task, Result
from django.conf import settings

@app.task
def parse(id, word):
    """
    Фоновая задача подсчета количества слов `word` в тексте www-страницы.
    Принимает `id` задачи и слово для поиска `word`.
    В случае успешного поключения к html-адресу, подсчитывает количество слов,
    отправляет результирующую запись в очередь NSQ и заполняет атрибуты задачи в Django. 
    Если подключение не удалось выставляет задаче статус `FAIL`.
    """
    task = Task.objects.get(id=id)

    if not task.address.startswith("http"):
        address = "http://" + task.address
    else:
        address = task.address

    words_count = 0
    http_status_code = 0
    task_status = 3
    try:
        response = requests.get(address,timeout=10)
        response.raise_for_status()
        words_count = response.text.lower().split().count(word.lower())
        http_status_code = response.status_code
    except Exception:
        task_status = 4

    # result = Result.objects.create(address=address, word=word, words_count=words_count, http_status_code=http_status_code)
    # result.save()

    requests.post("http://" + settings.NSQ_ADDR + "/pub", params={"topic":"bg_worker"}, json={"address":address, "word":word, "words_count":words_count, "http_status_code":http_status_code})

    task.task_status = task_status
    task.http_status_code = http_status_code
    task.save()

