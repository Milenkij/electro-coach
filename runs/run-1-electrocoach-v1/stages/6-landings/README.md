# Stage 6 — Landings

## Цель

Собрать лендинги под сегменты: тексты, дизайн, квизы (если много сегментов). Цель — проверить гипотезу через реальные клики и заявки.

## Inputs

- PRD из Stage 4
- Нейминг / brand из Stage 5
- Core Jobs из Stage 2

## Prompts

- `landing-page-text.md` — генерация текста лендинга под сегмент (перенесено из Run 1)
- `landing-design.md` — дизайн-направление, секционная структура (перенесено из Run 1)
- `ajtbd-landing.md` — лендинг из AJTBD-анализа (перенесено из Run 2)

## Outputs

- `results/landing-<segment>.html` — по одному лендингу на сегмент (или один общий квиз-хаб)
- `results/landing-copy-<segment>.md` — тексты отдельно от вёрстки
- `results/site-b2c/`, `results/site-b2b/` — если ран имеет две ветки аудитории

## Patterns

- [Dark landing system](../../../../knowledge/patterns/dark-landing-system.md) — dark theme, Sora/Outfit, IntersectionObserver, standalone HTML
- [Quiz hub pattern](../../../../knowledge/patterns/quiz-hub-pattern.md) — 3-вопросный квиз → профилирование → подходящий лендинг
