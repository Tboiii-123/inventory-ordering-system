from django.db.models import Q
from products.models import Product



def product_search_queryset(params):
    """
    Builds and returns a filtered Product queryset
    based on query params.
    """

    qs = Product.objects.select_related("category")

    # --------------------
    # Keyword search
    # --------------------
    keyword = params.get("q")
    if keyword:
        qs = qs.filter(
            Q(title__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(category__name__icontains=keyword)
        )

    # --------------------
    # Filters
    # --------------------
    category = params.get("category")
    if category:
        qs = qs.filter(category__name__iexact=category)

    min_price = params.get("min_price")
    if min_price:
        qs = qs.filter(price__gte=min_price)

    max_price = params.get("max_price")
    if max_price:
        qs = qs.filter(price__lte=max_price)

    store_id = params.get("store_id")
    in_stock = params.get("in_stock")

    if store_id:
        qs = qs.filter(inventory__store_id=store_id)

        if in_stock == "true":
            qs = qs.filter(inventory__quantity__gt=0)

    # --------------------
    # Sorting
    # --------------------
    sort = params.get("sort")

    if sort == "price":
        qs = qs.order_by("price")
    elif sort == "newest":
        qs = qs.order_by("-id")
    elif sort == "relevance" and keyword:
        qs = qs.order_by("-id")  # simple relevance fallback

    return qs.distinct()



def product_autocomplete(query):
    """
    Returns up to 10 product titles.
    Prefix matches come first.
    """

    if not query or len(query) < 3:
        return []

    # Prefix matches (higher priority)
    prefix_qs = Product.objects.filter(title__istartswith=query).values_list("title", flat=True)[:10]

    remaining_slots = 10 - len(prefix_qs)

    if remaining_slots <= 0:
        return list(prefix_qs)

    # General matches (exclude prefix ones)
    general_qs = Product.objects.filter(title__icontains=query).exclude(title__istartswith=query).values_list("title", flat=True)[:remaining_slots]
    

    return list(prefix_qs) + list(general_qs)



