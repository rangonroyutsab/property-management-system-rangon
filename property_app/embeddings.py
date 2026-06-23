from sentence_transformers import SentenceTransformer


_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def get_location_embedding_text(location):
    return " ".join(
        part.strip()
        for part in [location.city, location.state, location.country]
        if part and part.strip()
    )


def get_location_embedding(location):
    text = get_location_embedding_text(location)
    return get_model().encode(text).tolist()


def get_query_embedding(query):
    return get_model().encode(query).tolist()
