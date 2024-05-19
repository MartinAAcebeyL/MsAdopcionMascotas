from django.core.management.base import BaseCommand, CommandError


from .usecases import FakePet


class Command(BaseCommand):
    help = "Get data from the Dog API"

    def handle(self, *args, **options):
        fake_pet = FakePet()
        print(fake_pet.fake_a_pet())
        # self.stdout.write(self.style.SUCCESS("Data saved successfully"))
