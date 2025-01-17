import redis
import logging
from fastapi import FastAPI, Depends, Header, HTTPException
from app.auth import validate_token
from app.scraping.scraper import run_scraper
from app.storage.backend import get_storage_backend

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Redis setup
redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

app = FastAPI()

def get_storage():
    """ Dependency injection for storage backend """
    return get_storage_backend("mongodb")  # Change to "json" if needed

@app.post("/scrape")
def scrape(pages: int = 1, proxy: str = None, x_token: str = Header(...), storage=Depends(get_storage),):
    """ API Endpoint to trigger Scraping """
    try:
        validate_token(x_token)
    except ValueError as e:
        logger.error(f"Unauthorized access attempt: {str(e)}")
        raise HTTPException(status_code=401, detail=str(e))

    logger.info(f"Starting scraper for {pages} pages with proxy {proxy}")

    scraped_data = run_scraper(pages=pages, proxy=proxy)
    
    if not scraped_data:
        logger.warning("No data was scraped.")
        return {"message": "Scraping completed. No products were found."}

    inserted_count = storage.save_products(scraped_data, redis_client)
    logger.info(f"Scraping completed. {inserted_count} products saved.")

    return {"message": f"Scraping completed. {inserted_count} products saved."}

@app.get("/products")
def get_products(storage=Depends(get_storage)):
    """ Fetch all scraped products """
    products = storage.get_all_products()
    if not products:
        logger.info("No products found in the storage.")
    return products
