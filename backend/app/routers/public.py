from fastapi import APIRouter
from ..ngsi_client import get_entities
router = APIRouter(prefix="/api", tags=["public"])
@router.get("/health")
async def health(): return {"ok": True}
@router.get("/aqi")
async def aqi(limit: int = 100):
    data = await get_entities("AirQualityObserved", limit=limit); out=[]
    for e in data:
        loc=e.get("location",{}).get("value",{}); coords=loc.get("coordinates")
        aqi=(e.get("aqi") or {}).get("value"); pm25=(e.get("pm25") or {}).get("value"); pm10=(e.get("pm10") or {}).get("value")
        dt=(e.get("dateObserved") or {}).get("value")
        if isinstance(coords,list): out.append({"id":e.get("id"),"coords":coords,"aqi":aqi,"pm25":pm25,"pm10":pm10,"dateObserved":dt})
    return out
@router.get("/poi")
async def poi(limit: int = 200, category: str | None = None):
    data = await get_entities("PointOfInterest", limit=limit); out=[]
    for e in data:
        loc=e.get("location",{}).get("value",{}); coords=loc.get("coordinates")
        cat=(e.get("category") or {}).get("value"); name=(e.get("name") or {}).get("value")
        if category and cat!=category: continue
        if isinstance(coords,list): out.append({"id":e.get("id"),"name":name,"category":cat,"coords":coords})
    return out
@router.get("/weather")
async def weather(limit: int = 50):
    data = await get_entities("WeatherObserved", limit=limit); out=[]
    for e in data:
        loc=e.get("location",{}).get("value",{}); coords=loc.get("coordinates")
        temp=(e.get("temperature") or {}).get("value"); hum=(e.get("relativeHumidity") or {}).get("value")
        dt=(e.get("dateObserved") or {}).get("value")
        if isinstance(coords,list): out.append({"id":e.get("id"),"coords":coords,"temperature":temp,"humidity":hum,"dateObserved":dt})
    return out
