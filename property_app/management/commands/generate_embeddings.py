from django.core.management.base import BaseCommand

from property_app.models import Location


class Command(BaseCommand):
    def handle(self, *args, **options):
        locations = Location.objects.all()
        total = locations.count()

        if total == 0:
            return

        for loc in locations:
            loc.save()
            self.stdout.write(f"{loc.name} - done!")

        self.stdout.write(self.style.SUCCESS(f"\nEmbedded {total} location(s)."))
