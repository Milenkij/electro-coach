# MOC — <Run Name>

Map of Content: карта знаний и артефактов рана. Связывает стадии с карточками в `/knowledge/` и c результатами в `stages/<n>/results/`.

## Run meta

- **ID:** run-N-<slug>
- **Статус:** active | frozen
- **Hypothesis:** см. `meta.yml`
- **Parent run:** null или id
- **Governing methodology:** [Метод параноика](../../knowledge/methodology/метод-параноика.md) · [Воронка неопределённости](../../knowledge/methodology/воронка-неопределённости.md)

---

## Stage 0 — Team Constitution

**Статус:** in-progress | signed | historical-gap

**Участники:** <список>

**Методология:**
- [Диагностика основателя](../../knowledge/methodology/диагностика-основателя.md)
- [Диагностика команды](../../knowledge/methodology/диагностика-команды.md)

**Артефакты:**
- `stages/0-team-constitution/results/constitution.md` (после подписания)

---

## Stage 1 — Discovery

**Методология:** [GROW](../../knowledge/methodology/grow.md) · [Дилтс](../../knowledge/methodology/dilts-logical-levels.md)

**Артефакты:** `stages/1-discovery/results/`

---

## Stage 2 — Segmentation

**Методология:** [AJTBD](../../knowledge/methodology/ajtbd.md) · [JTBD extraction from reviews](../../knowledge/methodology/jtbd-extraction-from-reviews.md)

**Паттерны:** [AJTBD graph visualization](../../knowledge/patterns/ajtbd-graph-viz.md)

**Артефакты:** `stages/2-segmentation/results/`

---

## Stage 3 — Market Research

**Артефакты:** `stages/3-market-research/results/`

---

## Stage 4 — PRD

**Артефакты:** `stages/4-prd/results/`

---

## Stage 5 — Naming & Brand

**Методология:** [Naming Playbook](../../knowledge/methodology/naming-playbook.md) · [Lexicon Diamond](../../knowledge/methodology/lexicon-diamond.md) · [Landor 8 principles](../../knowledge/methodology/landor-8-principles.md)

**Артефакты:** `stages/5-naming-brand/results/`

---

## Stage 6 — Landings

**Паттерны:** [Dark landing system](../../knowledge/patterns/dark-landing-system.md) · [Quiz hub pattern](../../knowledge/patterns/quiz-hub-pattern.md)

**Артефакты:** `stages/6-landings/results/`

---

## Stage 7 — MVP

**Артефакты:** `stages/7-mvp/results/` или external (см. `meta.yml` → `mvp_artifact.path`)

---

## Stage 8 — Analytics

**Артефакты:** `stages/8-analytics/results/`

---

## Learnings (только для frozen-ранов)

- ссылки на `/knowledge/learnings/*.md`, которые экстрактированы из этого рана.
