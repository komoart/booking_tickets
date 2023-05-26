import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        User.objects.create_user(username=os.getenv(
            'NOTIFICATION_ADMIN', default='notification_admin'),
                                 email=os.getenv(
            'NOTIFICATION_ADMIN_EMAIL', default='notification_admin'),
                                 password=os.getenv(
            'NOTIFICATION_ADMIN_PASSWORD', default='notification_admin'),
                                 is_staff=True,
                                 is_active=True,
                                 is_superuser=True
                                 )
