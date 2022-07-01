from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import User
from trainer.models import Statistic


@receiver(post_save, sender=User, dispatch_uid="create_users_typing_statistics")
def create_users_typing_statistics(sender, **kwargs):
    if kwargs.get('created'):
        Statistic.objects.create(user=kwargs.get('instance'))
