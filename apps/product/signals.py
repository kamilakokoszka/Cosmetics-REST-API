"""Signals creating Groups and Categories."""

from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from apps.core.models import Group, Category


User = get_user_model()

GROUP_NAMES = [
    "Skin care",
    "Hair care",
    "Body care",
    "Makeup",
    "Other"
]


@receiver(post_save, sender=User)
def create_groups_and_categories_for_user(sender, instance, created, **kwargs):
    """Creates groups end 'Other' category in each group (except 'Other')
    when user is created."""
    if created:
        for group_name in GROUP_NAMES:
            group = Group.objects.create(name=group_name, user=instance)
            if group_name != 'Other':
                Category.objects.create(name='Other',
                                        group=group,
                                        user=instance)
