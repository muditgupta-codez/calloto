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
    paddle_api_key: str = ""
    paddle_price_id: str = ""
    paddle_client_token: str = ""
    paddle_webhook_secret: str = ""
    paddle_tax_enabled: bool = True

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
