import random
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

# IMPORTANT: Adjust these imports to match your actual app names
# If your Store model is in an app called 'stores', use: from stores.models import Store, Inventory
from stores.models import Store, Inventory 
from products.models import Product, Category

class Command(BaseCommand):
    help = "Seeds the database with Categories, Products, Stores, and Inventory"

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # We wrap everything in a transaction so if it fails, the DB stays clean
        with transaction.atomic():
            self.stdout.write(self.style.WARNING("Deleting old data..."))
            Inventory.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            Store.objects.all().delete()

            # 1. Create 12 Categories
            self.stdout.write("Creating categories...")
            cat_names = [
                "Electronics", "Home & Kitchen", "Books", "Fashion", 
                "Sports", "Beauty", "Automotive", "Toys", "Health", 
                "Grocery", "Garden", "Office Supplies"
            ]
            categories = [Category.objects.create(name=name) for name in cat_names]

            # 2. Create 1000 Products
            self.stdout.write("Creating 1000 products...")
            product_list = []
            for _ in range(1000):
                product_list.append(Product(
                    title=fake.catch_phrase(),
                    description=fake.paragraph(nb_sentences=3),
                    price=round(random.uniform(10.0, 1000.0), 2),
                    category=random.choice(categories)
                ))
            # Use bulk_create for speed
            Product.objects.bulk_create(product_list)
            all_products = list(Product.objects.all())

            # 3. Create 20 Stores
            self.stdout.write("Creating 20 stores...")
            store_list = []
            for _ in range(20):
                store_list.append(Store(
                    name=fake.company() + " " + random.choice(["Hub", "Outlet", "Store", "Mart"]),
                    location=fake.city()
                ))
            Store.objects.bulk_create(store_list)
            all_stores = list(Store.objects.all())

            # 4. Create Inventory (300+ items per store)
            self.stdout.write("Populating inventory (this may take a moment)...")
            inventory_to_create = []
            
            for store in all_stores:
                # Get 300 unique products to avoid UniqueConstraint errors
                sampled_products = random.sample(all_products, 300)
                for product in sampled_products:
                    inventory_to_create.append(Inventory(
                        store=store,
                        product=product,
                        quantity=random.randint(0, 100)
                    ))
            
            # Create in batches of 1000 to be safe with memory
            Inventory.objects.bulk_create(inventory_to_create, batch_size=1000)

        self.stdout.write(self.style.SUCCESS('Successfully seeded all data!'))