-- Сценарий 9: мульти-участник
ALTER TABLE sessions
  ADD COLUMN IF NOT EXISTS participant_count INT NOT NULL DEFAULT 1,
  ADD COLUMN IF NOT EXISTS participants JSONB;

-- Сценарий 10: отключение paywall для всех существующих пользователей
UPDATE users SET subscription_until = '2030-01-01 00:00:00+00';
