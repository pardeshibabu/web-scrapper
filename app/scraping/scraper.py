import scrapy
import logging
import re
import multiprocessing
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductItem(scrapy.Item):
    product_id = scrapy.Field(output_processor=TakeFirst())  # Extract product ID
    product_title = scrapy.Field(output_processor=TakeFirst())  # Now mapped to 'data-title'
    product_price = scrapy.Field(
        input_processor=MapCompose(lambda x: float(re.sub(r"[^\d.]", "", x)) if x and re.sub(r"[^\d.]", "", x) else 0.0),
        output_processor=TakeFirst(),
    )
    product_url = scrapy.Field(output_processor=TakeFirst())

class Scraper(scrapy.Spider):
    name = "scraper"

    def __init__(self, pages: int = 1, proxy: str = None, result_queue=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = pages
        self.proxy = proxy
        self.result_queue = result_queue

    def start_requests(self):
        for page in range(1, self.pages + 1):
            print(f"Pardeshi Scraping page {page}...")
            page_url = f"https://dentalstall.com/shop/page/{page}/"
            yield scrapy.Request(url=page_url, callback=self.parse, meta={"proxy": self.proxy})

    def parse(self, response):
        product_cards = response.xpath("//div[contains(@class, 'mf-product-details')]")
        logger.info(f"Found {len(product_cards)} product cards on this page.")

        scraped_data = []  # Initialize a list to hold scraped data

        for card in product_cards:
            loader = ItemLoader(item=ProductItem(), selector=card)
            loader.add_xpath("product_id", ".//a[contains(@class, 'add_to_cart_button')]/@data-product_id")  # Extract Product ID
            loader.add_xpath("product_title", ".//a[contains(@class, 'add_to_cart_button')]/@data-title | .//h2[contains(@class, 'woo-loop-product__title')]/a/text()")
            loader.add_xpath("product_url", ".//h2[contains(@class, 'woo-loop-product__title')]/a/@href")
            loader.add_xpath("product_price", ".//span[contains(@class, 'woocommerce-Price-amount')]/bdi/text()")
            product_item = loader.load_item()

            # Append the scraped product to the list
            scraped_data.append(product_item)

        # Send the scraped data back to the main process
        if self.result_queue:
            self.result_queue.put(scraped_data)

        next_page = response.xpath("//a[@class='next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse, meta={"proxy": self.proxy})

    def closed(self, reason):
        logger.info(f"Scraping finished: {reason}")

def configure_scrapy():
    """Configures Scrapy settings."""
    return get_project_settings()

def run(pages, proxy, result_queue):
    process = CrawlerProcess(get_project_settings())
    process.crawl(Scraper, pages=pages, proxy=proxy, result_queue=result_queue)
    process.start()  # Blocks until the scraping finishes

def run_scraper(pages=1, proxy=None):
    # Create a Queue for communication between the processes
    result_queue = multiprocessing.Queue()

    # Run the scraper in a separate process
    process = multiprocessing.Process(target=run, args=(pages, proxy, result_queue))
    process.start()
    process.join()  # Wait for the process to finish

    # Get the scraped data from the Queue
    scraped_data = result_queue.get()

    return scraped_data
