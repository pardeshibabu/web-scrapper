from abc import ABC, abstractmethod
from app.models.mongodb import MongoDBModel

class StorageBase(ABC):
    @abstractmethod
    def save_products(self, products: list, redis_client):
        pass

    @abstractmethod
    def get_all_products(self):
        pass
