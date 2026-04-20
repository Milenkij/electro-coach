---
id: bot-stays-at-root
title: Bot stays at /bot (CI path contract)
type: decision
tags: [architecture, ci-cd, constraints]
related_runs: [run-1-electrocoach-v1]
pipeline_versions: [v1]
related_cards: []
created: 2026-04-20
---

## Решение

Папка `/bot/` остаётся в корне репозитория, НЕ переносится в `runs/run-1-electrocoach-v1/stages/7-mvp/`.

## Почему

- **CI/CD контракт:** `.github/workflows/bot.yml` триггерится на изменения в `bot/**`. Перенос сломает автодеплой в продакшен
- **Боль миграции пути не окупается:** код работает, задеплоен, обновляется. Реструктура ради формального соответствия — риск без выгоды
- **В meta.yml Run 1 это отражено:** `mvp_artifact.path: /bot` — lineage явный

## Как читать структуру

- `runs/run-1-electrocoach-v1/` — весь research / PRD / landings / аналитика
- `/bot/` — исполняемый MVP этого рана, «вынесен наружу» по инфраструктурной причине
- `runs/run-1-electrocoach-v1/stages/7-mvp/README.md` — описывает, что MVP физически в `/bot/`

## Если Run 3 решит собирать своего бота

Код нового бота идёт в `runs/run-3-founder-coach/stages/7-mvp/`, **не в корень**. Это значит — CI/CD пайплайн для нового бота описывается отдельно, не переиспользует `bot.yml`.

Исключение: если новый бот заменяет старый (а не живёт параллельно) и использует ту же инфру — тогда можно обновить `bot/` и зафиксировать это как freeze Run 1 с передачей MVP в Run 3.
