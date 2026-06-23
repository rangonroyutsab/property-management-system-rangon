from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from django.utils.html import format_html

from .models import Location, Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ("image", "url", "preview", "caption", "is_primary")
    readonly_fields = ("preview",)

    def preview(self, obj):
        src = obj.get_image_url()
        if src:
            return format_html(
                '<img src="{}" style="height: 60px; border-radius: 4px;" />', src
            )
        return "-"

    preview.short_description = "Preview"


@admin.register(Property)
class PropertyAdmin(GISModelAdmin):
    list_display = (
        "title",
        "location",
        "price",
        "bedrooms",
        "bathrooms",
        "property_type",
        "status",
    )
    list_filter = (
        "property_type",
        "status",
        "bedrooms",
        "location__country",
        "location__state",
        "location__city",
    )
    search_fields = (
        "title",
        "description",
        "location__name",
        "location__city",
        "location__state",
        "location__country",
    )
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PropertyImageInline]


@admin.register(Location)
class LocationAdmin(GISModelAdmin):
    list_display = ("name", "city", "state", "country", "slug")
    list_filter = ("country", "state", "city")
    search_fields = ("name", "city", "state", "country")
    readonly_fields = ("name", "slug")
    exclude = ("embedding",)


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ("property", "is_primary", "preview")
    list_filter = ("is_primary",)
    readonly_fields = ("preview",)

    def preview(self, obj):
        src = obj.get_image_url()
        if src:
            return format_html(
                '<img src="{}" style="height: 60px; border-radius: 4px;" />',
                src,
            )
        return "-"

    preview.short_description = "Preview"
