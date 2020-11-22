E8.9 Практическое задание

В данном приложении мы собираем статистику по количеству упоминаний слова Python на различных вебсайтах. 

Это приложение использует Django в качестве фреймворка, celery для обработки фоновых задач, очередь NSQ для передачи результата выполенения фоновых задач и PostgreSQL для хранения данных. 

Чтобы запустить приложение на локальной машине нужно: 

- склонировать этот репозиторий;
- перейти в папку репозиторием;
- при первом запуске приложения необходимо собрать и запустить контейнер с postgres перед тем как запустить django для штатной отработки migrate `docker-compose up -d data_db`(можно и не выполнять этот пункт, просто после первого запуска `docker-compose up -d` нужно будет остановить контейнеры `docker-compose down` и запустить снова для отработки migrate);
- далее, после первой отработки migrate, приложение запускается как обычно `docker-compose up -d`

После успешного старта контейнеров, на `127.0.0.1:9000` запускается приложение с эндпоинтами: 

- / -- форма для добавления адреса сайта в очередь фоновых задач и ввода искомого слова Python;
- /result -- таблица с результатами подсчетов;
- /count -- служебный эндпоинт GET для запроса количества записей в модели Result со страницы результатов, из скрипта JS (автоматическая перезагрузка страницы при изменении результата запроса);
- /add_result -- служебный эндпоинт для приема POST от comsumer, результата выполения фоновой задачи, из очереди NSQ.

Для просмотра работы очереди NSQ запускается nsqadmin доступный по адресу - `http://127.0.0.1:4171`

Модели sqlalchemy были переделаны для Django.

Цепочка обработки задачи:

Пользователь(адрес, слово) -> web(task.html) -> django model Task -> celery(tasks.py) -> NSQ(bg_worker) -> consumer(bg_worker:consumer_channel) -> django model Result(API add_result) -> web(result.html) -> Пользователь