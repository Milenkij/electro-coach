---
id: grow
title: GROW
type: methodology
tags: [coaching, conversation-model]
related_runs: [run-1-electrocoach-v1, run-3-founder-coach]
pipeline_versions: [v1]
related_cards: [dilts-logical-levels]
created: 2026-04-20
---

Модель коучинговой беседы, стандарт de facto в McKinsey / Google / ICF. Применяется в Run 1 как основа диалога Telegram-бота.

## Четыре блока беседы

- **G — Goal** — что хочешь получить в результате сессии
- **R — Reality** — что сейчас, что реально происходит (факты, а не интерпретации)
- **O — Options** — какие варианты есть (минимум 3, включая неочевидные)
- **W — Will / Way forward** — что конкретно сделаешь и когда

## Принципы использования

- Коуч не даёт советов и не ведёт — только **задаёт вопросы** и отражает
- Один вопрос за раз
- На этапе Options — разнообразие важнее экспертности
- На этапе Will — конкретное действие с датой, а не «я подумаю»

## Как реализовано в боте

- `bot/prompts/playbook/` — операционные ходы по блокам GROW
- `bot/prompts/product-rules.md` — правила тайминга и UX
- `bot/prompts/base/` — идентичность коуча, правила безопасности

Детали методологии — в `bot/prompts/` как конкретная имплементация; эта карточка — указатель и контекст.
