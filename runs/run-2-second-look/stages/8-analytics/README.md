# Stage 8 — Analytics

## Цель

Измерить ран: воронки, unit economics, траектория. Вывести learnings. Принять решение по ране: продолжаем / замораживаем / делаем pivot → новый ран.

## Inputs

- MVP из Stage 7, работающий на реальных пользователях
- Лендинги из Stage 6 с траффиком
- PRD из Stage 4 (метрики успеха)

## Prompts

*(stubs — пайплайн v1 не фиксировал analytics в явном виде, будем дополнять)*

## Outputs

- `results/funnels.md` — воронки (пошагово, по сегментам, по каналам)
- `results/business-model.md` или `unit-economics.md` — экономика
- `results/learnings.md` — что узнали, что удивило, что подтвердилось
- `results/decision.md` — решение по ране: freeze / pivot / scale
- `results/dashboard.html` — визуализация (при необходимости)

## When run becomes frozen

- В `meta.yml` → `status: frozen`, `frozen_at: <дата>`
- Learnings экстрактируются в `/knowledge/learnings/<slug>.md` с ссылкой на этот ран
