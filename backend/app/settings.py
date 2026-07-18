import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[2] / ".env")


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-5.6")
    onemap_access_token: str | None = os.getenv("ONEMAP_ACCESS_TOKEN")
    supabase_url: str | None = os.getenv("SUPABASE_URL")
    supabase_key: str | None = os.getenv("SUPABASE_KEY")

    @property
    def has_openai(self) -> bool:
        return bool(self.openai_api_key)

    @property
    def has_onemap(self) -> bool:
        return bool(self.onemap_access_token)

    @property
    def has_supabase(self) -> bool:
        return bool(self.supabase_url and self.supabase_key)


settings = Settings()
