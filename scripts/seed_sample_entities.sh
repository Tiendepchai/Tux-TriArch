#!/usr/bin/env bash
set -euo pipefail
ORION=${ORION:-"http://localhost:1026"}
URL="$ORION/ngsi-ld/v1/entities"
curl -sS -X POST "$URL" -H 'Content-Type: application/ld+json' -d '{
  "id":"urn:ngsi-ld:PointOfInterest:park:demo",
  "type":"PointOfInterest",
  "name":{"type":"Property","value":"Công viên Demo"},
  "category":{"type":"Property","value":"park"},
  "location":{"type":"GeoProperty","value":{"type":"Point","coordinates":[105.85,21.03]}},
  "@context":["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
              "https://raw.githubusercontent.com/smart-data-models/dataModel.PointOfInterest/master/context.jsonld"]
}' || true
echo "Seeded sample POI"
