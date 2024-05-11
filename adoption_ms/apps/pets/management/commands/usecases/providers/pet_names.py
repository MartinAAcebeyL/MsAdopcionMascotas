import random


class FakePetNamesProvider:
    def __init__(self):
        self.prefixes = [
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
        self.suffixes = [
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
        prefix = random.choice(self.prefixes)
        suffix = random.choice(self.suffixes)
        return prefix + " " + suffix
