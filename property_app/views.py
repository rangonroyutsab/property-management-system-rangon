from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.gis.db.models.functions import Distance

from .models import Property, Location


def home(request):
    featured = Property.objects.select_related("location").order_by("-id")[:4]
    return render(request, "property_app/home.html", {"featured": featured})


def property_list(request):
    query = request.GET.get("q", "").strip()
    properties = Property.objects.select_related("location")

    if query:
        properties = properties.filter(
            Q(location__name__icontains=query) | Q(title__icontains=query)
        )

    properties = properties.order_by("-id")
    paginator = Paginator(properties, 9)
    page = paginator.get_page(request.GET.get("page"))

    return render(request, "property_app/property_list.html", {
        "page": page,
        "query": query,
    })


def property_detail(request, slug):
    property_obj = get_object_or_404(
        Property.objects.select_related("location").annotate(
            distance_from_city=Distance("point", "location__point")
        ),
        slug=slug,
    )
    return render(request, "property_app/property_detail.html", {
        "property": property_obj,
    })


def location_autocomplete(request):
    query = request.GET.get("q", "").strip()
    if len(query) < 2:
        return JsonResponse([], safe=False)

    locations = Location.objects.filter(name__icontains=query).values("name", "slug")[:6]
    return JsonResponse(list(locations), safe=False)


