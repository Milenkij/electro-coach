---
id: single-knowledge-kb
title: Single /knowledge/ KB across all runs
type: decision
tags: [architecture, knowledge-management]
related_runs: [run-1-electrocoach-v1, run-2-second-look, run-3-founder-coach]
pipeline_versions: [v1]
related_cards: [copy-at-start, pipeline-frozen-per-run]
created: 2026-04-20
---

## Решение

Одна библиотека знаний `/knowledge/` на весь проект. НЕ раскладываем карточки внутрь ранов.

## Альтернатива, которую отвергли

Per-run KB: `runs/run-N-.../knowledge/`. Каждый ран имел бы свою копию карточек.

## Почему единая

- Карточки описывают **переиспользуемое знание**. Если знание применимо только к одному рану — это не карточка, а артефакт рана (живёт в `stages/N/results/`)
- Обновление карточки сразу видно всем ранам (в отличие от пайплайна — промпты копируются, карточки нет)
- Нет drift между версиями одной и той же карточки

## Как линкуется

- В каждом `runs/run-N-.../MOC.md` — секции по стадиям со ссылками на релевантные карточки `/knowledge/`
- Во frontmatter карточки — поле `related_runs` для обратной навигации

## Что делать с knowledge, которое стало устаревшим

- Не удалять карточку (она описывает решение в контексте определённого времени)
- Добавить секцию «Что изменилось» со ссылкой на новую карточку
- Или пометить `status: superseded` во frontmatter и дать ссылку на преемника
