from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "sqlite+aiosqlite:///./data/calloto.db"
    secret_key: str = "change-me-in-production"
    admin_token: str = "change-me-in-production"

    voxvaani_api_key: str = ""
    voxvaani_api_secret: str = ""
    voxvaani_phone_number: str = ""

    app_url: str = "http://localhost:8000"
    stripe_secret_key: str = ""
    stripe_price_id: str = ""
    stripe_webhook_secret: str = ""
    stripe_tax_enabled: bool = False

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
