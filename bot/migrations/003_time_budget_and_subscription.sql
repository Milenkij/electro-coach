-- Сценарий 7: тайминг сессии
ALTER TABLE sessions
  ADD COLUMN IF NOT EXISTS time_budget TEXT;

-- Сценарий 8: paywall 72 часа
ALTER TABLE users
  ADD COLUMN IF NOT EXISTS subscription_until TIMESTAMPTZ NOT NULL DEFAULT NOW() + INTERVAL '72 hours';

ALTER TABLE users
  DROP COLUMN IF EXISTS free_sessions_left,
  DROP COLUMN IF EXISTS is_subscribed;
