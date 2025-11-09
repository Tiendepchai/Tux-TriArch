import os, asyncio, httpx
from .common import now_iso, post_or_patch, context_core
from dotenv import load_dotenv; load_dotenv()
CITY=os.getenv("CITY","Hanoi"); COUNTRY=os.getenv("COUNTRY","VN"); PARAMS=os.getenv("OPENAQ_PARAMETERS","pm25,pm10").split(",")
CONTEXT=context_core()+["https://raw.githubusercontent.com/smart-data-models/dataModel.Environment/master/context.jsonld"]
async def fetch_openaq(city,country,parameters):
    url="https://api.openaq.org/v2/latest"; params={"city":city,"country":country,"parameter":parameters}
    async with httpx.AsyncClient(timeout=30.0) as client: r=await client.get(url, params=params); r.raise_for_status(); return r.json()
def to_entity(result):
    coords=result.get("coordinates") or {}; lat=coords.get("latitude"); lon=coords.get("longitude")
    if lat is None or lon is None: return None
    measurements={m["parameter"]:m["value"] for m in result.get("measurements",[])}
    pm25=measurements.get("pm25"); pm10=measurements.get("pm10"); aqi=int(min(500, pm25*3)) if pm25 is not None else None
    e={"id":f"urn:ngsi-ld:AirQualityObserved:{result.get('location','unknown')}",
       "type":"AirQualityObserved",
       "dateObserved":{"type":"Property","value":now_iso()},
       "location":{"type":"GeoProperty","value":{"type":"Point","coordinates":[lon,lat]}},
       "@context":CONTEXT}
    if pm25 is not None: e["pm25"]={"type":"Property","value":pm25,"unitCode":"UGM3"}
    if pm10 is not None: e["pm10"]={"type":"Property","value":pm10,"unitCode":"UGM3"}
    if aqi is not None: e["aqi"]={"type":"Property","value":aqi}
    return e
async def run_once():
    data=await fetch_openaq(CITY,COUNTRY,PARAMS); ents=[]
    for res in data.get("results",[]): 
        e=to_entity(res); 
        if e: ents.append(e)
    for e in ents: await post_or_patch(e)
    return len(ents)
async def main(interval=None):
    import time
    if interval is None: print(f"OpenAQ upserted: {await run_once()}"); return
    while True:
        try: print(f"[OpenAQ] upserted {await run_once()}") 
        except Exception as ex: print("[OpenAQ] error:", ex)
        await asyncio.sleep(interval)
if __name__=="__main__":
    import argparse; ap=argparse.ArgumentParser(); ap.add_argument("--interval",type=int,default=None); args=ap.parse_args(); asyncio.run(main(args.interval))
