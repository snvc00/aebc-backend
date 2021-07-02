import random
import string

from ...models import *
from django.core.management.base import BaseCommand
from django.core import management
from django_seed import Seed


class Command(BaseCommand):
    """
    """

    def add_arguments(self, parser):
        parser.add_argument('number', type=int)

    def random_array(self, beg: int, end: int, length: int):
        result = []
        for i in range(length):
            result.append(random.randint(beg, end))
        return result

    def handle(self, *args, **kwargs):
        management.call_command("flush", verbosity=0, interactive=False)

        seeder = Seed.seeder()
        number = kwargs.get("number", 10)

        seeder.add_entity(Client, number, {
            "name": lambda x: seeder.faker.name(),
            "email": lambda x: "{id}_{email}".format(id="".join(random.choices(string.ascii_uppercase + string.digits, k=10)), email=seeder.faker.email()),
            "rfc": lambda x: "".join(random.choices(string.ascii_uppercase + string.digits, k=13)),
            "curp": lambda x: "".join(random.choices(string.ascii_uppercase + string.digits, k=18))
        })
        seeder.add_entity(Employee, number, {
            "name": lambda x: seeder.faker.name(),
            "email": lambda x: "{id}_{email}".format(id="".join(random.choices(string.ascii_uppercase + string.digits, k=10)), email=seeder.faker.email()),
            "rfc": lambda x: "".join(random.choices(string.ascii_uppercase + string.digits, k=13)),
            
        })
        seeder.add_entity(Insurance, number, {
            "max_protection": lambda x: random.randint(0, 10000)
        })
        seeder.add_entity(Promotion, number)
        seeder.add_entity(CreditCard, number, {
            "min_credit": lambda x: random.randint(0, 1000),
            "max_credit": lambda x: random.randint(1000, 3000)
        })
        seeder.add_entity(PreapprovalRequest, number)

        inserted_pks = seeder.execute()
        print(inserted_pks)

        credit_cards = CreditCard.objects.all()
        for credit_card in credit_cards:
            ids = self.random_array(1, number - 1, round(number / 2))
            credit_card.insurances.set(map(lambda id: Insurance.objects.get(id=id), ids))
            credit_card.promotions.set(map(lambda id: Promotion.objects.get(id=id), ids))

        print("Promotions and insurances were added to credit cards")
