from app.constants import SENTIMENT_MAP
from app.schemas import ContactRequest
from app.services.email_service import EmailService
from app.services.rate_limit_service import RateLimitService
from app.services.ai_service import AIService
from app.repositories.metrics_repository import MetricsRepository
from app.logging import logger


class ContactService:
    """
    Сервис для обработки контактных запросов пользователей.

    Основные задачи:
    - Проверка лимитов запросов (rate limiting) по email и IP-адресу.
    - Анализ тональности комментария с помощью внешнего AI-сервиса.
      При ошибке анализа используется fallback-значение "unknown".
    - Регистрация метрик по результатам анализа тональности.
    - Отправка писем владельцу сайта и пользователю через EmailService.
    """

    def __init__(
        self,
        email_service: EmailService,
        rate_limit_service: RateLimitService,
        ai_service: AIService,
        metrics_repo: MetricsRepository,
    ) -> None:
        self.email_service = email_service
        self.rate_limit_service = rate_limit_service
        self.ai_service = ai_service
        self.metrics_repo = metrics_repo

    async def submit_contact_request(
        self,
        data: ContactRequest,
        client_ip: str,
    ):

        self.rate_limit_service.check_rate_limit(data.email, client_ip)

        try:
            sentiment = await self.ai_service.analyze(data.comment)
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            sentiment = "not_analyzed"

        sentiment = SENTIMENT_MAP.get(sentiment, "unknown")

        self.metrics_repo.collect_metrics(sentiment)

        await self.email_service.send_contact_emails(data, sentiment)
