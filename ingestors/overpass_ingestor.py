import os, asyncio, httpx
from .common import now_iso, post_or_patch, context_core
from dotenv import load_dotenv; load_dotenv()
BBOX=os.getenv("BBOX","21.05,105.75,20.95,105.90"); TIMEOUT=int(os.getenv("OVERPASS_TIMEOUT","30"))
CATEGORIES={"parking":'node["amenity"="parking"]({bbox});',"park":'node["leisure"="park"]({bbox});',"bus_stop":'node["highway"="bus_stop"]({bbox});'}
CONTEXT=context_core()+["https://raw.githubusercontent.com/smart-data-models/dataModel.PointOfInterest/master/context.jsonld"]
def build_query(bbox): return "[out:json][timeout:{timeout}];(".format(timeout=TIMEOUT)+"".join([CATEGORIES[k].format(bbox=bbox) for k in CATEGORIES])+");out center;"
async def fetch_overpass(bbox):
    url="https://overpass-api.de/api/interpreter"; data=build_query(bbox)
    async with httpx.AsyncClient(timeout=60.0) as client: r=await client.post(url, data={"data":data}); r.raise_for_status(); return r.json()
def to_entities(js):
    ents=[]
    for el in js.get("elements",[]):
        lat=el.get("lat"); lon=el.get("lon"); tags=el.get("tags",{})
        if lat is None or lon is None: continue
        name=tags.get("name") or "POI"; category=None
        if tags.get("amenity")=="parking": category="parking"
        if tags.get("leisure")=="park": category="park"
        if tags.get("highway")=="bus_stop": category="bus_stop"
        if not category: continue
        eid=f"urn:ngsi-ld:PointOfInterest:{category}:{el.get('id')}"
        ents.append({"id":eid,"type":"PointOfInterest","name":{"type":"Property","value":name},"category":{"type":"Property","value":category},
                     "location":{"type":"GeoProperty","value":{"type":"Point","coordinates":[lon,lat]}},"dateObserved":{"type":"Property","value":now_iso()},"@context":CONTEXT})
    return ents
async def run_once():
    js=await fetch_overpass(BBOX); ents=to_entities(js)
    for e in ents: await post_or_patch(e)
    return len(ents)
async def main(interval=None):
    if interval is None: print(f"Overpass upserted: {await run_once()}"); return
    while True:
        try: print(f"[Overpass] upserted {await run_once()}") 
        except Exception as ex: print("[Overpass] error:", ex)
        await asyncio.sleep(interval)
if __name__=="__main__":
    import argparse; ap=argparse.ArgumentParser(); ap.add_argument("--interval",type=int,default=None); args=ap.parse_args(); asyncio.run(main(args.interval))
