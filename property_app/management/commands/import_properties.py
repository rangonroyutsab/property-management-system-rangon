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
                city = self.clean_value(row["city"])
                state = self.clean_value(row["state"])
                country = self.clean_value(row["country"])

                location_name = self.build_location_name(city, state, country)
                location_slug = slugify(location_name)

                location_latitude = float(row["location_latitude"])
                location_longitude = float(row["location_longitude"])
                location_point = Point(location_longitude, location_latitude, srid=4326)

                property_latitude = float(row["property_latitude"])
                property_longitude = float(row["property_longitude"])
                property_point = Point(property_longitude, property_latitude, srid=4326)

                location, _ = Location.objects.get_or_create(
                    slug=location_slug,
                    defaults={
                        "city": city,
                        "state": state,
                        "country": country,
                        "point": location_point,
                    },
                )

                slug = slugify(f"{row['title']}-{location_name}")

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
                        "point": property_point,
                    },
                )

                primary_image_url = row.get("primary_image_url", "")

                if pd.notna(primary_image_url) and str(primary_image_url).strip():
                    PropertyImage.objects.get_or_create(
                        property=property_obj,
                        url=str(primary_image_url).strip(),
                        defaults={
                            "caption": property_obj.title,
                            "is_primary": True,
                        },
                    )

                image_urls = row.get("image_urls", "")
                image_captions = row.get("image_captions", "")

                if pd.notna(image_urls) and str(image_urls).strip():
                    urls = [
                        image_url.strip()
                        for image_url in str(image_urls).split("|")
                        if image_url.strip()
                    ]

                    captions = []

                    if pd.notna(image_captions) and str(image_captions).strip():
                        captions = [
                            caption.strip()
                            for caption in str(image_captions).split("|")
                        ]

                    has_primary = property_obj.images.filter(is_primary=True).exists()

                    for index, image_url in enumerate(urls):
                        caption = property_obj.title

                        if index < len(captions) and captions[index]:
                            caption = captions[index]

                        _, image_created = PropertyImage.objects.get_or_create(
                            property=property_obj,
                            url=image_url,
                            defaults={
                                "caption": caption,
                                "is_primary": index == 0 and not has_primary,
                            },
                        )

                        if image_created and index == 0 and not has_primary:
                            has_primary = True

        self.stdout.write(self.style.SUCCESS("Import complete."))

    def clean_value(self, value):
        if pd.isna(value):
            return ""

        return str(value).strip()

    def build_location_name(self, city, state, country):
        return ", ".join(part for part in [city, state, country] if part)
