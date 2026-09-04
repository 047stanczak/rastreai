import os


class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/rastreiaai",
    )
    JWT_SECRET: str = os.getenv("JWT_SECRET", "change-me")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

    LINKE_TRACK_TOKEN: str = os.getenv("LINKE_TRACK_TOKEN", "")
    LINKE_TRACK_BASE_URL: str = os.getenv(
        "LINKE_TRACK_BASE_URL", "https://seurastreio.com.br"
    )

    TRACKING_INTERVAL_MINUTES: int = int(os.getenv("TRACKING_INTERVAL_MINUTES", "10"))

    CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
        if origin.strip()
    ]


settings = Settings()
