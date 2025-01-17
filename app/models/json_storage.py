import json

class JSONModel:
    FILE_PATH = "products.json"
    
    @staticmethod
    def read():
        try:
            with open(JSONModel.FILE_PATH, "r") as file:
                content = file.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Error decoding JSON, file might be corrupted.")
            return []
        except Exception as e:
            print(f"Error reading from JSON: {e}")
            return []

    @staticmethod
    def write(data):
        try:
            if not isinstance(data, list):
                raise ValueError("Data should be a list of dictionaries")

            # Ensure that all items are dictionaries and handle invalid items
            processed_data = []
            for item in data:
                if isinstance(item, dict):
                    processed_data.append(item)
                elif hasattr(item, "_asdict"):  # For namedtuples
                    processed_data.append(item._asdict())
                elif hasattr(item, "items"):  # For Scrapy Item objects
                    processed_data.append(dict(item))  # Convert Scrapy Item to a dict
                else:
                    print(f"Warning: Skipping invalid item: {item} ({type(item)})")

            # Save to JSON file only if processed_data is not empty
            if processed_data:
                with open(JSONModel.FILE_PATH, "w") as file:
                    json.dump(processed_data, file, indent=4)
            else:
                print("Warning: No valid items to save.")
                
        except Exception as e:
            print(f"Error saving to JSON: {e}")

