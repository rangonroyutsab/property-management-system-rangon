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
    list_filter = ("property_type", "status", "bedrooms")
    search_fields = ("title", "description", "location__name")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PropertyImageInline]


@admin.register(Location)
class LocationAdmin(GISModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


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
