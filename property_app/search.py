from sentence_transformers import SentenceTransformer
from pgvector.django import CosineDistance
from .models import Location

_model = None


# Lazy loading the model
def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def semantic_location_search(query: str, top_k: int = 6) -> list:
    """
    Encode query text and return the top_k Locations
    ordered by cosine similarity to their stored embeddings.
    """
    query_vector = get_model().encode(query).tolist()
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
    exact = list(Location.objects.filter(name__icontains=query)[:top_k])
    if exact:
        return exact
    return semantic_location_search(query, top_k)
