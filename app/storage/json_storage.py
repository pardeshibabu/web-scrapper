from app.storage.base import StorageBase
from app.models.json_storage import JSONModel

class JSONStorage(StorageBase):
    def save_products(self, products: list):
        try:
            data = JSONModel.read()
            data.extend(products)
            JSONModel.write(data)
            return len(products)
        except Exception as e:
            print(f"Error saving to JSON: {e}")
            return 0

    def get_all_products(self):
        try:
            return JSONModel.read()
        except Exception as e:
            print(f"Error reading JSON: {e}")
            return []
