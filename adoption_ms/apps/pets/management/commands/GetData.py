import requests
import json

from django.core.management.base import BaseCommand, CommandError


class GetData:
    URL: str = "https://dogapi.dog/api/v2/groups"

    def get_groups_data(self):
        try:
            response = requests.get(GetData.URL)
            data = response.json()
            return data
        except Exception as e:
            raise CommandError(e)


class SafeData:
    pass


class Command(BaseCommand):
    help = "Get data from the Dog API"

    def handle(self, *args, **options):
        data = GetData().get_data()
        print(json.dumps(data, indent=4))
        # self.stdout.write(self.style.SUCCESS("Data saved successfully"))
