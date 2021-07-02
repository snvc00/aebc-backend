from ...models import Employee, Client
from django.core.management.base import BaseCommand
from django_seed import Seed
import os

class Command(BaseCommand):
    """
    """
    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()
        testing_client = os.environ.get("DJANGO_TESTING_CLIENT")
        testing_admin = os.environ.get("DJANGO_TESTING_ADMIN")

        if Client.objects.filter(email=testing_client).first() is None:
            seeder.add_entity(Client, 1, {
                "name": "Client",
                "email": testing_client,
                "rfc": "RFCXXXXXXXXXX",
                "curp": "CURPXXXXXXXXXXXXXX",
                "income": 1000000
            })

        if Employee.objects.filter(email=testing_admin).first() is None:
            seeder.add_entity(Employee, 1, {
                "name": "Admin",
                "email":  testing_admin,
                "rfc": "RFCXXXXXXXXXX"
            })

        inserted_pks = seeder.execute()
        print(inserted_pks)
