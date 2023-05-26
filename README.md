# Дипломный проект "Бронирование билетов"

## Проектное задание

Здорово будет связать фильмы с походами в кино. Не всем нравится сидеть дома и
смотреть фильмы в одиночку. Иногда хочется их посмотреть с компанией единомышленников.

Для реализации такой возможности от вас требуется реализовать для определенной 
группы фильмов кнопку покупки билета в кино. Система должна позволять пользователям
создавать свои расписания, фильмы и место сбора, а также возможное количество людей
давать возможность любому пользователю выбирать пользователя-хоста 
(тот, который предлагает фильм и место) и затем дату + время фильма. 
Для данной задачи реализовывать оплату не нужно, достаточно бронировать 
билеты и не давать забронировать больше билетов, чем есть мест у конкретного человека. 


Так как эти посиделки камерные, то заданием со звездочкой будет придумать систему 
оценки пользователя-хоста и пользователя-гостя (тот, который пришел на совместный просмотр).

## Используемые технологии

Nginx - проксирование внешних запросов
Fastapi - асинхронный фреймворк для создания API
PostgreSQL - база данных для хранения данных о событиях и бронировании
Redis - база данных для хранения кэша
Docker - развертывание проекта


## Основные сервисы проекта

- Auth API - регистрация пользователя, информация о пользователе
- UGC API - информация о друзьях пользователя
- Movie API - информация о фильмах
- Booking API - бронирование билетов
- Url generation - генерация коротких ссылок
- Notification - отправка уведомлений
- Graylog - логирование событий микросервисов


## Общая схема проекта

![](docs/main.png)

# Запуск проекта

1. Скопировать/заполнить файл настроек окружения
```shell
cp example.env .env
```

2. Создать внешнюю сеть "project-network" командой:
```shell
docker network create 'project-network'
```

3. Запустить контейнер ELK для организации логирования
```
cd ELK
docker-compose up
```

Доступ в интерфейс elastic. Выбрать нужные метрики и сервисы.
```
http://localhost:5601/app/home#/
```

4. Запустить контейнер основного сервиса
```
cd ../
docker-compose up
```

5. Получить идентификаторы и токены доступов
```shell
python jwt_token.py
```

```json
{
  "user": "f55291b9-c09d-405b-b025-36f26c887905", 
  "user_access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmNTUyOTFiOS1jMDlkLTQwNWItYjAyNS0zNmYyNmM4ODc5MDUiLCJwZXJtaXNzaW9ucyI6WzAsM10sImlzX3N1cGVyIjpmYWxzZX0.2WPPv2WQnidid3uDKROtmUSHLGwXtrw-LvipKNCjOFQ",
  
  "sudo": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a",
  "sudo_access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhNWE4ZjU3My0zY2VlLTRjY2MtOGEyYi05MWNiOWY1NTI1MGEiLCJwZXJtaXNzaW9ucyI6WzAsM10sImlzX3N1cGVyIjp0cnVlfQ.t2XpMQQhN7lJ1eXQWaSGgjiSt1qlhaPTT-HYaRa2umc",
  
  "author": "50760ee6-2073-445d-ad25-f665937f3b33",
  "author_access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1MDc2MGVlNi0yMDczLTQ0NWQtYWQyNS1mNjY1OTM3ZjNiMzMiLCJwZXJtaXNzaW9ucyI6WzAsM10sImlzX3N1cGVyIjpmYWxzZX0.Osgl1ubOKLHiAI-FrfA8HdZnEA7DlXmYBpj-UTwgp6w",
  
  "guest_1": "39e60237-83ea-4c65-9bc9-f6b47d109738",
  "guest_1_access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzOWU2MDIzNy04M2VhLTRjNjUtOWJjOS1mNmI0N2QxMDk3MzgiLCJwZXJtaXNzaW9ucyI6WzAsM10sImlzX3N1cGVyIjpmYWxzZX0.sjEPqtfXJnj6nYxPLCs_dO2j1jEvl8dkzfhojCp-uz0",
  
  "guest_2": "d0c5635c-3211-4cf8-94ab-cbe6800771c4",
  "guest_2_access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkMGM1NjM1Yy0zMjExLTRjZjgtOTRhYi1jYmU2ODAwNzcxYzQiLCJwZXJtaXNzaW9ucyI6WzAsM10sImlzX3N1cGVyIjpmYWxzZX0.5Ae__t-XpIUZswIZtoHMDsxhyr91V9uwb7ZkTG9lWP8",
}
```

## BOOKING API

Сервис бронирования билетов.

Ссылка на openapi:
```
http://localhost:8080/api/openapi#/
```

![](docs/booking_openapi_v.2.png)

### Организатор

- Автор создает объявление о событии, "Собираюсь посмотреть фильм завтра вечером, ищу компанию".
- Другие пользователи могут подать заявку на участие в событии. Создают запись.
- Автор может вносить изменения в объявление.
- При внесении изменений в объявление - всем участникам и потенциальным гостям приходит уведомление и ссылка на анонс.
- За 24 часа до события - всем участникам приходит уведомление и ссылка на анонс.
- За 1 час до события - всем участникам приходит уведомление и ссылка на анонс.

  - автору приходят заявки на участие в событии от гостей бронирования.
  - автору приходит уведомление и ссылка на подробную информацию о состоянии бронирования.
  - автор может принять или отклонить заявку на участие в событии.
  - если состояние бронирования изменяется - автору и гостю приходит уведомление и ссылка на подробную информацию о состоянии бронирования.
  - когда заявка одобрена - сведения о госте появляются в информации о событии.

### 2. Сценарий гость

- Пользователь может посмотреть подробную информацию о событии анонса.
- Для поиска подходящего события, пользователь использует фильтры и получает список объявлений.
- Пользователь отправляет заявку на участие в событии. Создается запись бронирования.
- Автору приходит уведомление и ссылка на подробную информацию о состоянии бронирования.
- Если информация о событии изменилась - пользователю приходит уведомление и ссылка на анонс.
- Когда статус заявки меняется - пользователю приходит уведомление и ссылка на бронирование.

### Анонсы

- Нельзя создавать дубликаты объявлений от одного пользователя
- Проверять права пользователя перед изменением записи

<hr style="border:2px solid gray">
Создание объявления

Request URL
```shell
http://localhost:8080/app/v1/announcement/23536729-1e1f-4639-a9cf-0883634143ab
```

Server response
```json
{
  "id": "3b694076-c2a2-4aac-b7e1-b496a3f9724b",
  "created": "2023-05-26T12:45:22.889921+00:00",
  "modified": "2023-05-26T12:45:22.889933+00:00",
  "status": "Created",
  "title": "Fake Title",
  "description": "Fake description",
  "movie_title": "Fake movie",
  "author_name": "Max Reed",
  "sub_only": false,
  "is_free": true,
  "tickets_count": 2,
  "tickets_left": 2,
  "event_time": "2023-05-26T12:45:22.842896+00:00",
  "event_location": "Fake location",
  "guest_list": [],
  "author_rating": 4.9,
  "duration": 0
}
```

Получение всей информации по объявлению

Request URL
```shell
http://localhost:8080/app/v1/announcement/2a580a71-4ba6-4626-b88e-381d3cf6e1da
```

Server response
```json
{
  "id": "2a580a71-4ba6-4626-b88e-381d3cf6e1da",
  "created": "2023-05-26T11:19:13.822707+00:00",
  "modified": "2023-05-26T11:19:13.822714+00:00",
  "status": "Created",
  "title": "Fake Title",
  "description": "Fake description",
  "movie_title": "Fake movie",
  "author_name": "Max Reed",
  "sub_only": false,
  "is_free": true,
  "tickets_count": 2,
  "tickets_left": 2,
  "event_time": "2023-05-26T11:19:13.732697+00:00",
  "event_location": "Fake location",
  "guest_list": [],
  "author_rating": 4.9,
  "duration": 0
}
```

Получение списка всех объявлений

Request URL
```shell
http://localhost:8080/app/v1/announcements
```

Server response
```json
[
  {
    "id": "2a580a71-4ba6-4626-b88e-381d3cf6e1da",
    "title": "Fake Title",
    "author_id": "f55291b9-c09d-405b-b025-36f26c887905",
    "sub_only": false,
    "is_free": true,
    "tickets_count": 2,
    "event_time": "2023-05-26T11:19:13.732697+00:00",
    "event_location": "Fake location",
    "duration": 0
  },
  {
    "id": "52b1c581-5ab9-48c1-9df6-52f29bc71872",
    "title": "Fake Title",
    "author_id": "f55291b9-c09d-405b-b025-36f26c887905",
    "sub_only": false,
    "is_free": true,
    "tickets_count": 2,
    "event_time": "2023-05-26T11:20:39.945723+00:00",
    "event_location": "Fake location",
    "duration": 0
  },
  {
    "id": "3b694076-c2a2-4aac-b7e1-b496a3f9724b",
    "title": "Fake Title",
    "author_id": "f55291b9-c09d-405b-b025-36f26c887905",
    "sub_only": false,
    "is_free": true,
    "tickets_count": 2,
    "event_time": "2023-05-26T12:45:22.842896+00:00",
    "event_location": "Fake location",
    "duration": 0
  }
]
```

<hr style="border:2px solid gray">

### Бронирование

- Нельзя быть гостем на своем событии
- Нельзя регистрироваться на события с одним временем начала
- Проверять права пользователя перед изменением записи
- Показывать пользователю только его записи


Создание бронирования

Request URL
```shell
http://localhost:8080/app/v1/booking/52b1c581-5ab9-48c1-9df6-52f29bc71872
```

Server response
```json
{
  "id": "862cc5f8-d445-48b0-bcec-2219a97093c8",
  "announcement_id": "52b1c581-5ab9-48c1-9df6-52f29bc71872",
  "movie_title": "Fake movie",
  "author_name": "Michael Simpson",
  "guest_name": "Greg Porter",
  "author_status": null,
  "guest_status": true,
  "guest_rating": 0,
  "author_rating": 0.2,
  "event_time": "2023-05-26T11:20:39.945723+00:00"
}
```

Получение всей информации по заявке

Request URL
```shell
http://localhost:8080/app/v1/booking/862cc5f8-d445-48b0-bcec-2219a97093c8
```

Server response
```json
{
  "id": "862cc5f8-d445-48b0-bcec-2219a97093c8",
  "announcement_id": "52b1c581-5ab9-48c1-9df6-52f29bc71872",
  "movie_title": "Fake movie",
  "author_name": "Michael Simpson",
  "guest_name": "Greg Porter",
  "author_status": null,
  "guest_status": true,
  "guest_rating": 0,
  "author_rating": 0.2,
  "event_time": "2023-05-26T11:20:39.945723+00:00"
}
```

Получение списка заявок

Request URL
```shell
http://localhost:8080/app/v1/bookings?filter%5Bself%5D=guest
```

Server response
```json
[
  {
    "id": "862cc5f8-d445-48b0-bcec-2219a97093c8",
    "author_name": "Michael Simpson",
    "guest_name": "Greg Porter",
    "author_status": null,
    "guest_status": true
  }
]
```

## AUTH API

Сервис-заглушка для имитации регистрации пользователей, получения данных о 
пользователе, получения группы пользователя.

Ссылка на openapi:
```
http://localhost:8080/auth/api/openapi#/
```

![](docs/auth_openapi.png)

Регистрация пользователя
```
POST

/auth/v1/register/
```

Получение данных пользователя
```
POST

/auth/v1/user_info/{uuid}
```

Получение группы пользователя
```
POST

/auth/v1/user_group/{group}
```


## UGC API

Сервис-заглушка для имитации обзоров на фильмы, подписок на фильмы, оценки 
рейтинга фильма.

Ссылка на openapi:
```
http://localhost:8080/ugc/api/openapi#/
```

![](docs/ugc_openapi.png)

Информация об обзоре
```
POST

/ugc/v1/review_info/{movie_id}/{user_id}/{review_id}
```

Информация о подписке
```
POST

/ugc/v1/subscribers/{movie_id}
```

Информация о рейтинге
```
POST

/ugc/v1/likes_count/{review_id}
```


## MOVIES API

Сервис-заглушка для получения данных о фильме.

Ссылка на openapi:
```
http://localhost:8080/movie/api/openapi#/
```

![](docs/movie_openapi.png)

Информация о фильме
```
POST

/movie_api/v1/movie/{uuid}
```

## Graylog

ссылка на схему
