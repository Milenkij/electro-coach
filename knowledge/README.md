# Knowledge Base

Библиотека переиспользуемого знания проекта. Отделена от конкретных ранов — здесь живёт то, что применимо за рамками одного эксперимента.

## Структура

- [`methodology/`](methodology/) — методологические рамки, применяемые в пайплайне (GROW, Дилтс, AJTBD, Метод параноика, диагностики, Landor 8, Lexicon Diamond, Naming playbook)
- [`patterns/`](patterns/) — переиспользуемые технические / продуктовые паттерны (Dark landing system, Quiz hub pattern, AJTBD graph visualization)
- [`learnings/`](learnings/) — уроки, извлечённые из ранов (что работает / что не работает и почему)
- [`decisions/`](decisions/) — архитектурные решения по платформе (copy-at-start, frozen-per-run, stage-0 gating, etc.)

## Формат карточки

Каждая карточка — отдельный markdown-файл с frontmatter:

```markdown
---
id: <slug>
title: <читаемое имя>
type: methodology | pattern | learning | decision
tags: [тег1, тег2]
related_runs: [run-id, ...]
pipeline_versions: [v1]
related_cards: [другой-slug, ...]
created: YYYY-MM-DD
---

<тело карточки>
```

**Рекомендуемая длина:** ≤ 40 строк тела. Карточка — указатель и контекст, не учебник. Для развёрнутого материала — ссылка на `archive/source-materials/` или внешний источник.

## Как использовать

- В `MOC.md` каждого рана — ссылки на релевантные карточки по стадиям.
- При старте нового рана — пройти по `/knowledge/methodology/` и отметить, что применяется.
- Learnings из завершённых ранов — обязательный шаг заморозки (freeze): что вынесли, чего не ожидали.
