from vertexai.generative_models import GenerativeModel, Type

schema = {
    "type": Type.OBJECT,
    "properties": {
        "name": {"type": Type.STRING}
    }
}
print(schema)
