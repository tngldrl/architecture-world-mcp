from pydantic import BaseModel, Field
from typing import List
import json

class Dependency(BaseModel):
    service_name: str
    description: str

class Microservice(BaseModel):
    name: str
    dependencies: List[Dependency]

class ArchitectureExtraction(BaseModel):
    microservices: List[Microservice]

print(json.dumps(ArchitectureExtraction.model_json_schema(), indent=2))
