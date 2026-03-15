import requests
from django.conf import settings

HEADERS = {
    "Authorization": f"Bearer {settings.DAILY_API_KEY}",
    "Content-Type": "application/json",
}


def create_room(name: str = None, expires_in_seconds: int = 3600):
    """Создать комнату в Daily.co"""
    import time

    payload = {
        "properties": {
            "exp": int(time.time()) + expires_in_seconds,  # время жизни комнаты
            "enable_chat": True,
            "enable_screenshare": True,
            "start_video_off": False,
            "start_audio_off": False,
        }
    }

    if name:
        payload["name"] = name  # если не указать — Daily сгенерирует сам

    response = requests.post(
        f"{settings.DAILY_API_URL}/rooms",
        json=payload,
        headers=HEADERS,
    )
    response.raise_for_status()
    return response.json()


def get_room(room_name: str):
    """Получить информацию о комнате"""
    response = requests.get(
        f"{settings.DAILY_API_URL}/rooms/{room_name}",
        headers=HEADERS,
    )
    response.raise_for_status()
    return response.json()


def delete_room(room_name: str):
    """Удалить комнату"""
    response = requests.delete(
        f"{settings.DAILY_API_URL}/rooms/{room_name}",
        headers=HEADERS,
    )
    response.raise_for_status()
    return response.json()


def create_meeting_token(room_name: str, user_name: str = None, is_owner: bool = False):
    """Создать токен доступа для участника"""
    import time

    payload = {
        "properties": {
            "room_name": room_name,
            "exp": int(time.time()) + 3600,
            "is_owner": is_owner,  # True = модератор
        }
    }

    if user_name:
        payload["properties"]["user_name"] = user_name

    response = requests.post(
        f"{settings.DAILY_API_URL}/meeting-tokens",
        json=payload,
        headers=HEADERS,
    )
    response.raise_for_status()
    return response.json()