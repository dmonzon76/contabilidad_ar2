from django.db.models.signals import post_migrate
from django.contrib.sessions.models import Session
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
import logging

logger = logging.getLogger(__name__)


@receiver(post_migrate)
def clear_sessions_on_start(sender, **kwargs):
    # Delete all sessions after migrations are loaded
    Session.objects.all().delete()


@receiver(user_logged_in)
def log_user_logged_in(sender, user, request, **kwargs):
    logger.debug(
        "User logged in: %s, session_keys=%s", user, list(request.session.keys())
    )


@receiver(user_logged_out)
def log_user_logged_out(sender, user, request, **kwargs):
    logger.debug("User logged out: %s", user)
