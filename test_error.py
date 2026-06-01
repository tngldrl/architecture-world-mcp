from vertexai.generative_models import GenerationConfig

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"}
    }
}

try:
    from vertexai.generative_models._generative_models import GenerationConfig as GC
    config = GC(response_mime_type="application/json", response_schema=schema)
    print(config._raw_generation_config)
except Exception as e:
    import traceback
    traceback.print_exc()
