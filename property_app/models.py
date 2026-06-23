from django.contrib.gis.db import models
from django.utils.text import slugify
from pgvector.django import VectorField, HnswIndex

from .embeddings import get_location_embedding


class Location(models.Model):
    name = models.CharField(max_length=255, editable=False)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique=True, editable=False)
    point = models.PointField(geography=True, srid=4326)
    embedding = VectorField(dimensions=384, null=True, blank=True)

    def __str__(self):
        return self.name

    def build_name(self):
        return ", ".join(
            part.strip()
            for part in [self.city, self.state, self.country]
            if part and part.strip()
        )

    def save(self, *args, **kwargs):
        self.name = self.build_name()
        self.slug = slugify(self.name)
        self.embedding = get_location_embedding(self)

        update_fields = kwargs.get("update_fields")

        if update_fields is not None:
            update_fields = set(update_fields)
            update_fields.update({"name", "slug", "embedding"})
            kwargs["update_fields"] = list(update_fields)

        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            HnswIndex(
                name="location_embedding_idx",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            )
        ]


class Property(models.Model):
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="properties"
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    property_type = models.CharField(max_length=50)
    status = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.PositiveSmallIntegerField(default=0)
    bathrooms = models.PositiveSmallIntegerField(default=0)
    amenities = models.TextField(blank=True)
    point = models.PointField(geography=True, srid=4326)

    def __str__(self):
        return self.title

    @property
    def primary_image(self):
        return self.images.filter(is_primary=True).first() or self.images.first()


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="properties/%Y/%m/", blank=True)
    url = models.URLField(max_length=1000, blank=True)
    caption = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)

    def get_image_url(self):
        """Returns whichever image source is available. URL takes priority."""
        if self.url:
            return self.url
        if self.image:
            return self.image.url
        return None
