from datetime import datetime, timezone
from app.schemas import AdCreate, AdUpdate, AdResponse

ads_store: dict[int, dict] = {}
_next_id: int = 1


def _to_response(ad: dict) -> AdResponse:
    return AdResponse(**ad)


async def create_ad(ad: AdCreate) -> AdResponse:
    global _next_id
    stored = {
        "id": _next_id,
        "title": ad.title,
        "description": ad.description,
        "price": ad.price,
        "author": ad.author,
        "creation_date": datetime.now(timezone.utc),
    }
    ads_store[_next_id] = stored
    _next_id += 1
    return _to_response(stored)


async def get_ad(ad_id: int) -> AdResponse | None:
    ad = ads_store.get(ad_id)
    if ad is None:
        return None
    return _to_response(ad)


async def update_ad(ad_id: int, ad_update: AdUpdate) -> AdResponse | None:
    ad = ads_store.get(ad_id)
    if ad is None:
        return None
    update_data = ad_update.model_dump(exclude_none=True)
    ad.update(update_data)
    return _to_response(ad)


async def delete_ad(ad_id: int) -> bool:
    return ads_store.pop(ad_id, None) is not None


async def search_ads(
    query: str | None = None,
    title: str | None = None,
    author: str | None = None,
) -> list[AdResponse]:
    results = []
    for ad in ads_store.values():
        match = True
        if query is not None:
            q = query.lower()
            if q not in ad["title"].lower() and q not in ad["description"].lower():
                match = False
        if title is not None and title.lower() not in ad["title"].lower():
            match = False
        if author is not None and author.lower() not in ad["author"].lower():
            match = False
        if match:
            results.append(_to_response(ad))
    return results


