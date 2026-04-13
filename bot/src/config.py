import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load .env from bot/ directory
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_path)


@dataclass(frozen=True)
class Config:
    telegram_token: str
    openrouter_api_key: str
    database_url: str
    openrouter_model: str = "@preset/electrocoach"
    free_sessions_limit: int = 2

    @classmethod
    def from_env(cls) -> "Config":
        token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
        if not token:
            raise ValueError("TELEGRAM_BOT_TOKEN is not set")

        api_key = os.environ.get("OPENROUTER_API_KEY", "")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY is not set")

        database_url = os.environ.get(
            "DATABASE_URL",
            "postgresql://electrocoach:password@localhost:5432/electrocoach",
        )

        return cls(
            telegram_token=token,
            openrouter_api_key=api_key,
            database_url=database_url,
            openrouter_model=os.environ.get(
                "OPENROUTER_MODEL", "@preset/electrocoach"
            ),
        )


config = Config.from_env()
