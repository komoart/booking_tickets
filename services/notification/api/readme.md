# API Notification. Точка входа для приема запросов на рассылку.

Структура модели данных событий:

| Field       | Type | Description                          |
|-------------|------|--------------------------------------|
| is_promo    | bool | Маркер типа события                  |
| template_id | str  | ID шаблона рассылки                  |
| user_ids    | str  | Список ID пользователей для рассылки |

Эндпоинт отправки уведомлений:
**/api/v1/send_notification**
```json
{
  "201": "Created mailing event"
}
```

Эндпоинт уведомлений при регистрации:
**/api/v1/user_registration**
```json
{
  "201": "Created welcome event"
}
```
