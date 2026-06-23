from django.core.management.base import BaseCommand
from sentence_transformers import SentenceTransformer
from property_app.models import Location


class Command(BaseCommand):
    def handle(self, *args, **options):
        locations = Location.objects.filter(embedding__isnull=True)
        total = locations.count()

        if total == 0:
            return

        model = SentenceTransformer("all-MiniLM-L6-v2")

        for loc in locations:
            loc.embedding = model.encode(loc.name).tolist()
            loc.save(update_fields=["embedding"])
            self.stdout.write(f"{loc.name} - done!")

        self.stdout.write(self.style.SUCCESS(f"\nEmbedded {total} location(s)."))
