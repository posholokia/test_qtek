## Тестовое задание

### Настройка переменных окружения

1. Создать json файл конфигурации БД:
```
  "type": тип используемой БД. Может быть postgres/memory. Для memory остальные не нужны
  "DB_SCHEME": схема подключения к БД.
  "DB_USER": пользователь БД
  "DB_PASS": пароль БД
  "DB_HOST": хост для подключения к БД
  "DB_NAME": название БД
  "DB_PORT": порт, на котором будет запущена БД
```
Если type будет указан неверно, будет использоваться InMemory репозиторий. 
В db_conf.example.json находится конфиг для запуска в докере. 

2. Создать .env в корне проекта со следующим содержимым:
```
DEBUG - режим запуска сервера, True/False
DB_CONF - название файла конфигурации с настройками БД (в данном случае Postgres)
```
(Можно скопировать из example.env)

3. Запуск в докере:

 - Через докер композ:
```
docker compose -f ./docker/storage.yml up --build -d
docker compose -f ./docker/app.yml up --build -d
```
 - С помощью make:

`make run`

4. Остановить приложение:
```
docker compose -f ./docker/storage.yml down
docker compose -f ./docker/app.yml down
```
или

`make down`
