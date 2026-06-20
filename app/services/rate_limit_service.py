from collections import defaultdict
from datetime import datetime, timedelta
from app.config import settings
from app.exceptions import RateLimitExceededError


class RateLimitService:
    """Сервис для ограничения частоты запросов."""

    def __init__(self) -> None:
        self.rate_limit_storage = defaultdict(list)

    def check_rate_limit(self, email: str, client_ip: str) -> None:
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=settings.RATE_LIMIT_SECONDS)
        key = f"{client_ip}:{email}"
        requests = self.rate_limit_storage.get(key, [])

        requests = [ts for ts in requests if ts > window_start]

        if len(requests) >= settings.RATE_LIMIT_MAX_REQUESTS:
            raise RateLimitExceededError()

        requests.append(now)
        self.rate_limit_storage[key] = requests
