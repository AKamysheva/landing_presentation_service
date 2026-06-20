from app.services.rate_limit_service import RateLimitService
from app.services.contact_service import ContactService
from app.services.email_service import EmailService
from app.services.ai_service import AIService
from app.repositories.metrics_repository import MetricsRepository

rate_limit_service = RateLimitService()


def get_contact_service():
    email_service = EmailService()
    ai_service = AIService()
    metrics_repo = get_metrics_repo()
    contact_service = ContactService(
        email_service, rate_limit_service, ai_service, metrics_repo
    )
    return contact_service


def get_metrics_repo():
    metrics_repo = MetricsRepository()
    return metrics_repo
