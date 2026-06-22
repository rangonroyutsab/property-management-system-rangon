import pandas as pd
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from property_app.models import Location, Property


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str)

    def handle(self, *args, **options):
        df = pd.read_csv(options["csv_path"])

        with transaction.atomic():
            for _, row in df.iterrows():

                # Find or create the location (avoids duplicate cities)
                location, _ = Location.objects.get_or_create(
                    name=row["location_name"],
                    defaults={
                        "slug": slugify(row["location_name"]),
                        "point": Point(float(row["longitude"]), float(row["latitude"])),
                    },
                )

                # Skip this property if it was already imported
                slug = slugify(row["title"])
                if Property.objects.filter(slug=slug).exists():
                    continue

                Property.objects.create(
                    location=location,
                    title=row["title"],
                    slug=slug,
                    description=row["description"],
                    property_type=row["property_type"],
                    status=row["status"],
                    price=row["price"],
                    bedrooms=int(row["bedrooms"]),
                    bathrooms=int(row["bathrooms"]),
                    amenities=row["amenities"],
                    point=Point(float(row["longitude"]), float(row["latitude"])),
                )

        self.stdout.write(self.style.SUCCESS("Import complete."))
