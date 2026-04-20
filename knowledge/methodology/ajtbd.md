---
id: ajtbd
title: Advanced Jobs To Be Done (AJTBD)
type: methodology
tags: [segmentation, jtbd, discovery]
related_runs: [run-2-second-look, run-3-founder-coach]
pipeline_versions: [v1]
related_cards: [jtbd-extraction-from-reviews, ajtbd-graph-viz]
created: 2026-04-20
---

Расширение классического JTBD. В AJTBD «работа» разделяется на граф: **надзадача → задача → подзадача**, а рядом — конкурирующие способы решения и триггеры.

## Ключевые добавления к JTBD

- **Граф работ**, а не список — видно, где задача «в служении» более высокой работы
- **Конкурирующие решения** в рамках одной задачи — явно (не только «альтернативы», а все способы)
- **Триггеры** — что запускает потребность решать задачу
- **Препятствия** — что мешает завершить работу

## Применение в Run 2

AJTBD-карта работ фаундера — центральный артефакт рана:
- [run-2 / ajtbd-analysis.md](../../runs/run-2-second-look/stages/2-segmentation/results/ajtbd-analysis.md)
- [run-2 / ajtbd-graph/](../../runs/run-2-second-look/stages/2-segmentation/results/ajtbd-graph/)

Инсайт, породивший Run 3: «персональное использование — не prerequisite для группового, а параллельная точка входа; ~15% — третий путь "персональное в служении групповому"».

## Как применять в ране

1. Начать с топовой работы («фаундер развивает бизнес»)
2. Раскладывать вниз до уровня, где видны конкретные триггеры
3. Для каждой задачи — фиксировать текущие способы решения (конкуренты)
4. Проверять гипотезу продукта против графа: куда именно встраиваемся

## Связанные промпты

- `pipeline-templates/v1/stages/2-segmentation/prompts/ajtbd-segments-b2c.md`
- `pipeline-templates/v1/stages/2-segmentation/prompts/ajtbd-segments-b2b.md`
- `pipeline-templates/v1/stages/2-segmentation/prompts/ajtbd-rat.md`
