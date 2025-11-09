# Smart City NGSI-LD Starter

Runnable starter: Orion-LD + MongoDB + FastAPI + Leaflet + Ingestors (OpenAQ, Overpass, OpenWeather).

## Quick Start
1) `cp .env.example .env`
2) `docker compose -f infra/docker-compose.yml up -d --build`
3) (optional) `bash scripts/seed_sample_entities.sh`
4) Run ingestors:
   - `docker compose exec api bash -lc "python -m ingestors.openaq_ingestor --interval 600"`
   - `docker compose exec api bash -lc "python -m ingestors.overpass_ingestor --interval 3600"`
   - `docker compose exec api bash -lc "python -m ingestors.openweather_ingestor --interval 900"`
5) Open: Frontend http://localhost:8080  |  API http://localhost:8000

## Notes
- Entities: AirQualityObserved, PointOfInterest, WeatherObserved.
- Aligns with SOSA/SSN + Smart Data Models via JSON-LD contexts.
