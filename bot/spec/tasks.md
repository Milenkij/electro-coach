# Tasks: ElectroCoach Bot MVP

## Этап 1: Инфраструктура
- [x] .gitignore
- [x] .env / .env.example
- [x] spec-kit документы (constitution, spec, plan, tasks)
- [ ] Структура папок + requirements.txt

## Этап 2: Core модули
- [ ] config.py — загрузка настроек
- [ ] db.py — asyncpg клиент + миграция SQL
- [ ] llm.py — OpenRouter клиент
- [ ] session.py — управление сессиями

## Этап 3: Бот
- [ ] bot.py — aiogram handlers
- [ ] main.py — точка входа

## Этап 3.1: Нетекстовые сообщения (Сценарий 4)
- [x] В `bot.py` handle_text: вместо молчаливого return на нетекстовые сообщения — ответить пользователю

## Этап 4: Тестирование
- [ ] Локальный запуск
- [ ] Прогон полного сценария сессии

## Этап 5: Деплой
- [ ] PostgreSQL на VPS
- [ ] Код на VPS
- [ ] systemd service
- [ ] Боевой тест
