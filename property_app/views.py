from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.gis.db.models.functions import Distance

from .models import Property
from .search import combined_location_search


def home(request):
    featured = (
        Property.objects.select_related("location")
        .order_by("-id")
        .filter(status="available")[:6]
    )
    return render(request, "property_app/home.html", {"featured": featured})


def property_list(request):
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "").strip()
    properties = Property.objects.select_related("location")

    if query:
        matched_locations = combined_location_search(query, top_k=10)
        if matched_locations:
            location_ids = [loc.id for loc in matched_locations]
            properties = properties.filter(location__id__in=location_ids)
        else:
            properties = properties.none()

    sort_options = {
        "price_asc": "price",
        "price_desc": "-price",
    }
    properties = properties.order_by(sort_options.get(sort, "-id"))
    paginator = Paginator(properties, 9)
    page = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "property_app/property_list.html",
        {
            "page": page,
            "query": query,
            "sort": sort if sort in sort_options else "",
        },
    )


def property_detail(request, slug):
    property_obj = get_object_or_404(
        Property.objects.select_related("location").annotate(
            distance_from_city=Distance("point", "location__point")
        ),
        slug=slug,
    )

    distance_km = None
    if property_obj.distance_from_city is not None:
        distance_km = round(property_obj.distance_from_city.km, 1)

    return render(
        request,
        "property_app/property_detail.html",
        {
            "property": property_obj,
            "distance_km": distance_km,
        },
    )


def location_autocomplete(request):
    query = request.GET.get("q", "").strip()
    if len(query) < 2:
        return JsonResponse([], safe=False)

    locations = combined_location_search(query, top_k=6)
    return JsonResponse(
        [{"name": loc.name, "slug": loc.slug} for loc in locations],
        safe=False,
    )
