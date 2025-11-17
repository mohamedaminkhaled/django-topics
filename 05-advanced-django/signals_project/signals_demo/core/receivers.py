import logging
from django.dispatch import receiver
from django.db.models.signals import (
    pre_save, post_save, pre_delete, post_delete,
    pre_init, post_init, m2m_changed
)
from django.core.signals import (
    request_started, request_finished, got_request_exception
)
from django.contrib.auth.models import User
from .custom_signals import user_action_signal
from .models import Book, Author

logger = logging.getLogger(__name__)

# -----------------------------------
# Model init signals
# -----------------------------------
@receiver(pre_init)
def before_init(sender, *args, **kwargs):
    if sender.__name__ != "WSGIRequest":  # avoid spamming
        logger.info(f"[pre_init] Initializing model: {sender.__name__}")


@receiver(post_init)
def after_init(sender, instance, **kwargs):
    if sender.__name__ != "WSGIRequest":
        logger.info(f"[post_init] Initialized: {instance}")


# -----------------------------------
# Save/Delete signals
# -----------------------------------
@receiver(pre_save, sender=Book)
def before_book_save(sender, instance, **kwargs):
    logger.info(f"[pre_save] Book about to save: {instance.title}")


@receiver(post_save, sender=Book)
def after_book_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"[post_save] New Book created: {instance.title}")
    else:
        logger.info(f"[post_save] Book updated: {instance.title}")


@receiver(pre_delete, sender=Book)
def before_book_delete(sender, instance, **kwargs):
    logger.info(f"[pre_delete] Book about to delete: {instance.title}")


@receiver(post_delete, sender=Book)
def after_book_delete(sender, instance, **kwargs):
    logger.info(f"[post_delete] Book deleted: {instance.title}")


# -----------------------------------
# Many-to-Many signals
# -----------------------------------
@receiver(m2m_changed, sender=Book.tags.through)
def book_tags_changed(sender, instance, action, pk_set, **kwargs):
    logger.info(f"[m2m_changed] Book={instance.title}, action={action}, tags={pk_set}")


# -----------------------------------
# Request signals
# -----------------------------------
@receiver(request_started)
def on_request_started(sender, environ, **kwargs):
    logger.info("[request_started] A request has started")


@receiver(request_finished)
def on_request_finished(sender, **kwargs):
    logger.info("[request_finished] A request has finished")


@receiver(got_request_exception)
def on_exception(sender, request, **kwargs):
    logger.error("[got_request_exception] Django caught an exception")


# -----------------------------------
# Custom signal receiver
# -----------------------------------
@receiver(user_action_signal)
def on_user_action(sender, **kwargs):
    logger.info(f"[custom_signal] User action received: {kwargs}")
