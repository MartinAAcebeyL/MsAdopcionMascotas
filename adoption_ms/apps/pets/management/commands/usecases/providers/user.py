import random
from faker.providers import BaseProvider
from apps.pets.db.models import Pet


class PersonProvider(BaseProvider):
    def fake_user(self) -> None:
        all_users = Pet.get_all_users()
        user = random.choice(all_users)
        user_id = user.get("_id")
        return user_id
