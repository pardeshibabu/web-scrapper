from app.storage.base import StorageBase
from app.models.mongodb import MongoDBModel

class MongoDBStorage(StorageBase):
    def __init__(self):
        self.db_model = MongoDBModel()
        self.collection = self.db_model.get_collection("products")

    def save_products(self, products: list,redis_client):
        updated_count = 0

        for product in products:
            product_id = product.get("product_id", "No ID")
            product_price = product.get("product_price", 0.0)

            # Get last stored price from Redis
            cached_price = redis_client.get(f"product_price:{product_id}")

            if cached_price is None or float(cached_price) != product_price:
                # Price has changed or product is new → Update MongoDB
                self.collection.update_one(
                    {"product_id": product_id},
                    {"$set": product},
                    upsert=True
                )
                # Update Redis cache
                redis_client.set(f"product_price:{product_id}", product_price)
                updated_count += 1
            else:
                print(f"Skipping update for product_id {product_id}, price unchanged.")

        return updated_count

    def get_all_products(self):
        return list(self.collection.find({}, {"_id": 0}))
