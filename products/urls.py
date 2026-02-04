
from  django.urls import path
from . import views

urlpatterns = [
  path("api/search/products/", views.product_search),
    path("api/search/suggest/", views.product_suggest),
    ]

 
