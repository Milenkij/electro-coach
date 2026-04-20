# ElectroCoach — Agent Guide

## Что это за репо

**Платформа для запуска экспериментов (runs)** над гипотезой AI-коуча для фаундеров и людей в точке перемен. Не один продукт, а набор версионированных ранов на общем шаблоне пайплайна.

**Governing methodology:** [Метод параноика](knowledge/methodology/метод-параноика.md) — производство цифровых продуктов в условиях неопределённости. Воронка неопределённости, продюсерская модель, 5 принципов. Каждая стадия пайплайна — шаг воронки, каждый ран проходит одну и ту же последовательность.

## Архитектура

```
pipeline-templates/v1/     — шаблон пайплайна (9 стадий, read-only для ранов)
runs/
  run-1-electrocoach-v1/   — frozen (B2C + B2B-as-EAP → MVP-бот в /bot)
  run-2-second-look/       — frozen (B2B-консалтинг, пивот от run-1)
  run-3-founder-coach/     — active, current_stage: 0-team-constitution
knowledge/                 — библиотека знаний (methodology / patterns / learnings / decisions)
archive/
  workshop/                — frozen учебные материалы
  source-materials/        — исходники для экстракта в knowledge/
bot/                       — live-артефакт Run 1 (CI/CD на путь bot/**)
```

Детали — в [README.md](README.md).

## Как найти текущую работу за 60 секунд

1. `runs/*/meta.yml` → ищи `status: active`
2. В этом ране: `meta.yml → current_stage`
3. Работать в `runs/<active-run>/stages/<current_stage>/results/`
4. Контекст — в [`runs/<active-run>/MOC.md`](runs/)

На сегодня **active run — `run-3-founder-coach`**, на стадии `0-team-constitution` (in-progress).

## Где писать артефакты

**Только внутри active run.** Путь: `runs/<active-run>/stages/<N>/results/<artifact>`.

Не пишите артефакты в:
- `pipeline-templates/v1/` — шаблон read-only, мутации запрещены
- Корень репо — ран-артефакты живут в своём ране
- Frozen раны (`run-1-*`, `run-2-*`) — они зафиксированы

Исключение — `/bot/` (live Telegram-бот Run 1, см. ниже).

## Как работать с pipeline-template

- Каждая версия (`v1/`, потенциально `v2/` в будущем) — **read-only per run**. Ран копирует шаблон при старте (решение [copy-at-start](knowledge/decisions/copy-at-start.md)).
- Раны остаются на **своей** версии навсегда ([pipeline-frozen-per-run](knowledge/decisions/pipeline-frozen-per-run.md)). Нельзя «подтянуть актуальный шаблон» в уже стартовавший ран.
- Delta в методологии → создать `pipeline-templates/v2/` (см. триггеры в карточке решения).

## Как стартовать новый ран

```bash
# 1. Скопировать шаблон
cp -r pipeline-templates/v1 runs/run-N-<name>
rm runs/run-N-<name>/{meta.template.yml,MOC.template.md}

# 2. Написать meta.yml (под конкретный ран) и MOC.md (скелет)

# 3. Пройти Stage 0 — Team Constitution
#    Результат: stages/0-team-constitution/results/constitution.md
#    БЕЗ ЭТОГО АРТЕФАКТА РАН НЕ ПЕРЕХОДИТ В STAGE 1

# 4. Только после подписанной конституции — открыть Stage 1 (Discovery)
```

## Stage 0 gating

**Новый ран не стартует в Discovery, пока Stage 0 не закрыт подписанной `constitution.md`.** Это реализация принципа «гибкие проектные команды» Метода параноика. Причины — в [stage-0-gating.md](knowledge/decisions/stage-0-gating.md).

Форматы Stage 0 по размеру команды:
- Соло — self-diagnostic (один проходит все 7 промптов на себе)
- Dyad — cross-diagnostic (каждый ведёт второго)
- Команда — полный формат

Исторические раны (Run 1, Run 2) прошли до введения Stage 0 — в них `stages/0-team-constitution/results/STUB.md` с пометкой «historical gap», не ретро-заполняются.

## Как использовать `/knowledge/`

- **MOC-first:** каждый ран имеет `MOC.md` с разделами по стадиям и ссылками на карточки. Начинать ориентирование с MOC, не с рандомного grep
- 4 подпапки:
  - [`methodology/`](knowledge/methodology/) — методологические рамки (GROW, Дилтс, AJTBD, Метод параноика, диагностики, Naming playbook)
  - [`patterns/`](knowledge/patterns/) — техн. / продуктовые паттерны (Dark landing system, Quiz hub, AJTBD graph)
  - [`learnings/`](knowledge/learnings/) — уроки из ранов
  - [`decisions/`](knowledge/decisions/) — архитектурные решения
- Новая карточка — только если знание переиспользуемо (применимо за пределами одного рана). Для узкого контекста — артефакт рана

## Bot как live-артефакт

`/bot/` — исполняемый MVP Run 1, физически в корне **по инфраструктурной причине**: `.github/workflows/bot.yml` триггерится на путь `bot/**`. Перенос сломает CI/CD (см. [bot-stays-at-root.md](knowledge/decisions/bot-stays-at-root.md)).

- Любая разработка в `bot/` — **через spec-kit** (см. [`bot/AGENTS.md`](bot/AGENTS.md))
- Если Run 3 решит делать своего бота — код идёт в `runs/run-3-founder-coach/stages/7-mvp/`, не в `/bot/`
- `/bot/prompts/`, `/bot/spec/`, `/bot/src/` — продакшен-артефакты, не перемещать без freeze Run 1 с передачей MVP

## Обязательные MCP-серверы

**Context7** (`context7`) — документация по библиотекам и API. При старте сессии агент **обязан** проверить доступность Context7 через `ToolSearch` с запросом `context7`. Если инструменты не загружены — **немедленно сообщить пользователю**.

## Правила деплоя

- **Код — только через git.** Все изменения доставляются через `git push` → GitHub Actions. Никогда не редактировать на сервере по SSH
- **SSH — только для не-git операций:** `.env`, gitignored конфиги, `docker compose restart`, логи
- **Запрет `git push` внутри сессий Claude** — см. [CLAUDE.md](CLAUDE.md). Агент может делать коммиты / теги / ветки локально, но push делает пользователь

## Язык

**Все разговоры с пользователем — строго на русском.** Технические идентификаторы и имена файлов — в оригинале. Контент артефактов — на языке, в котором написан.

## Быстрая карта знаний

- Governing methodology: [Метод параноика](knowledge/methodology/метод-параноика.md)
- Pipeline: [v1 charter](pipeline-templates/v1/README.md)
- Архитектурные решения: [knowledge/decisions/](knowledge/decisions/)
- Урок Run 1 → Run 2: [b2b-eap-pivot-to-consulting](knowledge/learnings/b2b-eap-pivot-to-consulting.md)
- Seed Run 3: [founder-coach-group-mode](knowledge/learnings/founder-coach-group-mode.md)
