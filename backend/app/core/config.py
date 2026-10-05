from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RecoFlow"
    app_env: str = "development"
    debug: bool = True

    database_url: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    cors_origins: str = "http://localhost:8501,http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @model_validator(mode="after")
    def validate_runtime_settings(self) -> "Settings":
        if self.app_env.lower() in {"production", "staging"}:
            if self.debug:
                raise ValueError("DEBUG must be false in production-like environments.")
            if len(self.jwt_secret_key) < 32 or self.jwt_secret_key.startswith("change-this"):
                raise ValueError(
                    "JWT_SECRET_KEY must be a strong, non-placeholder secret "
                    "in production-like environments."
                )
            if any("localhost" in origin or "127.0.0.1" in origin for origin in self.cors_origin_list):
                raise ValueError(
                    "CORS_ORIGINS must not contain local development origins "
                    "in production-like environments."
                )
        return self

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()