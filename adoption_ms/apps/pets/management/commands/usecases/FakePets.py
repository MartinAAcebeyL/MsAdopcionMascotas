import random

from faker import Faker
from typing import Tuple

from . import bolivian_places_provider, FakePetNamesProvider, AnimalBreedsProvider


class FakePet:
    def __init__(self) -> None:
        self.fake = Faker(["es_ES", "en_US"])
        self.fake.add_provider(bolivian_places_provider)
        self.fake.add_provider(FakePetNamesProvider)
        self.fake.add_provider(AnimalBreedsProvider)

    def fake_name(self) -> str:
        return self.fake.fake_pet_name()

    def fake_history(self) -> str:
        return self.fake.text(max_nb_chars=50)

    def fake_age(self) -> Tuple[int, str]:
        age = random.randint(0, 15)
        time = "años"
        if not age:
            age = random.randint(0, 11)
            time = "meses"
        return age, time

    def fake_person_submit_pet(self):
        """
        This method is still under construction
        """

    def fake_breed(self):
        dog_breeds = self.fake.dog_breed
        cat_breeds = self.fake.cat_breed

        return random.choice([dog_breeds(), cat_breeds()])

    def fake_city(self) -> str:
        return self.fake.bolivian_places_provider()

    def fake_sex(self) -> str:
        return random.choice(["F", "M"])

    def fake_size(self) -> int:
        return random.choice(["small", "middle", "big"])

    def fake_status(self):
        return random.choice(["progress", "adopted", "able"])
