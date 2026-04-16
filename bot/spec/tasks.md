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

## Этап 3.6: Мульти-участник + отключение paywall (Сценарии 9 + 10)

### 3.6.1 Миграция БД
- [x] `migrations/004_multi_participant_and_paywall_off.sql` — `participant_count INT DEFAULT 1` и `participants JSONB` в `sessions`, UPDATE всех users `subscription_until = '2030-01-01'`

### 3.6.2 db.py
- [x] `get_or_create_user()` — дефолт `subscription_until` → `'2030-01-01 00:00:00+00'` в INSERT
- [x] `set_session_participants(session_id, participants: list[str])` — UPDATE `participant_count` + `participants` (JSON)
- [x] `get_session_participants(session_id) -> list[str] | None` — SELECT + распарсить JSON
- [x] `get_session_meta()` — добавить `participants` в SELECT

### 3.6.3 session.py — FSM и онбординг
- [x] Новые состояния в `UserState`: `CHOOSING_MODE`, `COLLECTING_NAMES`, `CONFIRMING_NAMES`
- [x] `_user_participants: dict[int, list[str]]` — in-memory хранение имён
- [x] `start_session()` — создаёт DB-сессию, переводит в `CHOOSING_MODE`, возвращает «Сессия на одного или на нескольких?»
- [x] `_handle_choosing_mode(user_id, text)` — эвристика «один/несколько», роутинг в `ACTIVE` или `COLLECTING_NAMES`
- [x] `_handle_collecting_names(user_id, text)` — парсинг имён, сохранение в `_user_participants`, переход в `CONFIRMING_NAMES`
- [x] `_handle_confirming_names(user_id, text)` — подтверждение → запись в DB → `ACTIVE`; отклонение → `COLLECTING_NAMES`

### 3.6.4 session.py — роутинг сообщений
- [x] `handle_message()` — роутинг по `CHOOSING_MODE` / `COLLECTING_NAMES` / `CONFIRMING_NAMES` перед проверкой `ACTIVE`
- [x] `handle_message_stream()` — аналогичный роутинг (yield ответа без стриминга для онбординг-состояний)
- [x] Загрузка `participants` из DB meta и передача в `llm.chat()` / `llm.chat_stream()`

### 3.6.5 session.py — restore_state
- [x] `restore_state()` — если сессия active и `participants IS NOT NULL` → восстановить `_user_participants`

### 3.6.6 llm.py — групповой system prompt
- [x] `_build_system_prompt()` — новый параметр `participants: list[str] | None`, добавление блока `[Групповая сессия]` с полным групповым ритмом GROW
- [x] `chat()` — новый параметр `participants`, передача в `_build_system_prompt()`
- [x] `chat_stream()` — новый параметр `participants`, передача в `_build_system_prompt()`

### 3.6.7 Ручное тестирование
- [ ] Соло-сессия: проверить, что флоу «один/несколько → один → стандартная сессия» работает
- [ ] Групповая сессия: проверить онбординг (имена → подтверждение), ведение диалога по участникам, финальное резюме
- [ ] Paywall: проверить, что новые пользователи получают доступ до 2030
- [ ] Рестарт бота: проверить restore_state для соло и групповых сессий

## Этап 3.7: Версионирование + тесты
- [ ] `bot/VERSION` — semver, обновить до `0.4.0`
- [ ] `bot/tests/test_base.py` — обновить/добавить тесты для мульти-участника

## Этап 4: Тестирование
- [ ] Локальный запуск
- [ ] Прогон полного сценария сессии

## Этап 5: Деплой
- [ ] PostgreSQL на VPS
- [ ] Код на VPS
- [ ] Docker Compose
- [ ] Боевой тест
