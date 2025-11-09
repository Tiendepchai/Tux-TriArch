import httpx
from .config import ORION_BASE, ORION_ENTITIES
HEADERS_JSONLD = {"Accept":"application/ld+json","Content-Type":"application/ld+json"}
def entities_url(): return f"{ORION_BASE.rstrip('/')}{ORION_ENTITIES}"
async def get_entities(entity_type: str, limit: int = 100):
    params = {"type": entity_type, "limit": str(limit)}
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.get(entities_url(), params=params, headers={"Accept":"application/ld+json"})
        r.raise_for_status(); return r.json()
async def post_entity(entity: dict):
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.post(entities_url(), headers=HEADERS_JSONLD, json=entity)
        if r.status_code in (201,204): return r
        if r.status_code == 409:
            eid = entity.get("id"); url = f"{entities_url()}/{eid}/attrs"
            attrs = {k:v for k,v in entity.items() if k not in ("id","type","@context")}
            return await client.patch(url, headers=HEADERS_JSONLD, json=attrs)
        r.raise_for_status(); return r
