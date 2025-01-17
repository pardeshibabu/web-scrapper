# Web Scraper with Redis Caching and MongoDB Storage

## 📌 Project Overview
This project is a **web scraper** built using **Scrapy** that extracts product data from an e-commerce website. It includes a **MongoDB storage system** and implements **Redis caching** to avoid unnecessary database writes when the product price remains unchanged.

## 🚀 Features
- Scrapes product details such as **title, price, URL, and product ID**.
- Stores product data in **MongoDB**.
- Uses **Redis** to cache the last known price and update the database **only when the price changes**.
- Implements **multiprocessing** to handle scraping tasks efficiently.
- Supports **proxy configuration** for anonymous scraping.

---

## 🛠 Installation
### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/your-username/web-scraper.git
cd web-scraper
```

### 2️⃣ **Create a Virtual Environment (Optional but Recommended)**
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3️⃣ **Install Dependencies**
```sh
pip install -r requirements.txt
```

### 4️⃣ **Start Redis Server** (Make sure Redis is running)
```sh
redis-server
```

### 5️⃣ **Set Up MongoDB**
Ensure you have **MongoDB running** locally or use a cloud service like **MongoDB Atlas**.

Update the MongoDB connection details in `app/models/mongodb.py` if necessary.

---

## 🔥 Usage

### **Run the Scraper**
```sh
python run_scraper.py --pages 2 --proxy http://your-proxy-url
```
- `--pages`: Number of pages to scrape.
- `--proxy`: (Optional) Proxy URL to use.

### **Example Output**
```json
[
    {
        "product_id": "15653",
        "product_title": "Dental Kit",
        "product_price": 4395.00,
        "product_url": "https://example.com"
    },
    {
        "product_id": "17890",
        "product_title": "Toothpaste",
        "product_price": 1199.99,
        "product_url": "https://example.com"
    }
]
```

---

## 🏛 Project Structure
```plaintext
web-scraper/
│── app/
│   ├── storage/
│   │   ├── base.py             # Abstract class for storage
│   │   ├── mongodb_storage.py  # MongoDB storage with Redis caching
│   ├── models/
│   │   ├── mongodb.py          # MongoDB connection setup
│── scraper.py                  # Scrapy spider implementation
│── run_scraper.py              # Entry point for running scraper
│── requirements.txt            # Required dependencies
│── README.md                   # Project documentation
```

---

## 🛠 Technology Stack
- **Python** (Scrapy, multiprocessing)
- **MongoDB** (Data storage)
- **Redis** (Caching)
- **Docker** (Optional: for deployment)

---

## 🐳 Running with Docker (Optional)
```sh
docker-compose up --build
```

---

## ✨ Contributing
Feel free to fork and contribute by submitting a PR!

---

## 📜 License
This project is licensed under the **MIT License**.

