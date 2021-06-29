from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    """
    """
    def handle(self, *args, **kwargs):
        DJANGO_SU_PASSWORD = os.environ.get("DJANGO_SU_PASSWORD")

        if User.objects.get(username="aecb-admin") is None:
            User.objects.create_superuser("aecb-admin", "admin@aecb.com", DJANGO_SU_PASSWORD)
            print("aecb-admin user created")
        else:
            print("aecb-admin already exists")
