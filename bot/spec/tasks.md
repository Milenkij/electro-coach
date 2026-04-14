# Tasks: ElectroCoach Bot MVP

## Этап 1: Инфраструктура
- [x] .gitignore
- [x] .env / .env.example
- [x] spec-kit документы (constitution, spec, plan, tasks)
- [ ] Структура папок + requirements.txt

## Этап 2: Core модули
- [ ] config.py — загрузка настроек
- [ ] db.py — asyncpg клиент + миграция SQL
- [ ] llm.py — OpenRouter клиент
- [ ] session.py — управление сессиями

## Этап 3: Бот
- [ ] bot.py — aiogram handlers
- [ ] main.py — точка входа

## Этап 3.1: Нетекстовые сообщения (Сценарий 4)
- [x] В `bot.py` handle_text: вместо молчаливого return на нетекстовые сообщения — ответить пользователю

## Этап 3.2: Учёт токенов и стоимости (Сценарий 5)
- [x] Миграция `migrations/002_add_token_usage.sql` — колонки `prompt_tokens`, `completion_tokens`, `cost` в `messages`
- [x] `llm.py` — `chat()` возвращает `LLMResponse` dataclass с content + usage, парсинг `usage` из ответа OpenRouter
- [x] `db.py` — `save_message()` принимает и записывает `prompt_tokens`, `completion_tokens`, `cost`
- [x] `session.py` — передаёт usage из `LLMResponse` в `save_message()`
- [x] `bot.py` — логирует текст user-сообщений в stdout
- [x] `main.py` — применяет все миграции из `migrations/` при старте (glob + sort)

## Этап 3.3: Стриминг ответа LLM (Сценарий 6)
- [x] `requirements.txt` — обновить aiogram 3.15.0 → 3.27.0
- [x] `llm.py` — метод `chat_stream()`: SSE streaming, async generator, yield accumulated text, парсинг usage из последнего чанка
- [x] `session.py` — метод `handle_message_stream()`: итерирует `chat_stream()`, yield'ит текст, сохраняет в БД с usage, fallback на `handle_message()`
- [x] `bot.py` — `handle_text()`: draft_id, итерация `handle_message_stream()`, throttle 300ms `sendMessageDraft()`, финальный `sendMessage()` с HTML, fallback

## Этап 3.4: Тайминг сессии (Сценарий 7)
- [ ] Миграция `003_time_budget_and_subscription.sql` — `time_budget TEXT` в `sessions`
- [ ] `db.py` — `set_time_budget()`, `get_session_meta()`
- [ ] `llm.py` — передача `session_started_at` и `time_budget` в system prompt
- [ ] `session.py` — загрузка meta и передача в LLM
- [x] `prompts/product-rules.md` — инструкции по управлению временем

## Этап 3.5: Paywall 72 часа (Сценарий 8)
- [ ] Миграция `003` — `subscription_until` в `users`, DROP `free_sessions_left`/`is_subscribed`
- [ ] `db.py` — `is_subscription_active()`, удалить `decrement_free_sessions()`
- [ ] `session.py` — проверка подписки в `start_session()`, убрать `decrement_free_sessions` из `_handle_rating()`
- [ ] `bot.py` — проверка подписки перед любым хэндлером, CTA на `@shapovalov_vsegda`

## Этап 3.6: Версионирование + тесты
- [ ] `bot/VERSION` — semver, начало с `0.3.0`
- [ ] `bot/tests/test_base.py` — 10 базовых тестов

## Этап 4: Тестирование
- [ ] Локальный запуск
- [ ] Прогон полного сценария сессии

## Этап 5: Деплой
- [ ] PostgreSQL на VPS
- [ ] Код на VPS
- [ ] Docker Compose
- [ ] Боевой тест
