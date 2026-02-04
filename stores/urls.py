
from  django.urls import path
from . import views

urlpatterns = [
        path('stores/<int:store_id>/orders/',views.list_store_orders, name="list_orders"),
        path('stores/<int:store_id>/inventory/',views.store_inventory, name="store_inventory")
        
    ]

    