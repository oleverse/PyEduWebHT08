- для підключення до MongoDB і Redis використовується файл **db.ini**
- робота скрипту протестована з Python 3.11.3

Послідовність для запуску:
- клонуємо проєкт з репозиторію:
> $ git clone --branch part-1 git@github.com:oleverse/PyEduWebHT08.git
- встановлюємо залежності:
> cd PyEduWebHT08

> poetry shell

> poetry update

- створюємо порожню MongoDB базу даних
- можна запустити контейнер для Redis:
> docker run --name redis-cache -d -p 6379:6379 redis

- задаємо MongoDB.url і параметри підключення до Redis у файлі db.ini
- запускаємо основний скрипт:
> python main.py

- скрипт заповнить базу даних даними із JSON-файлів, що лежать у каталозі **data**
- далі можна користуватися запитами:
> name:st

> tag: world

> tags:ive,rld
- пробіли біля розділових знаків запитів ігноруються
