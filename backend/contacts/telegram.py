"""
Telegram bot orqali admin'larga xabar yuborish.

Bot: @dgd_consulting_bot
Adminlar TELEGRAM_ADMIN_IDS settingida ko'rsatilgan.
"""
import json
import logging
from urllib import request as urlrequest, parse as urlparse, error as urlerror

from django.conf import settings

logger = logging.getLogger(__name__)

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


def _escape_html(text):
    """Telegram HTML parse_mode uchun maxsus belgilarni qochirish."""
    if text is None:
        return ""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def send_telegram_message(text, chat_id=None):
    """
    Telegram bot orqali bitta admin'ga xabar yuborish.
    Token yoki chat_id bo'lmasa, jim turadi (request fail bo'lmasligi uchun).
    Returns: True agar yuborilgan bo'lsa, aks holda False.
    """
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", "") or ""
    if not token or not chat_id:
        return False

    url = TELEGRAM_API.format(token=token)
    payload = urlparse.urlencode({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": "true",
    }).encode("utf-8")

    req = urlrequest.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urlrequest.urlopen(req, timeout=8) as resp:
            body = resp.read().decode("utf-8", errors="ignore")
            data = json.loads(body) if body else {}
            if not data.get("ok"):
                logger.warning("Telegram API javobi: %s", body[:300])
                return False
            return True
    except urlerror.HTTPError as e:
        logger.warning("Telegram HTTPError %s: %s", e.code, e.reason)
    except urlerror.URLError as e:
        logger.warning("Telegram URLError: %s", e.reason)
    except Exception as e:
        logger.exception("Telegram bot xatosi: %s", e)
    return False


def notify_admins_contact(submission):
    """
    Yangi ContactSubmission yaratilganda barcha admin'larga xabar yuborish.
    Returns: muvaffaqiyatli yuborilgan admin'lar soni.
    """
    admin_ids = getattr(settings, "TELEGRAM_ADMIN_IDS", []) or []
    if not admin_ids:
        return 0

    text = (
        "🆕 <b>DGD Consulting — Yangi so'rov</b>\n"
        "\n"
        f"👤 <b>Ism:</b> {_escape_html(submission.name)}\n"
        f"🏢 <b>Kompaniya:</b> {_escape_html(submission.company or '—')}\n"
        f"📞 <b>Telefon:</b> {_escape_html(submission.phone)}\n"
        f"🛠 <b>Xizmat:</b> {_escape_html(submission.get_service_display())}\n"
        "\n"
        f"📝 <b>Loyiha izohi:</b>\n{_escape_html(submission.notes or '—')}\n"
        "\n"
        f"🕒 {submission.created_at.strftime('%Y-%m-%d %H:%M')}"
    )

    sent = 0
    for admin_id in admin_ids:
        if send_telegram_message(text, chat_id=admin_id):
            sent += 1
    return sent
