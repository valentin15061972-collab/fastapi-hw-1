from fastapi import FastAPI, HTTPException, Query
from app.schemas import AdCreate,  AdUpdate, AdResponse
from app.ads import create_ad, get_ad, update_ad, delete_ad, search_ads


app = FastAPI(title="Ads Service", version="1.0.0")


@app.post("/ad", response_model=AdResponse, summary="Create an ad")
async def create_ad_endpoint(ad: AdCreate):
    return await create_ad(ad)


@app.get("/ad/{ad_id}", response_model=AdResponse, summary="Get an ad")
async def get_ad_endpoint(ad_id: int):
    result = await get_ad(ad_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Ad not found")
    return result


@app.patch("/ad/{ad_id}", response_model=AdResponse, summary="Update an ad")
async def update_ad_endpoint(ad_id: int, ad_update: AdUpdate):
    result = await update_ad(ad_id, ad_update)
    if result is None:
        raise HTTPException(status_code=404, detail="Ad not found")
    return result


@app.delete("/ad/{ad_id}", status_code=204, summary="Delete an ad")
async def delete_ad_endpoint(ad_id: int):
    deleted = await delete_ad(ad_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Ad not found")


@app.get("/ad", response_model=list[AdResponse])
async def search_ads_endpoint(
    query: str | None = Query(None),
    title: str | None = Query(None),
    author: str | None = Query(None),
):
    return await search_ads(query=query, title=title, author=author)
