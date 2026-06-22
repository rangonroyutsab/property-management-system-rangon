from django.contrib import admin
from django.utils.html import format_html
from .models import Location, Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ("image", "preview", "caption", "is_primary")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 60px; border-radius: 4px;" />', obj.image.url)
        return "(no image yet)"
    preview.short_description = "Preview"


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "price", "bedrooms", "bathrooms", "property_type", "status")
    list_filter = ("property_type", "status", "bedrooms")
    search_fields = ("title", "description", "location__name")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PropertyImageInline]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}