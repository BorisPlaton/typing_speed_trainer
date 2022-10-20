from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from account.models import User
from account.services import create_user_statistic, create_user_profile
from type_results.services import delete_all_user_cached_results


@receiver(post_save, sender=User, dispatch_uid="create_users_typing_statistics")
def create_users_typing_statistics(sender, **kwargs):
    """Creates a `Statistic` model after a `User` creation."""
    if kwargs.get('created'):
        create_user_statistic(kwargs.get('instance'))


@receiver(post_save, sender=User, dispatch_uid="create_users_profile")
def create_users_profile(sender, **kwargs):
    """Creates a `Profile` model after a `User` creation."""
    if kwargs.get('created'):
        create_user_profile(kwargs.get('instance'))


@receiver(pre_delete, sender=User, dispatch_uid="delete_all_cached_user_results")
def delete_all_cached_user_results(sender, **kwargs):
    """
    Deletes all user's cached results from cache if
    the `User` model is deleted.
    """
    instance: User = kwargs.get('instance')
    delete_all_user_cached_results(instance.pk)
