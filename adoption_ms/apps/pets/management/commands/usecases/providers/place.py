from faker.providers import DynamicProvider

# List of Bolivian cities
CITIES = (
    "La Paz",
    "Santa Cruz",
    "Cochabamba",
    "Sucre",
    "Tarija",
    "Oruro",
    "Potosí",
    "Beni",
    "Pando",
    "El Alto",
)

bolivian_places_provider = DynamicProvider(
    provider_name="bolivian_places_provider",
    elements=CITIES,
)
