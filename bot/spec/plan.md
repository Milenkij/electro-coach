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
- `bot.py` — aiogram handlers для команд, текстовых и нетекстовых сообщений
- `main.py` — инициализация и запуск

## База данных

3 таблицы: users, sessions, messages. Миграция в `migrations/001_init.sql`.

## Учёт токенов и стоимости (Сценарий 5)

### Миграция
`migrations/002_add_token_usage.sql` — добавить в `messages`:
- `prompt_tokens INT` — токены промпта (NULL для user-сообщений)
- `completion_tokens INT` — токены ответа (NULL для user-сообщений)
- `cost NUMERIC(12,6)` — стоимость в USD (NULL для user-сообщений)

### Изменения в модулях
- **`llm.py`** — `chat()` возвращает dataclass `LLMResponse(content, prompt_tokens, completion_tokens, cost)` вместо строки. Парсит `usage` из ответа OpenRouter.
- **`db.py`** — `save_message()` принимает опциональные `prompt_tokens`, `completion_tokens`, `cost`. Записывает в новые колонки.
- **`session.py`** — при сохранении assistant-сообщения передаёт токены/стоимость из `LLMResponse`.
- **`bot.py`** — логирует полный текст user-сообщений в stdout (`logger.info`).

### Агрегация
Токены/стоимость по сессии и пользователю — SQL `SUM` по `messages`. Новых колонок/таблиц для агрегатов не создаём.

## Контекст LLM

Каждое сообщение пользователя → загрузка всей истории сессии из БД → отправка в LLM с системным промптом. Контекст ограничен одной сессией.

## Деплой

systemd service с автозапуском. PostgreSQL на том же VPS.
