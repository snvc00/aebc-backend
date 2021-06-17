import random
import string

from aecb.api.models import *
from django.core.management.base import BaseCommand
from django_seed import Seed


class Command(BaseCommand):
    """
    """

    def add_arguments(self, parser):
        parser.add_argument('number', type=int)

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()
        number = kwargs.get("number", 10)
        print(number)

        seeder.add_entity(Client, number, {
            "email": lambda x: "{id}_{email}".format(id="".join(random.choices(string.ascii_uppercase + string.digits, k=10)), email=seeder.faker.email()),
            "rfc": lambda x: "".join(random.choices(string.ascii_uppercase + string.digits, k=13)),
            "curp": lambda x: "".join(random.choices(string.ascii_uppercase + string.digits, k=18))
        })
        seeder.add_entity(Employee, number, {
            "email": lambda x: "{id}_{email}".format(id="".join(random.choices(string.ascii_uppercase + string.digits, k=10)), email=seeder.faker.email()),
            "rfc": lambda x: "".join(random.choices(string.ascii_uppercase + string.digits, k=13)),
            
        })
        seeder.add_entity(Insurance, number)
        seeder.add_entity(Promotion, number)
        seeder.add_entity(CreditCard, number)

        inserted_pks = seeder.execute()
        print(inserted_pks)
