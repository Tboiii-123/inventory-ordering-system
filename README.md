
````markdown
#  Project

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

7. **Email / Notifications**
   - Simulated order confirmation emails using `send_mail`.
   - Configurable `EMAIL_RECEIVER` in settings.

8. **Performance Optimization**
   - Use of `select_for_update` for inventory locking during order creation.
   - Bulk creation of `OrderItem` objects.
   - Celery offloads slow tasks from API requests.

---

## **Project Structure**

````
Project/
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
REDIS_URL=redis_url
EMAIL_RECEIVER=demo@example.com
EMAIL_PASSWORD=app_password
EMAIL_HOST=email_host
```

> **Note:** Do not commit `.env` to GitHub.

---

### **3. Build and run with Docker**

```bash
docker-compose build
docker-compose up
```

* Django API: [http://localhost:8000](http://localhost:8000)
* Celery worker logs will show background task executions.

---

### **4. API Usage**

**Create Order** (POST `/order/orders/`):

```json
{
  "store_id": 1,
  "items": [
    {"product_id": 1, "quantity_requested": 2},
    {"product_id": 2, "quantity_requested": 1}
  ]
}
```

* API responds with order details including:

  * Status (`CONFIRMED` or `REJECTED`)
  * Ordered items
  * Total quantity

**Celery Task:** After order creation, Celery runs `send_order_confirmation` asynchronously.

---

### **5. Celery**

Start Celery worker (if not using Docker):

```bash
celery -A Celery_pro worker -l info
```

* Tasks run asynchronously and retry up to 3 times in case of failure.

---

### **6. Notes**

* CSRF exempted for public order endpoint.
* SQLite used for demo; PostgreSQL recommended for production.
* Docker ensures all services (web, worker, Redis) are containerized for easy deployment.
* Redis can be local or online (RedisLabs) for demo purposes.

---

### **7. Next Steps / Improvements**

* Add authentication for users.
* Add Celery Beat for scheduled tasks (e.g., daily inventory reports).
* Move sensitive settings to `.env` using `django-environ`.
* Replace `print` statements in Celery task with real email notifications.

---

**Author:** Hussein Lawal
**Date:** February 2026

```




