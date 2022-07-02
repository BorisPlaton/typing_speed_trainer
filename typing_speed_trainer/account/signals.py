from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import User, Profile
from trainer.models import Statistic


@receiver(post_save, sender=User, dispatch_uid="create_users_typing_statistics")
def create_users_typing_statistics(sender, **kwargs):
    """
    Создает запись в таблице `Statistic` с только что созданным
    пользователем.
    """
    if kwargs.get('created'):
        Statistic.objects.create(user=kwargs.get('instance'))


@receiver(post_save, sender=User, dispatch_uid="create_users_profile")
def create_users_profile(sender, **kwargs):
    """
    Создает запись в таблице `Profile` с только что созданным
    пользователем.
    """
    if kwargs.get('created'):
        Profile.objects.create(user=kwargs.get('instance'))
