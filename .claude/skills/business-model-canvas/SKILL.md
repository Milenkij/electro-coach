---
name: business-model-canvas
description:
  Design and analyze business models using the Business Model Canvas framework.
  Use when evaluating startups, planning new products, pivoting existing
  businesses, analyzing competitors, or documenting a business model.
  Project-level entry point — delegates to business-model/SKILL.md.
---

# Business Model Canvas — project entry point

Это тонкий wrapper. **Единственный источник правды — `business-model/SKILL.md`** в корне проекта.

## Как выполнять

1. Прочитай `business-model/SKILL.md` целиком. Это процессный документ. Методология — в `knowledge/methodology/osterwalder/` (см. Knowledge map в SKILL.md). Читай нужные файлы оттуда по ходу работы.
2. Прочитай `business-model/README.md` — там индекс существующих канвасов и конвенции именования.
3. Уточни у пользователя предмет канваса (продукт / гипотеза / сегмент / конкурент), если не задан в аргументах.
4. Сохрани результат в `business-model/canvases/<name>.md`, где `<name>` — kebab-case, отражает предмет (`electrocoach-b2c.md`, `competitor-airbnb.md`, `pivot-v2.md`).
5. Обнови секцию «Индекс канвасов» в `business-model/README.md` — добавь ссылку на новый файл.

## Границы

- **Канвы и индекс** — в `business-model/`.
- **Методология** — в `knowledge/methodology/osterwalder/`. Читать по ссылкам, не дублировать в канву.
- Один файл = один канвас.
- Если канвас с таким именем уже существует — спроси пользователя: обновить существующий или создать новую версию (`<name>-v2.md`).
