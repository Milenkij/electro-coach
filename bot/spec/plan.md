# Technical Plan: ElectroCoach Bot

## Стек

- Python 3.11+ / aiogram 3 / asyncpg / httpx
- PostgreSQL на VPS
- OpenRouter API (модель: anthropic/claude-sonnet-4-20250514)
- Деплой: systemd на VPS

## Архитектура

```
main.py → Bot (aiogram) → SessionManager → LLM (OpenRouter)
                                         → DB (asyncpg/PostgreSQL)
```

Polling mode (не webhook) — проще для MVP, не нужен домен/SSL.

## Модули

- `config.py` — загрузка .env, dataclass настроек
- `db.py` — asyncpg pool, CRUD для users/sessions/messages
- `llm.py` — OpenRouter chat completions, загрузка системного промпта
- `session.py` — FSM сессии (idle → active → awaiting_rating → idle)
- `bot.py` — aiogram handlers для команд и текстовых сообщений
- `main.py` — инициализация и запуск

## База данных

3 таблицы: users, sessions, messages. Миграция в `migrations/001_init.sql`.

## Контекст LLM

Каждое сообщение пользователя → загрузка всей истории сессии из БД → отправка в LLM с системным промптом. Контекст ограничен одной сессией.

## Деплой

systemd service с автозапуском. PostgreSQL на том же VPS.
