from django.apps import AppConfig
from watson import search as watson


class VenueConfig(AppConfig):
    name = 'venue'
    def ready(self):
        Venue = self.get_model("Venue")
        watson.register(Venue)

        Band = self.get_model("Band")
        watson.register(Band)