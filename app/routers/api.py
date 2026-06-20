from app.repositories.metrics_repository import MetricsRepository
from fastapi import APIRouter, Depends, Request
from app.schemas import ContactRequest, ContactResponse, MetricsResponse
from app.services.contact_service import ContactService
from app.dependencies import get_contact_service, get_metrics_repo

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/health")
async def health():
    """Эндпоинт для проверки состояния сервиса."""
    return {"status": "ok"}


@router.post("/contact", response_model=ContactResponse)
async def create_contact_request(
    contact_request: ContactRequest,
    http_request: Request,
    service: ContactService = Depends(get_contact_service),
):

    await service.submit_contact_request(
        data=contact_request,
        client_ip=http_request.client.host,
    )
    return ContactResponse(message="Request submitted successfully")


@router.get(
    "/metrics",
    response_model=MetricsResponse,
)
def metrics(metrics_repo: MetricsRepository = Depends(get_metrics_repo)):
    return metrics_repo.get_metrics()
