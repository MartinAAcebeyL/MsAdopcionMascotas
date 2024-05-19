import random
from faker.providers import BaseProvider


class FakePetNamesProvider(BaseProvider):
    prefixes = [
        "Fluffy",
        "Whiskers",
        "Mittens",
        "Fido",
        "Spot",
        "Buddy",
        "Lucky",
        "Spike",
        "Shadow",
        "Princess",
    ]
    suffixes = [
        "Paws",
        "Snuggles",
        "Wags",
        "Nose",
        "Furball",
        "Chomp",
        "Tail",
        "Whiskers",
        "Bark",
        "Purr",
    ]

    def fake_pet_name(self):
        prefix = random.choice(FakePetNamesProvider.prefixes)
        suffix = random.choice(FakePetNamesProvider.suffixes)
        return prefix + " " + suffix
