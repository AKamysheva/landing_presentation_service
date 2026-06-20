# flake8: noqa: E501
import aiosmtplib
from email.message import EmailMessage
from app.schemas import ContactRequest
from app.config import settings
from app.logging import logger
from app.exceptions import EmailSendError
from app.constants import SENTIMENT_MAP


class EmailService:
    """Сервис для отправки писем владельцу сайта и пользователю."""

    def _build_body(
        self,
        data: ContactRequest,
        sentiment: str,
    ) -> str:
        """Формирует текст письма с данными обращения и тональностью."""

        tonality = SENTIMENT_MAP.get(sentiment, "unknown")

        return (
            f"Имя: {data.name}\n"
            f"Email: {data.email}\n"
            f"Телефон: {data.phone[4:]}\n\n"
            f"Комментарий: {data.comment}\n\n"
            f"Тональность: {tonality}"
        )

    def _build_message(self, to_email: str, subject: str, body: str) -> EmailMessage:
        """Создаёт email-сообщение."""
        message = EmailMessage()
        message["From"] = settings.SMTP_USER
        message["To"] = to_email
        message["Subject"] = subject
        message.set_content(body)
        return message

    async def _send(self, message: EmailMessage, recipient: str):
        """Внутренний метод для отправки письма через SMTP."""
        try:
            await aiosmtplib.send(
                message,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
                start_tls=True,
            )
        except aiosmtplib.SMTPException as e:
            logger.error(f"Failed to send email to {recipient}: {e}")
            raise EmailSendError("Failed to send email") from e
        else:
            logger.info(f"Email sent to {recipient}")

    async def send_contact_emails(self, data: ContactRequest, sentiment: str):
        """Отправляет письмо владельцу и копию пользователю."""
        body = self._build_body(data, sentiment)

        owner_msg = self._build_message(
            to_email=settings.OWNER_EMAIL,
            subject="Обратная связь",
            body=body,
        )
        await self._send(owner_msg, settings.OWNER_EMAIL)

        user_msg = self._build_message(
            to_email=data.email,
            subject="Копия письма",
            body=body,
        )
        await self._send(user_msg, data.email)
