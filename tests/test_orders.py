def test_create_order_confirmed(api_client, store, product, inventory):
    payload = {
        "store_id": store.id,
        "items": [
            {"product_id": product.id, "quantity_requested": 2}
        ]
    }

    response = api_client.post("/orders/", payload, format="json")

    assert response.status_code == 201
    assert response.data["status"] == "CONFIRMED"

    inventory.refresh_from_db()
    assert inventory.quantity == 8  # assuming initial was 10
