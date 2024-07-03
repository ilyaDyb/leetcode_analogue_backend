from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.cache import cache

from .models import Problem


@receiver(post_save, sender=Problem)
def drop_cache_after_problem_creating(created, **kwargs):
    if created:
        cache_key = "all_problems"
        cache.delete(cache_key)