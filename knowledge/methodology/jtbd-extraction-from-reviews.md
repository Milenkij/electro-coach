---
id: jtbd-extraction-from-reviews
title: Извлечение JTBD из отзывов и разговоров
type: methodology
tags: [jtbd, research, extraction]
related_runs: [run-1-electrocoach-v1, run-2-second-look]
pipeline_versions: [v1]
related_cards: [ajtbd]
created: 2026-04-20
---

Техника вытаскивания «работ» из сырого материала — отзывов, интервью, переписок с ботом.

## Что ищем в сыром тексте

- **Контекст** — когда человек «нанимал» продукт
- **Триггер** — что заставило искать решение
- **Попытки** — что пробовал до этого, почему не сработало
- **Критерий успеха** — по чему понял, что сработало / не сработало

## Сигналы в языке

- «когда…», «каждый раз как…», «бывает что…» — контекст
- «последней каплей стало…», «после того как…» — триггер
- «сначала пробовал…», «думал сработает…» — попытки
- «теперь я…», «стало…» — критерий

## Применение

- `pipeline-templates/v1/stages/3-market-research/prompts/extract-jobs-from-reviews.md` — готовый промпт
- Run 1: [jobs-from-conversations.md](../../runs/run-1-electrocoach-v1/stages/3-market-research/results/jobs-from-conversations.md) — извлечено из разговоров пользователей бота
