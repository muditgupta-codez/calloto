import httpx

from app.config import settings


class StripeClient:
    BASE_URL = "https://api.stripe.com/v1"

    def __init__(self):
        self.api_key = settings.stripe_secret_key

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}

    async def create_checkout(self, customer_email: str) -> str | None:
        data = {
            "mode": "subscription",
            "customer_email": customer_email,
            "line_items[0][price]": settings.stripe_price_id,
            "line_items[0][quantity]": "1",
            "billing_address_collection": "required",
            "success_url": f"{settings.app_url}/static/onboarding.html?payment=success",
            "cancel_url": (
                f"{settings.app_url}/static/onboarding.html?payment=cancelled"
            ),
        }
        if settings.stripe_tax_enabled:
            data["automatic_tax[enabled]"] = "true"
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/checkout/sessions",
                headers=self._headers(),
                data=data,
                timeout=15,
            )
        if response.status_code == 200:
            return response.json().get("url")
        return None

    async def health_check(self) -> bool:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/balance",
                    headers=self._headers(),
                    timeout=5,
                )
                return response.status_code == 200
            except httpx.RequestError:
                return False


stripe_client = StripeClient()
