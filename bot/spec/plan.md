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

## Стриминг ответа LLM (Сценарий 6)

### Зависимости
- `aiogram` 3.15.0 → 3.27.0 (поддержка `sendMessageDraft`)

### Изменения в модулях
- **`llm.py`** — новый метод `chat_stream()`: запрос с `"stream": true`, async generator yield'ит accumulated text на каждый чанк. Последний чанк содержит `usage` — возвращается как `LLMResponse`. Существующий `chat()` остаётся как fallback.
- **`session.py`** — новый метод `handle_message_stream()`: вызывает `llm.chat_stream()`, yield'ит accumulated text, после завершения сохраняет в БД с usage. При ошибке — fallback на `handle_message()`.
- **`bot.py`** — `handle_text()`: генерирует `draft_id`, итерирует `handle_message_stream()`, throttle ~300ms между `sendMessageDraft()`. Финал: `sendMessage()` с HTML. При ошибке — fallback на обычный `message.answer()`.

### Не меняются
`config.py`, `db.py`, миграции, `main.py`.

## Контекст LLM

Каждое сообщение пользователя → загрузка всей истории сессии из БД → отправка в LLM с системным промптом. Контекст ограничен одной сессией.

## Тайминг сессии (Сценарий 7)

### Миграция
`migrations/003_time_budget_and_subscription.sql` — добавить в `sessions`:
- `time_budget TEXT` — сырой ответ пользователя о времени (nullable)

### Изменения в модулях
- **`db.py`** — `set_time_budget(session_id, text)` записывает time_budget. `get_session_meta(session_id)` возвращает `started_at` + `time_budget`.
- **`llm.py`** — `chat()` и `chat_stream()` принимают `session_started_at: datetime | None`, `time_budget: str | None`. Если переданы — добавляют блок `[Метаданные сессии]` в system prompt.
- **`session.py`** — `handle_message()` / `handle_message_stream()` загружают meta из сессии и передают в LLM.
- **`prompts/product-rules.md`** — инструкции: спросить о времени после прояснения запроса, калибровать глубину, мягко подсвечивать выход за рамки.

## Paywall (Сценарий 8)

### Миграция (в том же файле 003)
- `users`: `ADD COLUMN subscription_until TIMESTAMPTZ NOT NULL DEFAULT NOW() + INTERVAL '72 hours'`
- `users`: `DROP COLUMN free_sessions_left`, `DROP COLUMN is_subscribed`

### Изменения в модулях
- **`db.py`** — `is_subscription_active(user_id) -> bool`. Удалить `decrement_free_sessions()`.
- **`session.py`** — `start_session()` проверяет подписку через `is_subscription_active()`. Убрать `decrement_free_sessions()` из `_handle_rating()`.
- **`bot.py`** — перед обработкой любого сообщения проверяет подписку. Если истекла — CTA на `@shapovalov_vsegda`. Исключение: `/start` регистрирует нового пользователя.

## Версионирование

Файл `bot/VERSION` — semver (major.minor.patch). Начальная версия: `0.3.0`.

## Тесты

`bot/tests/test_base.py` — 10 базовых тестов (pytest + unittest.mock), запускаются после каждого инкремента.

## Деплой

Docker Compose на VPS с автозапуском. PostgreSQL в отдельном контейнере. CI/CD через GitHub Actions.
