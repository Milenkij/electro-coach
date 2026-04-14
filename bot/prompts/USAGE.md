# Prompt Stack Usage

## Default Stack

Всегда загружай:

1. `prompts/base/base-identity.md`
2. `prompts/base/safety-and-boundaries.md`

В большинстве полноценных коучинговых диалогов также загружай:

3. `prompts/playbook/coach-playbook.md`

## Conditional Retrieval

Подгружай тематические карточки только по необходимости:

- `prompts/cards/goal-pursuit.md`
- `prompts/cards/self-esteem-and-self-trust.md`
- `prompts/cards/systems-thinking.md`
- `prompts/cards/self-sabotage-patterns.md`
- `prompts/cards/adhd-like-patterns.md`

## Suggested Loading Logic

- если тема общая и ещё не ясна: `base + safety + playbook`
- если тема про цели и исполнение: добавить `goal-pursuit`
- если много самокритики и шаткой опоры: добавить `self-esteem-and-self-trust`
- если проблема циклическая и структурная: добавить `systems-thinking`
- если повторяются разрушительные сценарии: добавить `self-sabotage-patterns`
- если выражены проблемы запуска, времени, хаоса, гиперфокуса: добавить `adhd-like-patterns`

## Token Discipline

Не старайся загружать всё сразу.

Рабочий принцип:

- always-loaded stack должен оставаться компактным;
- retrieval cards включаются только когда реально повышают точность ответа;
- при сомнении лучше загрузить меньше и ответить чище.

## Operational Rule

Если диалог становится слишком теоретическим, сокращай слой знаний до:

- `base identity`
- `safety`
- 1 релевантная карточка

Это обычно лучше, чем перегруженный контекст с дублирующимися идеями.

## Transfer Rule For Other Projects

Если knowledge base переносится в другой проект, её нужно переносить не отдельными markdown-файлами, а связанными пакетами.

Минимальный переносимый runtime bundle:

- `prompts/base/base-identity.md`
- `prompts/base/safety-and-boundaries.md`
- `prompts/playbook/coach-playbook.md`
- `prompts/USAGE.md`

Retrieval cards нельзя переносить отдельно от этого bundle.

Полный protocol переноса и готовый prompt для внешнего агента лежат в:

- `prompts/playbook/knowledge-base-transfer-playbook.md`
- `prompts/EXTERNAL_AGENT_TRANSFER_PROMPT.md`
