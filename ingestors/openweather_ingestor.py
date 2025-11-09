import os, asyncio, httpx
from .common import now_iso, post_or_patch, context_core
from dotenv import load_dotenv; load_dotenv()
CITY_NAME=os.getenv("OWM_CITY_NAME","Hanoi,VN"); OWM_KEY=os.getenv("OWM_API_KEY")
CONTEXT=context_core()+["https://raw.githubusercontent.com/smart-data-models/dataModel.Weather/master/context.jsonld"]
async def fetch_weather(city_name):
    if not OWM_KEY: raise RuntimeError("Missing OWM_API_KEY")
    url="https://api.openweathermap.org/data/2.5/weather"; params={"q":city_name,"appid":OWM_KEY,"units":"metric"}
    async with httpx.AsyncClient(timeout=30.0) as client: r=await client.get(url, params=params); r.raise_for_status(); return r.json()
def to_entity(js):
    coord=js.get("coord",{}); lat,lon=coord.get("lat"),coord.get("lon"); main=js.get("main",{}); temp=main.get("temp"); hum=main.get("humidity"); name=js.get("name","city")
    e={"id":f"urn:ngsi-ld:WeatherObserved:{name}","type":"WeatherObserved","dateObserved":{"type":"Property","value":now_iso()},
       "location":{"type":"GeoProperty","value":{"type":"Point","coordinates":[lon,lat]}},"@context":CONTEXT}
    if temp is not None: e["temperature"]={"type":"Property","value":float(temp),"unitCode":"CEL"}
    if hum is not None: e["relativeHumidity"]={"type":"Property","value":float(hum)}
    return e
async def run_once(): e=to_entity(await fetch_weather(CITY_NAME)); await post_or_patch(e); return 1
async def main(interval=None):
    if interval is None: print(f"OpenWeather upserted: {await run_once()}"); return
    while True:
        try: print(f"[OpenWeather] upserted {await run_once()}") 
        except Exception as ex: print("[OpenWeather] error:", ex)
        await asyncio.sleep(interval)
if __name__=="__main__":
    import argparse; ap=argparse.ArgumentParser(); ap.add_argument("--interval",type=int,default=None); args=ap.parse_args(); asyncio.run(main(args.interval))
