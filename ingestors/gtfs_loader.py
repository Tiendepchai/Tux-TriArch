import csv, asyncio
from .common import post_or_patch, context_core
CONTEXT=context_core()+["https://raw.githubusercontent.com/smart-data-models/dataModel.PointOfInterest/master/context.jsonld"]
def stops_to_entities(stops_csv):
    ents=[]
    with open(stops_csv, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sid=row.get("stop_id"); name=row.get("stop_name"); lat=float(row.get("stop_lat")); lon=float(row.get("stop_lon"))
            ents.append({"id":f"urn:ngsi-ld:PointOfInterest:bus_stop:{sid}","type":"PointOfInterest","name":{"type":"Property","value":name},
                         "category":{"type":"Property","value":"bus_stop"},"location":{"type":"GeoProperty","value":{"type":"Point","coordinates":[lon,lat]}},"@context":CONTEXT})
    return ents
async def main(stops_path):
    ents=stops_to_entities(stops_path)
    for e in ents: await post_or_patch(e)
    print(f"Loaded {len(ents)} GTFS stops")
if __name__=="__main__":
    import argparse; ap=argparse.ArgumentParser(); ap.add_argument("--stops", required=True); args=ap.parse_args(); asyncio.run(main(args.stops))
