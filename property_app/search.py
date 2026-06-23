from django.db.models import Q
from pgvector.django import CosineDistance

from .embeddings import get_query_embedding
from .models import Location


def semantic_location_search(query: str, top_k: int = 6) -> list:
    """
    Encode query text and return the top_k Locations
    ordered by cosine similarity to their stored embeddings.
    """
    query_vector = get_query_embedding(query)
    return list(
        Location.objects.filter(embedding__isnull=False).order_by(
            CosineDistance("embedding", query_vector)
        )[:top_k]
    )


def combined_location_search(query: str, top_k: int = 6) -> list:
    """
    Try exact text match first. Fall back to semantic search
    only when text match returns nothing.
    """
    exact = list(
        Location.objects.filter(
            Q(name__icontains=query)
            | Q(city__icontains=query)
            | Q(state__icontains=query)
            | Q(country__icontains=query)
        )[:top_k]
    )

    if exact:
        return exact

    return semantic_location_search(query, top_k)
