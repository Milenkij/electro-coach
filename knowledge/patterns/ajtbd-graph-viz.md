---
id: ajtbd-graph-viz
title: AJTBD Graph Visualization
type: pattern
tags: [visualization, ajtbd, research]
related_runs: [run-2-second-look]
pipeline_versions: [v1]
related_cards: [ajtbd]
created: 2026-04-20
---

Интерактивная визуализация графа работ AJTBD — узлы (надзадача / задача / подзадача) + рёбра (в-служении / конкурирует).

## Функциональность

- **Flat view** — все задачи одним списком с фильтрами
- **Grouped view** — сгруппировано по надзадачам
- **Toggle** — переключение между видами (flat по умолчанию)
- **Интеграция** — `data.json` как единственный источник, обновляется отдельно от HTML

## Где реализовано

- Run 2: [ajtbd-graph/](../../runs/run-2-second-look/stages/2-segmentation/results/ajtbd-graph/) — файлы `index.html` + `data.json` + `README.md`

## Как переиспользовать в новом ране

1. Скопировать `index.html` + `README.md` в `stages/2-segmentation/results/ajtbd-graph/` рана
2. Построить собственный `data.json` из результатов ajtbd-анализа
3. Запускать локально (static HTML, не требует сервера)

## Почему отдельный паттерн

Граф быстро вырастает из списка и становится нечитабельным в линейном markdown. Визуализация экономит время на ориентирование и даёт «wow-эффект» в презентации команде / инвесторам.
