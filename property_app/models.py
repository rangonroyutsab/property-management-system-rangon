from django.contrib.gis.db import models
from pgvector.django import VectorField


class Location(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True) 
    point = models.PointField(geography=True, srid=4326) 
    embedding = VectorField(dimensions=384, null=True, blank=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="properties")
    title = models.CharField(max_length=255) 
    slug = models.SlugField(unique=True)    
    description = models.TextField(blank=True) 
    property_type = models.CharField(max_length=50) 
    status = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=12, decimal_places=2) 
    bedrooms = models.PositiveSmallIntegerField(default=0) 
    bathrooms = models.PositiveSmallIntegerField(default=0) 
    amenities = models.TextField(blank=True) 
    point = models.PointField(geography=True, srid=4326)

    def __str__(self):
        return self.title
    
    def primary_image(self):
        return self.images.filter(is_primary=True).first() or self.images.first()  


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="properties/%Y/%m/") 
    caption = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False) 