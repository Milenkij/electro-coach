# ElectroCoach — Runs Platform

Платформа для запуска экспериментов (runs) над гипотезой AI-коуча для фаундеров и людей в точке перемен.

Не один продукт, а набор версионированных ранов на общем шаблоне пайплайна. Каждый ран — отдельная гипотеза, проходящая через 9 стадий под управлением [Метода параноика](knowledge/methodology/метод-параноика.md) (governing methodology).

## Карта репозитория

| Директория | Назначение |
|---|---|
| [`pipeline-templates/v1/`](pipeline-templates/v1/) | Шаблон пайплайна v1. Read-only для ранов. 9 стадий от Team Constitution до Analytics |
| [`runs/`](runs/) | Раны — каждый со своей копией шаблона и своими артефактами |
| [`knowledge/`](knowledge/) | Библиотека знания: methodology, patterns, learnings, decisions |
| [`archive/workshop/`](archive/workshop/) | Frozen учебные материалы (историческая раскладка) |
| [`archive/source-materials/`](archive/source-materials/) | Исходники для экстракта в knowledge |
| [`bot/`](bot/) | Live Telegram-бот — MVP Run 1, остаётся в корне по CI-контракту |

## Текущие раны

| ID | Название | Статус | Стадия |
|---|---|---|---|
| [`run-1-electrocoach-v1`](runs/run-1-electrocoach-v1/MOC.md) | ElectroCoach v1 (B2C + B2B-as-EAP) | frozen | — |
| [`run-2-second-look`](runs/run-2-second-look/MOC.md) | Второй взгляд (B2B-консалтинг, пивот от Run 1) | frozen | — |
| [`run-3-founder-coach`](runs/run-3-founder-coach/MOC.md) | Founder-coach (персональный + групповая фасилитация) | **active** | `0-team-constitution` |

## Как сориентироваться за 60 секунд

1. `runs/*/meta.yml` — найти ран с `status: active`
2. В ране: `MOC.md` — индекс по стадиям + карточки knowledge
3. `meta.yml → current_stage` — где работа сейчас
4. Писать артефакты только в `runs/<active>/stages/<current_stage>/results/`

## Как стартовать новый ран

```bash
cp -r pipeline-templates/v1 runs/run-N-<name>
rm runs/run-N-<name>/{meta.template.yml,MOC.template.md}
# Написать meta.yml и MOC.md под конкретный ран
# Пройти Stage 0 — без constitution.md ран не переходит в Discovery
```

Детальный guide — в [AGENTS.md](AGENTS.md).

## Governing methodology: Метод параноика

Неопределённость должна схлопываться быстрее, чем расходуются ресурсы. Каждая стадия пайплайна — шаг воронки неопределённости. Пять принципов: проектирование, гибкие команды, продюсирование, сериал, вовлечённость бизнеса.

Подробнее:
- [Метод параноика (meta)](knowledge/methodology/метод-параноика.md)
- [Воронка неопределённости](knowledge/methodology/воронка-неопределённости.md)
- [5 принципов параноика](knowledge/methodology/5-принципов-параноика.md)
- [Paranoid as governing methodology (decision)](knowledge/decisions/paranoid-as-governing-methodology.md)

## Документы для агентов и контрибьюторов

- [`AGENTS.md`](AGENTS.md) — как агент работает с репо (архитектура, рецепты, gating, bot)
- [`CLAUDE.md`](CLAUDE.md) — правила для Claude Code (язык, push, MCP, bot spec-kit)
- [`knowledge/README.md`](knowledge/README.md) — формат карточек и конвенции KB
- [`bot/AGENTS.md`](bot/AGENTS.md) — spec-kit методология для разработки бота

## Статус

- 3 рана запущено (2 frozen, 1 active)
- Пайплайн v1 — стабилен, 9 стадий
- Telegram-бот задеплоен, CI/CD через GitHub Actions
- Следующий шаг: закрытие Stage 0 в Run 3 (dyad-диагностика Кирилл + Алексей)
