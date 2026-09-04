import httpx
from app.config import settings

LOOPS_API_URL = "https://app.loops.so/api/v1"

async def send_new_contact_request_email(
    client_name: str,
    pet_name: str | None,
    client_email: str,
    whatsapp: str,
    country: str,
) -> dict:
    """Notifica al admin por email que llegó una nueva solicitud de contacto"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{LOOPS_API_URL}/transactional",
            headers={
                "Authorization": f"Bearer {settings.LOOPS_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "email": settings.ADMIN_EMAIL,
                "transactionalId": settings.LOOPS_TRANSACTIONAL_ID,
                "dataVariables": {
                    "clientName": client_name,
                    "petName": pet_name or "No especificado",
                    "clientEmail": client_email,
                    "whatsapp": whatsapp,
                    "country": country,
                },
            },
        )
        return response.json()


async def subscribe_contact_to_promotions(email: str, first_name: str) -> dict:
    """Agrega o actualiza un contacto marcándolo como suscrito a promociones"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{LOOPS_API_URL}/contacts/create",
            headers={
                "Authorization": f"Bearer {settings.LOOPS_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "email": email,
                "firstName": first_name,
                "subscribed": True,
                "source": "Formulario de contacto",
            },
        )
        return response.json()
