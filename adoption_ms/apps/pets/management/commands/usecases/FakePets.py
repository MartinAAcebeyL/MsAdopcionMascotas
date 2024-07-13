import random

from faker import Faker
from typing import Tuple

from . import (
    bolivian_places_provider,
    FakePetNamesProvider,
    AnimalBreedsProvider,
    PersonProvider,
)


class FakePet:
    def __init__(self) -> None:
        self.fake = Faker(["es_ES"])
        self.fake.add_provider(bolivian_places_provider)
        self.fake.add_provider(FakePetNamesProvider)
        self.fake.add_provider(AnimalBreedsProvider)
        self.fake.add_provider(PersonProvider)

    def _fake_name(self) -> str:
        return self.fake.fake_pet_name()

    def _fake_history(self) -> str:
        return self.fake.text(max_nb_chars=50)

    def _fake_age(self) -> Tuple[int, str]:
        age = random.randint(0, 15)
        time = "años"
        if not age:
            age = random.randint(0, 11)
            time = "meses"
        return age, time

    def _fake_person_submit_pet(self)-> str:
        return self.fake.fake_user()

    def _fake_breed(self):
        dog_breeds = self.fake.dog_breed
        cat_breeds = self.fake.cat_breed

        return random.choice([dog_breeds(), cat_breeds()])

    def _fake_city(self) -> str:
        return self.fake.bolivian_places_provider()

    def _fake_sex(self) -> str:
        return random.choice(["F", "M"])

    def _fake_size(self) -> int:
        return random.choice(["small", "middle", "big"])

    def _fake_status(self):
        return random.choice(["progress", "adopted", "able"])

    def _fake_type(self):
        return random.choice(["Gato", "Perro"])

    def fake_a_pet(self):
        age_value, age_time = self._fake_age()
        return {
            "name": self._fake_name(),
            "history": self._fake_history(),
            "age_value": age_value,
            "age_time": age_time,
            "person": self._fake_person_submit_pet(),
            "breed": self._fake_breed(),
            "type": self._fake_type(),
            "city": self._fake_city(),
            "sex": self._fake_sex(),
            "size": self._fake_size(),
            "status": self._fake_status(),
        }
