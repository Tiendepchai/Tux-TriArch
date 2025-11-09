import os
from dotenv import load_dotenv
load_dotenv()
ORION_BASE = os.getenv("ORION_BASE","http://orion:1026")
ORION_ENTITIES = os.getenv("ORION_ENTITIES","/ngsi-ld/v1/entities")
CORS_ORIGINS = os.getenv("CORS_ORIGINS","*").split(",")
