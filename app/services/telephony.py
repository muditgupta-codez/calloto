import httpx

from app.config import settings


class VoxvaaniClient:
    BASE_URL = "https://api.voxvaani.com/v1"

    def __init__(self):
        self.api_key = settings.voxvaani_api_key
        self.api_secret = settings.voxvaani_api_secret

    async def _headers(self) -> dict:
        return {
            "X-API-Key": self.api_key,
            "X-API-Secret": self.api_secret,
            "Content-Type": "application/json",
        }

    async def drop_call(self, call_id: str) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/calls/{call_id}/hangup",
                headers=await self._headers(),
            )
            return response.status_code == 200

    async def send_whatsapp(self, to: str, body: str, from_number: str) -> str | None:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/whatsapp/send",
                headers=await self._headers(),
                json={"to": to, "body": body, "from": from_number},
            )
            if response.status_code == 200:
                return response.json().get("message_id")
            return None

    async def send_sms(self, to: str, body: str, from_number: str) -> str | None:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/sms/send",
                headers=await self._headers(),
                json={"to": to, "body": body, "from": from_number},
            )
            if response.status_code == 200:
                return response.json().get("message_id")
            return None

    async def provision_number(self, country: str = "GB") -> str | None:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/numbers/purchase",
                headers=await self._headers(),
                json={"country": country},
            )
            if response.status_code == 200:
                return response.json().get("number")
            return None

    async def health_check(self) -> bool:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/health",
                    headers=await self._headers(),
                    timeout=5.0,
                )
                return response.status_code == 200
            except httpx.RequestError:
                return False


voxvaani_client = VoxvaaniClient()
