## Weather API
## Стек:
* Python 3.10
* Django 4
* DRF
* Postgres
## Функционал:
* Получение текущей погоды
  * по названию населенного пункта `/name?city=Москва`
  * по географическим координатам `/coord?lat=50&lon=40`
  * дополнительные параметры
    * формат единиц измерения температуры 
      * `?units=standard` или пустой - в Кельвинах
      * `?units=imperial` - в Фаренгейтах
      * `?units=metric` - в Цельсиях
    * язык `?lang=en`

## Запуск
#### 1) Установить Docker на компьютер
#### 2) Клонировать этот репозиторий
#### 3) В корне создать файл .env.dev
    DEBUG=1
    SECRET_KEY=156eca1c3da67b3951edc0bf0728fd52
    DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    
    #db
    POSTGRES_ENGINE=django.db.backends.postgresql
    POSTGRES_DB=weather_api
    POSTGRES_USER=weather_api_user
    POSTGRES_PASSWORD=weather_api_pass
    POSTGRES_HOST=weather_api_db
    POSTGRES_PORT=5432
    DATABASE=postgres

    #api
    OPENWEATHER_API_KEY=<your key>
    DEFAULT_UNITS=metric
    DEFAULT_LANG=ru
   
#### 4) Собрать и запустить контейнер
    docker-compose up --build

