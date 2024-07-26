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
def create_groups(sender, instance, created, **kwargs):
    if created:
        for group_name in GROUP_NAMES:
            Group.objects.create(name=group_name, user=instance)


@receiver(post_save, sender=User)
def save_groups(sender, instance, **kwargs):
    for group in instance.group_set.all():
        group.save()


@receiver(post_save, sender=User)
def create_categories(sender, instance, created, **kwargs):
    if created:
        groups = Group.objects.all().exclude(name='Other')
        for group in groups:
            Category.objects.create(name='Other', group=group, user=instance)


@receiver(post_save, sender=User)
def save_categories(sender, instance, **kwargs):
    for category in instance.category_set.all():
        category.save()
