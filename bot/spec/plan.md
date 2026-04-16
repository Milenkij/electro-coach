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

## Мульти-участник (Сценарий 9)

### Миграция

`migrations/004_multi_participant_and_paywall_off.sql`:

```sql
-- Multi-participant support
ALTER TABLE sessions
  ADD COLUMN IF NOT EXISTS participant_count INT NOT NULL DEFAULT 1,
  ADD COLUMN IF NOT EXISTS participants JSONB;

-- Disable paywall for all existing users
UPDATE users SET subscription_until = '2030-01-01 00:00:00+00';
```

### Изменения в модулях

#### `session.py` — основной объём работы

**Новые FSM-состояния:**
```python
class UserState(str, Enum):
    IDLE = "idle"
    CHOOSING_MODE = "choosing_mode"        # NEW
    COLLECTING_NAMES = "collecting_names"  # NEW
    CONFIRMING_NAMES = "confirming_names"  # NEW
    ACTIVE = "active"
    AWAITING_RATING = "awaiting_rating"
```

**Новое in-memory хранение:**
- `_user_participants: dict[int, list[str]]` — список имён участников (заполняется на этапе confirming_names, записывается в DB при переходе в ACTIVE)

**Изменения в `start_session()`:**
- Создаёт DB-сессию сразу (как сейчас)
- Переводит в `CHOOSING_MODE` вместо `ACTIVE`
- Возвращает текст «Сессия будет на одного человека или на нескольких?»

**Новые обработчики (приватные функции):**

1. `_handle_choosing_mode(user_id, text) -> str`:
   - Определяет «один» / «несколько» из свободного текста (простая эвристика: ищем «один/сам/solo/1» vs «несколько/двое/трое/группа/вместе/N»)
   - Если «один» → `participant_count=1`, `participants=NULL` в DB → `ACTIVE` → «С чем пришёл сегодня?»
   - Если «несколько» → `COLLECTING_NAMES` → «Перечисли имена участников»
   - Если непонятно → переспрашивает

2. `_handle_collecting_names(user_id, text) -> str`:
   - Парсит имена из свободного текста (split по запятым, переносам строк, «и»)
   - Сохраняет в `_user_participants[user_id]`
   - → `CONFIRMING_NAMES` → «Участники: {names}. Всё верно?»

3. `_handle_confirming_names(user_id, text) -> str`:
   - Если «да/верно/ок/правильно» → записывает `participant_count` и `participants` в DB → `ACTIVE` → «С чем вы пришли сегодня?»
   - Если «нет» или содержит новые имена → обратно в `COLLECTING_NAMES`, просит перечислить заново
   - Если непонятно → переспрашивает

**Изменения в `handle_message()` / `handle_message_stream()`:**
- Добавить роутинг по новым состояниям в начало (перед проверкой ACTIVE):
  ```python
  if state == UserState.CHOOSING_MODE:
      return await _handle_choosing_mode(user_id, text)
  if state == UserState.COLLECTING_NAMES:
      return await _handle_collecting_names(user_id, text)
  if state == UserState.CONFIRMING_NAMES:
      return await _handle_confirming_names(user_id, text)
  ```
- При отправке в LLM — загружать `participants` из DB и передавать в `llm.chat()` / `llm.chat_stream()`

**Изменения в `restore_state()`:**
- При восстановлении из DB: если сессия active и `participants IS NOT NULL` → восстановить `_user_participants`
- Состояния `CHOOSING_MODE` / `COLLECTING_NAMES` / `CONFIRMING_NAMES` не восстанавливаются из DB (если бот перезапустился в процессе онбординга — пользователь начинает заново через `/new`)

#### `db.py`

**Изменение существующих функций:**
- `get_or_create_user()`: INSERT дефолт `subscription_until` → `'2030-01-01 00:00:00+00'` (вместо `NOW() + INTERVAL '72 hours'`)
- `create_session()`: без изменений (participant_count и participants добавляются позже через update)

**Новые функции:**
- `set_session_participants(session_id, participants: list[str]) -> None` — UPDATE sessions SET participant_count = len(participants), participants = json(participants)
- `get_session_participants(session_id) -> list[str] | None` — SELECT participants FROM sessions, вернуть распаршенный JSON или None

**Изменение `get_session_meta()`:**
- Добавить `participants` в SELECT → возвращает `started_at`, `time_budget`, `participants`

#### `llm.py`

**Изменение `_build_system_prompt()`:**
- Новый параметр `participants: list[str] | None = None`
- Если `participants` не None — добавлять блок после core prompt, перед cards:

```
[Групповая сессия]
Участники: {список имён через запятую}

## Обращение
- К группе — на «вы»: «С чем вы пришли сегодня?»
- К конкретному участнику — на «ты»: «Аня, как ты видишь эту ситуацию?»

## Главный принцип
Один вопрос — одному участнику — один ответ. Не задавай следующий вопрос, пока не получишь ответ на текущий. Не задавай вопрос группе целиком, если можно спросить конкретного человека.

## Задача сессии
Привести всех участников к ответам на один общий запрос. Если участники приходят с разными темами — твоя задача найти общий знаменатель или помочь группе выбрать одну тему для этой сессии.

## Групповой ритм GROW

### 0. Контракт
1. Спроси группу: «С чем вы пришли сегодня?»
2. Выслушай ответ (один человек пишет за всех — это нормально)
3. Если запрос один — уточни его у каждого участника по очереди: «{Имя}, что для тебя будет результатом 10 из 10?»
4. Если запросы разные — помоги группе выбрать один общий
5. После прояснения запроса — спроси каждого участника о времени: «{Имя}, сколько у тебя есть времени?»
6. Если ответы о времени расходятся — приведи к единому: «Аня говорит 30 минут, Макс — час. Давайте определимся вместе.»

### На каждом этапе GROW (G → R → O → W)

Выполняй **раунд опроса**:

1. **Опроси каждого.** Задай вопрос первому участнику по имени → дождись ответа → задай тот же (или адаптированный) вопрос следующему → и так по кругу.

2. **Определи уровень Дилтса каждого ответа** (окружение → поведение → способности → убеждения → идентичность → миссия). Целевой уровень определяется текущей фазой GROW:
   - G (Goal): убеждения / идентичность / миссия
   - R (Reality): окружение / поведение / способности
   - O (Options): способности / поведение / убеждения
   - W (Will): поведение / окружение

3. **Выровняй уровни.** Если ответы участников на разных уровнях Дилтса:
   - Задай уточняющий вопрос каждому, кто не на целевом уровне: «{Имя}, ты говоришь о {текущий уровень}. А если посмотреть на уровне {целевой уровень} — что ты видишь?»
   - Сделай до 2–3 попыток выравнивания
   - Если прогресса нет — зафиксируй текущее состояние каждого и двигайся дальше: «Фиксирую: Аня видит это на уровне убеждений, Макс — на уровне поведения. Идём дальше.»

4. **Разреши конфликты.** Если ответы противоречат друг другу:
   - Отрази противоречие группе: «Аня говорит X, а Макс — Y. Это интересное расхождение.»
   - Задай каждому уточняющий вопрос, чтобы прояснить позицию
   - Старайся привести к общему пониманию — это ключевая ценность групповой сессии
   - Если после 2–3 попыток приведение не происходит — зафиксируй обе позиции и двигайся дальше

5. **Только после выравнивания** переходи к следующему этапу GROW.

## Проверка авторства
Если ты задал вопрос Ане, а из ответа явно следует, что отвечает не Аня (другой контекст, другое имя, смена перспективы) — уточни: «Это ответ Ани или кого-то другого?»

## Пропуск участника
Если пользователь говорит, что у участника нет ответа — прими это спокойно и переходи к следующему. Пропущенный участник остаётся в сессии и участвует в следующих вопросах.

## Финальное резюме

Когда сессия завершается, сформируй два блока:

**Общее резюме:**
- Общий запрос группы
- Ключевые выводы и найденные инсайты
- Общий первый шаг (если применимо)
- Динамика группы: где было единство, где расхождение

**Индивидуальное резюме (по каждому участнику):**
- {Имя}: ключевые инсайты, текущий уровень по Дилтсу, персональный первый шаг, на что обратить внимание
```

**Изменение `chat()` и `chat_stream()`:**
- Новый параметр `participants: list[str] | None = None`
- Передают в `_build_system_prompt()`

#### `bot.py`

- Минимальные изменения. Весь роутинг новых состояний внутри `session.py`
- `handle_text()` уже вызывает `session.handle_message_stream()` → всё работает

#### Промпты

- Новый файл `prompts/playbook/group-session-playbook.md` НЕ создаём — инструкции для группы передаются динамически через `[Групповая сессия]` блок в system prompt. Причина: это условный слой (только для групповых сессий), а не always-loaded.

### Что НЕ меняется

- `config.py`, `main.py`, `formatting.py`
- Стриминг работает как раньше
- Paywall-механизм сохраняется (дата сдвинута на 2030)
- Retrieval cards, prompt stack, USAGE.md

## Отключение paywall (Сценарий 10)

### Миграция

В том же файле `004_multi_participant_and_paywall_off.sql` (см. выше).

### Изменения в `db.py`

- `get_or_create_user()`: дефолт subscription_until → `'2030-01-01 00:00:00+00'`
- Всё остальное без изменений — `is_subscription_active()`, `_check_subscription()` в bot.py, `PAYWALL_MESSAGE` — остаются на месте

## Версионирование

Файл `bot/VERSION` — semver (major.minor.patch). Начальная версия: `0.3.0`.

## Тесты

`bot/tests/test_base.py` — 10 базовых тестов (pytest + unittest.mock), запускаются после каждого инкремента.

## Деплой

Docker Compose на VPS с автозапуском. PostgreSQL в отдельном контейнере. CI/CD через GitHub Actions.
