---
id: dark-landing-system
title: Dark Landing System (ElectroCoach)
type: pattern
tags: [frontend, landing, design-system]
related_runs: [run-1-electrocoach-v1]
pipeline_versions: [v1]
related_cards: [quiz-hub-pattern]
created: 2026-04-20
---

Дизайн-система для лендингов ElectroCoach. Standalone HTML без билд-системы (CSS и JS инлайн).

## Спецификация

- **Тема:** dark — фон `#111318`, accent `#5b8def`
- **Шрифты:** Sora (заголовки), Outfit (текст) — Google Fonts
- **Анимации:** IntersectionObserver, класс `.r` → `.r.v`, задержки `.d1`–`.d4`
- **Адаптив:** CSS Grid, media queries на 820px и 640px

## Структура типового лендинга

- `hero` с болью
- «Узнаёшь себя?» триггеры (B2C) / статистика (B2B)
- Чат-мокап или фичи
- Сравнение с альтернативами (B2B)
- FAQ
- CTA → Telegram-бот (B2C) / форма пилота (B2B)

## Где живут артефакты

- Run 1 B2C: [site-b2c/](../../runs/run-1-electrocoach-v1/stages/6-landings/results/site-b2c/)
- Run 1 B2B: [site-b2b/](../../runs/run-1-electrocoach-v1/stages/6-landings/results/site-b2b/)
- Run 2 B2B v2 (светлая тема Torch): [landing.html](../../runs/run-2-second-look/stages/6-landings/results/landing.html) — **отступление от этого паттерна**, отдельная система

## Принципы

- Ты-форма для B2C, эмоциональный тон
- Вы-форма для B2B, деловой тон + ROI-метрики
- Каждый лендинг = одна боль, не просто подстановка заголовка
