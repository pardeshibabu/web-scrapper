from app.storage.json_storage import JSONStorage
from app.storage.mongodb import MongoDBStorage



def get_storage_backend(backend_type: str):
    if backend_type == "mongodb":
        return MongoDBStorage()
    elif backend_type == "json":
        return JSONStorage()
    raise ValueError("Unsupported storage backend")
