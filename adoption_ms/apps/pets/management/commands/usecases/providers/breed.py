from faker.providers import BaseProvider

# List of dog breeds
DOG_BREEDS = (
    "Labrador Retriever",
    "German Shepherd",
    "Golden Retriever",
    "Bulldog",
    "Beagle",
    "Poodle",
    "French Bulldog",
    "Siberian Husky",
    "Dachshund",
    "Boxer",
)

# List of cat breeds
CAT_BREEDS = (
    "Siamese",
    "Persian",
    "Maine Coon",
    "Ragdoll",
    "Bengal",
    "British Shorthair",
    "Sphynx",
    "Scottish Fold",
    "Russian Blue",
    "American Shorthair",
)


class AnimalBreedsProvider(BaseProvider):
    def dog_breed(self):
        return self.random_element(DOG_BREEDS)

    def cat_breed(self):
        return self.random_element(CAT_BREEDS)
