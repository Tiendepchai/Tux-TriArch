import os, datetime, httpx
from dotenv import load_dotenv; load_dotenv()
ORION_BASE=os.getenv("ORION_BASE","http://orion:1026"); ORION_ENTITIES=os.getenv("ORION_ENTITIES","/ngsi-ld/v1/entities")
ENTITIES_URL=f"{ORION_BASE.rstrip('/')}{ORION_ENTITIES}"
HEADERS_JSONLD={"Accept":"application/ld+json","Content-Type":"application/ld+json"}
def now_iso(): return datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
async def post_or_patch(entity):
    async with httpx.AsyncClient(timeout=30.0) as client:
        r=await client.post(ENTITIES_URL, headers=HEADERS_JSONLD, json=entity)
        if r.status_code in (201,204): return r
        if r.status_code==409:
            eid=entity["id"]; attrs={k:v for k,v in entity.items() if k not in ("id","type","@context")}
            url=f"{ENTITIES_URL}/{eid}/attrs"; return await client.patch(url, headers=HEADERS_JSONLD, json=attrs)
        r.raise_for_status(); return r
def context_core(): return ["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"]
