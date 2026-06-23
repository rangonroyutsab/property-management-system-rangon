import pandas as pd
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from property_app.models import Location, Property, PropertyImage


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str)

    def handle(self, *args, **options):
        df = pd.read_csv(options["csv_path"])

        with transaction.atomic():
            for _, row in df.iterrows():
                latitude = float(row["latitude"])
                longitude = float(row["longitude"])
                point = Point(longitude, latitude)

                location, _ = Location.objects.get_or_create(
                    name=row["location_name"],
                    defaults={
                        "slug": slugify(row["location_name"]),
                        "point": point,
                    },
                )

                slug = slugify(row["title"])

                property_obj, _ = Property.objects.get_or_create(
                    slug=slug,
                    defaults={
                        "location": location,
                        "title": row["title"],
                        "description": row["description"],
                        "property_type": row["property_type"],
                        "status": row["status"],
                        "price": row["price"],
                        "bedrooms": int(row["bedrooms"]),
                        "bathrooms": int(row["bathrooms"]),
                        "amenities": row["amenities"],
                        "point": point,
                    },
                )

                image_urls = row.get("image_urls", "")

                if pd.notna(image_urls) and str(image_urls).strip():
                    urls = [
                        image_url.strip()
                        for image_url in str(image_urls).split("|")
                        if image_url.strip()
                    ]

                    has_primary = property_obj.images.filter(is_primary=True).exists()

                    for index, image_url in enumerate(urls):
                        _, image_created = PropertyImage.objects.get_or_create(
                            property=property_obj,
                            url=image_url,
                            defaults={
                                "caption": property_obj.title,
                                "is_primary": index == 0 and not has_primary,
                            },
                        )

                        if image_created and index == 0 and not has_primary:
                            has_primary = True

        self.stdout.write(self.style.SUCCESS("Import complete."))
