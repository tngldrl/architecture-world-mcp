from vertexai.generative_models import GenerationConfig

vertex_schema = {
    "type": "object",
    "properties": {
        "microservices": {
            "type": "array"
        }
    }
}

try:
    GenerationConfig(response_mime_type="application/json", response_schema=vertex_schema)
    print("Success")
except Exception as e:
    import traceback
    traceback.print_exc()
