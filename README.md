
````bash
#  Project - Django Orders API

This project is a **Django-based API** for managing orders, products, and stores, with **Celery integration** for asynchronous tasks and **Docker support** for containerization.  

---

## **Features Implemented**

1. ** Orders**
   - Create orders with multiple products.
   - Track inventory per store.
   - Confirm or reject orders based on stock availability.

2. **Django Models**
   - `Product`, `Category`, `Store`, `Inventory`, `Order`, `OrderItem`.
   - Proper relationships using `ForeignKey` and `related_name`.

3. **Django REST Framework**
   - API endpoints for creating and retrieving orders.
   - Serializers for nested data:
     - `OrderSerializer` includes `OrderItemSerializer` with product details.
   - Public endpoint for order creation (no authentication needed).

4. **Celery Integration**
   - Asynchronous background tasks using Celery.
   - Redis used as the message broker.
   - Task implemented: `send_order_confirmation` (simulates sending order confirmation emails).
   - Configured retry logic with:
     ```python
     @shared_task(bind=True, max_retries=3, default_retry_delay=60)
     ```
   - Triggered after order creation using:
     ```python
     send_order_confirmation.delay(order.id)
     ```

5. **Database**
   - SQLite for local/demo purposes.
   - PostgreSQL optional for production.

6. **Docker & Containerization**
   - Dockerfile for Django API.
   - docker-compose.yml to run:
     - Django web server
     - Celery worker
     - Redis broker
     - PostgreSQL (optional)
   - Local development and demo-ready setup.

7. **Seed Data**
   - Added `python manage.py seed_data` command to populate demo data for stores, products, and inventory.

8. **Email / Notifications**
   - Simulated order confirmation emails using `send_mail`.
   - Configurable `EMAIL_RECEIVER` in settings.

9. **Performance Optimization**
   - Use of `select_for_update` for inventory locking during order creation.
   - Bulk creation of `OrderItem` objects.
   - Celery offloads slow tasks from API requests.

---

## **Project Structure**

````

FIS_Project/
├─ orders/
│  ├─ models.py
│  ├─ views.py
│  ├─ serializers.py
│  ├─ tasks.py
├─ products/
│  ├─ models.py
├─ stores/
│  ├─ models.py
├─ project/
│  ├─ settings.py
│  ├─ wsgi.py
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
└─ manage.py

````

---

## **Setup & Running the Project**

### **1. Clone the repository**

```bash
git clone https://github.com/yourusername/fis-project.git
cd fis-project
````

### **2. Create `.env` for sensitive info**

```env
REDIS_URL=redis://default:your_redis_password@your_redis_host:port
EMAIL_RECEIVER=demo@example.com
EMAIL_PASSWORD=app_password
EMAIL_HOST=email_host
```

---

### **3. Build and run with Docker**

```bash
docker-compose build
docker-compose up
```

* Django API: [http://localhost:8000](http://localhost:8000)
* Celery worker logs will show background task executions.

---

### **4. Seed Data**

Run the custom management command to populate demo data:

```bash
python manage.py seed_data
```

* This creates sample stores, products, inventory, and categories for testing.

---

## **API Endpoints**

### **1. Create Order**

* **URL:** `/orders/`
* **Method:** POST
* **Description:** Create a new order for a store.
* **Request Body Example:**

```json
{
  "store_id": 1,
  "items": [
    {"product_id": 1, "quantity_requested": 2},
    {"product_id": 2, "quantity_requested": 1}
  ]
}
```

* **Response Example:**

```json
{
  "id": 1,
  "store": 1,
  "status": "CONFIRMED",
  "items": [
    {"product": {"id":1,"title":"Product A"},"quantity_requested":2},
    {"product": {"id":2,"title":"Product B"},"quantity_requested":1}
  ]
}
```

---

### **2. List Orders for a Store**

* **URL:** `/stores/<store_id>/orders/`
* **Method:** GET
* **Description:** Retrieve all orders for a specific store.
* **Response Example:**

```json
[
  {
    "id": 1,
    "store": 1,
    "status": "CONFIRMED",
    "items": [
      {"product": {"id":1,"title":"Product A"},"quantity_requested":2}
    ]
  }
]
```

---

### **3. Store Inventory**

* **URL:** `/stores/<store_id>/inventory/`
* **Method:** GET
* **Description:** Retrieve all products and their quantities for a specific store.
* **Response Example:**

```json
[
  {
    "product": {"id":1,"title":"Product A"},
    "quantity": 10
  },
  {
    "product": {"id":2,"title":"Product B"},
    "quantity": 5
  }
]
```

---

### **4. Product Search**

* **URL:** `/api/search/products/`
* **Method:** GET
* **Query Parameters:** `?q=<search_term>`
* **Description:** Search products by name or description.
* **Response Example:**

```json
[
  {"id":1,"title":"Product A","description":"Example product","price":"100.00"},
  {"id":2,"title":"Product B","description":"Another product","price":"50.00"}
]
```

---

### **5. Product Suggestions**

* **URL:** `/api/search/suggest/`
* **Method:** GET
* **Query Parameters:** `?q=<partial_term>`
* **Description:** Get suggested products based on partial search input.
* **Response Example:**

```json
[
  {"id":1,"title":"Product A"},
  {"id":2,"title":"Product B"}
]
```

---

## **5. Celery**

Start Celery worker (if not using Docker):

```bash
celery -A Celery_pro worker -l info
```

* Tasks run asynchronously and retry up to 3 times in case of failure.
* Example task: `send_order_confirmation` triggered after order creation.

---

## **6. Notes**

* CSRF exempted for public order endpoint.
* SQLite used for demo; PostgreSQL recommended for production.
* Docker ensures all services (web, worker, Redis) are containerized for easy deployment.
* Redis can be local or online (RedisLabs) for demo purposes.

---

## **7. Next Steps / Improvements**

* Add authentication for users.
* Add Celery Beat for scheduled tasks (e.g., daily inventory reports).
* Move sensitive info to `.env` using `django-environ`.
* Replace `print` statements in Celery task with real email notifications.
* Add more comprehensive API tests.

---

**Author:** Hussein Lawal
**Date:** February 2026

```
