from django.core.management.base import BaseCommand

from .usecases import FakePet
from apps.pets.models import Pet


class Command(BaseCommand):
    help = "Save fake data in pets collection"

    def add_arguments(self, parser):
        parser.add_argument(
            "amount",
            nargs="?",
            type=int,
            default=5,
            help="Number of pets to create",
        )

    def handle(self, *args, **options):
        try:
            pet_model = Pet()
            amount = options.get("amount", 5)
            fake_pet = FakePet()
            for _ in range(amount):
                new_pet = fake_pet.fake_a_pet()
                pet_model.save_a_pet(new_pet)

            self.stdout.write(self.style.SUCCESS("Data saved successfully"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Something was wrong: {e}"))
