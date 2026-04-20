# Archive — Source Materials

Исходные материалы, из которых экстрактированы карточки `/knowledge/` и промпты шаблона `/pipeline-templates/`.

Хранятся здесь для воспроизводимости и ссылок из карточек. Не редактируются — только как источник.

## Карта экстракции

### paranoid-method.pdf

Книга «Метод параноика» (Артур Абрамов). 514 страниц. Governing methodology пайплайна v1.

Экстрактированные карточки:
- `/knowledge/methodology/метод-параноика.md` — meta-карточка
- `/knowledge/methodology/воронка-неопределённости.md`
- `/knowledge/methodology/5-принципов-параноика.md`
- `/knowledge/methodology/продюсерская-модель.md`
- `/knowledge/methodology/проджект-раннер.md`
- `/knowledge/methodology/типы-проектов.md`
- `/knowledge/decisions/paranoid-as-governing-methodology.md`

**Copyright hygiene:** в карточках хранятся только тезисы и суффиксы-ссылки на главы PDF, не полные цитаты.

### founder-diagnostic.md

«Диагностика основателя», исходник из Клуба менторов. Структура первой встречи с фаундером.

Экстрактированные промпты (вошли в Stage 0 шаблона):
- `pipeline-templates/v1/stages/0-team-constitution/prompts/00-founder-diagnostic-prep.md`
- `pipeline-templates/v1/stages/0-team-constitution/prompts/01-founder-interview.md`
- `pipeline-templates/v1/stages/0-team-constitution/prompts/02-founder-balance-wheel.md`

Тонкая карточка: `/knowledge/methodology/диагностика-основателя.md`

### team-diagnostic.md

«Диагностика команды», исходник из Клуба менторов. Структура работы с командой на старте.

Экстрактированные промпты (вошли в Stage 0 шаблона):
- `pipeline-templates/v1/stages/0-team-constitution/prompts/03-team-core-mapping.md`
- `pipeline-templates/v1/stages/0-team-constitution/prompts/04-team-interviews.md`
- `pipeline-templates/v1/stages/0-team-constitution/prompts/05-communication-assessment.md`
- `pipeline-templates/v1/stages/0-team-constitution/prompts/06-team-constitution.md`

Тонкая карточка: `/knowledge/methodology/диагностика-команды.md`

## Когда добавляется новый источник

1. Положить файл в `archive/source-materials/`
2. Обновить эту README с картой экстракции
3. Создать связанные карточки `/knowledge/` с ссылкой на исходник
