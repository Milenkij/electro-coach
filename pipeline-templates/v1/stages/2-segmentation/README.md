# Stage 2 — Segmentation

## Цель

Выделить сегменты, выписать Core Jobs (AJTBD), построить граф работ, найти RAT (reach-addressable-target).

## Inputs

- Гипотеза из Stage 1
- Первичное понимание аудитории

## Prompts

- `ajtbd-segments-b2b.md` — сегментация B2B по AJTBD
- `ajtbd-segments-b2c.md` — сегментация B2C по AJTBD
- `ajtbd-rat.md` — отбор RAT-сегмента (reachable / addressable / targetable)
- `ajtbd-graph-of-work.md` — граф работ ниже уровнем к Core Job

## Outputs

- `results/segments.md` или `segment-analysis.md`
- `results/ajtbd-<segment>.md` для каждого сегмента (Core Job + критерии успеха)
- `results/ajtbd-graph/` — визуализация графа работ (при необходимости)

## Methodology

- [AJTBD](../../../../knowledge/methodology/ajtbd.md)
- [JTBD extraction from reviews](../../../../knowledge/methodology/jtbd-extraction-from-reviews.md)

## Patterns

- [AJTBD graph visualization](../../../../knowledge/patterns/ajtbd-graph-viz.md)
