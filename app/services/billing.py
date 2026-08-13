import httpx

from app.config import settings


class PaddleClient:
    BASE_URL = "https://api.paddle.com"

    def __init__(self):
        self.api_key = settings.paddle_api_key

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def health_check(self) -> bool:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/products",
                    headers=self._headers(),
                    timeout=5,
                )
                return response.status_code == 200
            except httpx.RequestError:
                return False


paddle_client = PaddleClient()
