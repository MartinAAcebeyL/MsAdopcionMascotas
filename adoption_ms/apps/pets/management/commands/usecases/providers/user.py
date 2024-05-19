import random

from adoption_ms.apps.pets.models import Pet
class PersonProvider:
    def fake_user(self) -> None:
        all_users = Pet.get_all_users()
        print(all_users)
        return random.choice(all_users)
