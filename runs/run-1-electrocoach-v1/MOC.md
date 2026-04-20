# Run 1 — ElectroCoach v1 — MOC

Map of Content рана. Индекс по стадиям: артефакты рана + карточки `/knowledge/`, использованные или извлечённые.

**Статус:** frozen (2026-04-17). MVP — Telegram-бот в [`/bot`](../../bot/).

---

## Stage 0 — Team Constitution [historical gap]

Ран прошёл до введения Stage 0. См. [STUB](stages/0-team-constitution/results/STUB.md).

Команда рана (по факту): соло-фаундер — Кирилл Миленкий.

---

## Stage 1 — Discovery

Discovery для Run 1 не велся отдельной стадией — гипотеза сформулирована до начала пайплайна v1. Сырой seed — идея «AI-коуч в Telegram на базе GROW + Дилтс».

Карточки:
- [GROW](../../knowledge/methodology/grow.md)
- [Логические уровни Дилтса](../../knowledge/methodology/dilts-logical-levels.md)

---

## Stage 2 — Segmentation

13 сегментов B2C/B2B, проработаны через лендинги. AJTBD как отдельный инструмент в этом ране не применялся (введён в Run 2).

Артефакты рана — вшиты в 8 B2C + 5 B2B лендингов (см. Stage 6).

---

## Stage 3 — Market Research

Артефакты:
- [competitor-research.md](stages/3-market-research/results/competitor-research.md)
- [market-trends-research.md](stages/3-market-research/results/market-trends-research.md)
- [differentiation-strategy.md](stages/3-market-research/results/differentiation-strategy.md)
- [jobs-from-conversations.md](stages/3-market-research/results/jobs-from-conversations.md)
- [research.html](stages/3-market-research/results/research.html), [research-dashboard.html](stages/3-market-research/results/research-dashboard.html)
- [data/](stages/3-market-research/results/data/) — бот-аналитика и production-user-анализ (2026-04-17)

Карточки:
- [JTBD extraction from reviews](../../knowledge/methodology/jtbd-extraction-from-reviews.md)

---

## Stage 4 — PRD

Артефакт: [PRD.md](stages/4-prd/results/PRD.md) — MVP scope, JTBD, метрики.

---

## Stage 5 — Naming & Brand

Артефакт: [PLAYBOOK.md](stages/5-naming-brand/results/PLAYBOOK.md) — полный playbook, применённый в ране. Финальный нейминг не выбран — «ElectroCoach» остаётся рабочим.

Карточки:
- [Naming playbook](../../knowledge/methodology/naming-playbook.md)
- [Lexicon Diamond](../../knowledge/methodology/lexicon-diamond.md)
- [Landor 8 Principles](../../knowledge/methodology/landor-8-principles.md)

---

## Stage 6 — Landings

Артефакты:
- [index.html](stages/6-landings/results/index.html) — стартовый лендинг (для себя / для бизнеса)
- [site-b2c/](stages/6-landings/results/site-b2c/) — квиз-хаб + 8 сегментных лендингов
- [site-b2b/](stages/6-landings/results/site-b2b/) — квиз-хаб + 5 сегментных лендингов
- [b2b.html](stages/6-landings/results/b2b.html), [my-landing-page-text.md](stages/6-landings/results/my-landing-page-text.md)

Карточки:
- [Dark landing system](../../knowledge/patterns/dark-landing-system.md)
- [Quiz hub pattern](../../knowledge/patterns/quiz-hub-pattern.md)

---

## Stage 7 — MVP

MVP — Telegram-бот. Код живёт в корне репозитория: [`/bot`](../../bot/). Причина — CI/CD контракт GitHub Actions на путь `bot/**`.

Методология разработки бота: spec-kit (см. [`bot/AGENTS.md`](../../bot/AGENTS.md) и [`bot/spec/`](../../bot/spec/)).

---

## Stage 8 — Analytics

Артефакты:
- [funnels.md](stages/8-analytics/results/funnels.md) — воронки по 13 сегментам, unit economics, цель 1M ₽/мес
- [dashboard.html](stages/8-analytics/results/dashboard.html)

---

## Learnings

- [B2B EAP → консалтинг pivot](../../knowledge/learnings/b2b-eap-pivot-to-consulting.md) — урок, который породил Run 2

## Residual

- [what-to-do.md](what-to-do.md) — исходная раскладка воркшопа, по которой начинался ран (историческая заметка)
