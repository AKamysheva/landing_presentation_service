# Landing Presentation Service

Бэкенд-сервис для лендинг-презентации разработчика с полноценной API-частью и интеграцией AI-инструментов.

## Функциональность

- API:
    - ```POST /api/contact``` — Принимает от пользователя форму обратной связи, анализирует тональность комментария с помощью AI и отправляет email-уведомления владельцу сайта и пользователю.
    - ```GET /api/health``` — проверка работоспособности сервиса.
    - ```GET /api/metrics``` — получение статистики обращений и результатов анализа тональности.

## 

## Stack
- Backend: Python, FastAPI, aiosmtplib
- Dependency manager: Poetry
- AI: openai

## Необходимые технологии
- Python 3.13
- Poetry
- Docker and Docker Compose (optional)

## Установка
1. Клонируем репозиторий:
   ```
   git clone https://github.com/AKamysheva/landing_presentation_service.git
   poetry install 
   ```
2. Создать .env файл в папке ```app```
   ```
    SMTP_HOST=smtp.gmail.com
    SMTP_PORT=587
    SMTP_USER=youremail@gmail.com
    SMTP_PASSWORD=yourpassword
    OWNER_EMAIL=owner@gmail.com

    RATE_LIMIT_SECONDS=120
    RATE_LIMIT_MAX_REQUESTS=1

    OPENROUTER_API_KEY=your_api_key
   ```
3. Запускаем проект с Docker Compose:
   ```
   docker compose up -d
   ```
   Либо локально:
   ```
   poetry run uvicorn app.main:app --host 0.0.0.0 --port 8900 --reload
   ```

### API
###### POST /api/contact - Отправка формы обратной связи.

Пример запроса:
```
{
  "name": "Anastasia",
  "phone": "+79991234567",
  "email": "anastasia@example.com",
  "comment": "Очень понравилось ваше портфолио"
}
```
Успешный ответ: 
```
{
  "message": "Request submitted successfully"
}
```
Возможные ошибки:
- 422 Validation Error - Некорректные данные.
- 429 Too Many Requests - Превышен лимит запросов.
- 500 Internal Server Error - Ошибка отправки email или внутренняя ошибка сервиса.

###### GET /api/metrics - Получение статистики обращений.
Ответ:
```
{
  "total_requests": 10,
  "positive": 6,
  "neutral": 3,
  "negative": 1,
  "unknown": 0
}
```

### Валидация данных

Для валидации используется Pydantic.

Ограничения:

имя: от 2 до 80 символов;
email: корректный email-адрес;
телефон: валидный номер телефона;
комментарий: минимум 5 символов.

### AI-интеграция

Для анализа комментариев используется OpenRouter API.

Задача AI: определить тональность сообщения; классифицировать комментарий как позитивный, нейтральный или негативный. Вернуть только одно слово.

Используемый промпт:
Определи тональность текста. 
Ответь одним словом: положительная, отрицательная или нейтральная. 
Текст: ```comment```

Fallback

Если AI-сервис недоступен, запрос продолжает обрабатываться; письмо отправляется; в статистику записывается значение unknown.

### Хранение данных
Все запросы и ошибки записываются в файл: ``logs.log``
Статистика обращений хранится в: ```app/metrics.json```

## API Documentation
👉 http://localhost:8900/docs