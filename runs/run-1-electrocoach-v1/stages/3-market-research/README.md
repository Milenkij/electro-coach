# Stage 3 — Market Research

## Цель

Проверить гипотезу через рынок: конкуренты, тренды, отзывы, данные. Подкрепить сегменты из Stage 2 числами.

## Inputs

- Сегменты из Stage 2
- RAT-сегмент (приоритетный)

## Prompts

- (4 prompt-файла из `4-Working-with-data/prompts/` — переносятся сюда из Run 1)

## Outputs

- `results/competitors.md` — анализ конкурентов
- `results/trends.md` — макротренды, поддерживающие гипотезу
- `results/reviews-analysis.md` — JTBD, извлечённые из отзывов существующих решений
- `results/data/` — сырые данные (reviews JSON, exit-survey, support-tickets, subscription-events)
- `results/production-user-analysis.md` — анализ боевых пользователей (если есть работающий продукт-прекурсор)

## Methodology

- [JTBD extraction from reviews](../../../../knowledge/methodology/jtbd-extraction-from-reviews.md)
- [Метод параноика — типы проектов](../../../../knowledge/methodology/типы-проектов.md) — инверсный формат оценки
