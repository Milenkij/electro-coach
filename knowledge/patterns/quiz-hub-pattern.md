---
id: quiz-hub-pattern
title: Quiz Hub Pattern
type: pattern
tags: [frontend, ux, conversion]
related_runs: [run-1-electrocoach-v1]
pipeline_versions: [v1]
related_cards: [dark-landing-system]
created: 2026-04-20
---

Паттерн стартовой страницы с квизом, которая профилирует пользователя в 3 вопроса и перенаправляет на сегментный лендинг.

## Ключевые принципы

1. **Не навешивает ярлыки.** Результат — ситуация («Кажется, у вас вот такая ситуация»), а не тип личности.
2. **3 вопроса** — баланс точности и конверсии (меньше drop-off, чем 5+).
3. **Fallback `Или выберите сами`** — полная сетка сегментов под результатом, если предсказание не попало.

## Где реализовано

- Run 1 B2C: [site-b2c/index.html](../../runs/run-1-electrocoach-v1/stages/6-landings/results/site-b2c/index.html) — 3 вопроса → 8 B2C-сегментов
- Run 1 B2B: [site-b2b/index.html](../../runs/run-1-electrocoach-v1/stages/6-landings/results/site-b2b/index.html) — размер → вызов → приоритеты → 5 B2B-сегментов

## Почему работает

- Квиз повышает вовлечённость и CTR на целевой лендинг
- Профилирование (а не ярлык) не вызывает сопротивления
- Fallback защищает от ложноотрицательных результатов
