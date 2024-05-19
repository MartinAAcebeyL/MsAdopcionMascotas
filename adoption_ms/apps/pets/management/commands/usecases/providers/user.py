import random
from faker.providers import BaseProvider
from apps.pets.models import Pet
class PersonProvider(BaseProvider):
    def fake_user(self) -> None:
        all_users = Pet.get_all_users()
        return random.choice(all_users)
