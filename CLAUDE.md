# ElectroCoach

**Runs platform** для экспериментов с AI-коучем для фаундеров и людей в точке перемен. Методология продукта: GROW (McKinsey/Google/ICF) + Логические уровни Дилтса. Governing methodology пайплайна — [Метод параноика](knowledge/methodology/метод-параноика.md).

Рабочее название «ElectroCoach» — нейминг не финализирован.

## Язык общения

**Все разговоры с пользователем — строго на русском языке.** Любые объяснения, комментарии, вопросы, сводки. Технические термины, идентификаторы в коде и имена файлов — в оригинале. Контент артефактов (лендинги, PRD, промпты) — на языке, в котором они написаны.

## Структура проекта

Полная архитектура и навигация — в [AGENTS.md](AGENTS.md) и [README.md](README.md).

Верхний уровень:
```
pipeline-templates/v1/     — шаблон пайплайна (9 стадий, read-only для ранов)
runs/                      — раны гипотез (run-1-*, run-2-*, run-3-* …)
knowledge/                 — methodology / patterns / learnings / decisions
archive/workshop/          — замороженные учебные материалы
archive/source-materials/  — исходники для экстракта в knowledge/
bot/                       — live MVP Run 1 (CI/CD контракт: путь bot/**)
```

Активный ран, куда писать новые артефакты, — `runs/<run>/` с `status: active` в `meta.yml`. На 2026-04-20 это `run-3-founder-coach`, стадия `0-team-constitution`.

## Дизайн-система лендингов (Run 1)

Паттерн описан в [`knowledge/patterns/dark-landing-system.md`](knowledge/patterns/dark-landing-system.md). Применяется к Run 1 B2C/B2B. Run 2 использует другую систему (светлая Torch). Новые лендинги — выбирать систему явно в PRD / кратком Дизайн-решении в ране.

## Обязательные MCP-серверы

- **Context7** (`context7`) — документация по библиотекам и API. При старте сессии агент **обязан** проверить доступность Context7 через `ToolSearch` с запросом `context7`. Если инструменты не загружены — **немедленно сообщить пользователю** и предложить перезапустить сессию.

## Правила деплоя

- **Код — только через git.** Все изменения доставляются на VPS через `git push` → GitHub Actions. Никогда не редактировать код на сервере по SSH.
- **SSH — только для не-git операций:** `.env`, gitignored конфиги, `docker compose restart`, логи.

## Запрет push в git

- **Агенту строго запрещено делать `git push`** ни в каком виде (включая `--force`, `-u`, push tags). Разрешены только локальные действия: `git add`, `git commit`, `git tag`, `git checkout -b`, `git mv`, `git rm`.
- **Решение о публикации на remote — только за пользователем.** Push в `main` триггерит CI/CD деплой бота, момент публикации контролирует пользователь сам.
- Если задача требует публикации — остановиться и явно спросить.

## Runs platform — правила

- Новые артефакты пишутся **только внутри active run** (`runs/<run>/stages/<N>/results/`).
- Шаблон `pipeline-templates/v1/` — **read-only**. Правки методологии → новая версия (`v2/`), не мутации v1.
- Стартовавший ран **не переходит в Stage 1**, пока не закрыт `stages/0-team-constitution/results/constitution.md` ([stage-0-gating](knowledge/decisions/stage-0-gating.md)).
- Frozen раны (`run-1-*`, `run-2-*`) — не редактировать, только читать для контекста.

## Telegram-бот (bot/)

Код живёт в `/bot/` в корне — live MVP Run 1. Остаётся в корне по CI-контракту ([bot-stays-at-root](knowledge/decisions/bot-stays-at-root.md)).

Методология разработки: [spec-kit](https://github.com/github/spec-kit/).

### Обязательный процесс для любых изменений в боте

**Любая** новая фича, изменение поведения или исправление бага в боте проходит через spec-kit агентов ([`bot/AGENTS.md`](bot/AGENTS.md)). Каждый этап **согласуется с пользователем** перед переходом к следующему:

1. **Specify** → задать все уточняющие вопросы → подтверждение → обновить `spec/spec.md` → ОК
2. **Plan** → техническое решение → ОК → обновить `spec/plan.md`
3. **Tasks** → декомпозиция → ОК → обновить `spec/tasks.md`
4. **Implement** → код по задачам → ОК
5. **Review** → проверка перед деплоем

Пользователь — владелец требований. На Specify агент спрашивает, а не додумывает. Нельзя писать код бота, минуя спецификацию. Исключение — критические хотфиксы (бот упал).

### Стек
- Python 3.11+, aiogram 3, asyncpg, httpx
- LLM: OpenRouter (пресет `@preset/electrocoach`)
- БД: PostgreSQL 16 (Docker)
- Деплой: Docker Compose на VPS (mentors@193.124.56.183), CI/CD через GitHub Actions

### Секреты (в `bot/.env`, не в git)
- `TELEGRAM_BOT_TOKEN`, `OPENROUTER_API_KEY`, `DATABASE_URL`

### Текущий статус
- Задеплоен на VPS в Docker (bot + PostgreSQL)
- CI/CD: push в `main` с изменениями в `bot/**` → GitHub Actions → SSH → `git pull` → `docker compose up --build`

### Принципы (из `bot/spec/constitution.md`)
- Async-first для всего I/O
- Коуч не советчик — только вопросы и отражение
- Один вопрос за раз в диалоге
- Атомарные сессии без памяти между ними
- 2 бесплатные сессии, потом заглушка подписки

### Запуск (локально)
```bash
cd bot && pip install -r requirements.txt && python -m src.main
```

### Запуск (продакшен)
```bash
cd ~/electrocoach/bot && docker compose up -d --build
```
