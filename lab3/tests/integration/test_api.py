from uuid import uuid4


def test_catalog_details(api):
    listing = api("GET", "/products")
    assert listing.status_code == 200
    product = next(x for x in listing.json() if x["title"] == "Linen Shirt")
    detail = api("GET", f"/products/{product['_id']}")
    assert detail.status_code == 200
    assert detail.json()["price"] == 35


def test_unknown_product(api):
    assert api("GET", "/products/000000000000000000000000").status_code == 404


def test_duplicate_registration(api, account):
    res = api("POST", "/users/register", json=account)
    assert res.status_code == 400
    assert res.json()["message"] == "Email already exists"


def test_wrong_password(api, account):
    res = api("POST", "/users/login", json={"email": account["email"], "password": uuid4().hex})
    assert res.status_code == 401
    assert "token" not in res.json()


def test_cart_requires_auth(api):
    assert api("GET", "/cart").status_code == 401


def test_cart_rejects_invalid_token(api):
    assert api("GET", "/cart", headers={"Authorization": "Bearer invalid"}).status_code == 401


def test_cart_update_and_remove(api, auth):
    headers = auth["headers"]
    product = next(x for x in api("GET", "/products").json() if x["title"] == "Wool Scarf")
    added = api("POST", "/cart/add", headers=headers, json={
        "userId": auth["user_id"], "productId": product["_id"], "images": product["images"],
        "title": product["title"], "price": product["price"], "quantity": 1, "size": "M"
    })
    assert added.status_code == 201, added.text
    item_id = added.json()["cartItem"]["_id"]
    updated = api("PUT", f"/cart/update/{item_id}", headers=headers, json={"quantity": 3})
    assert updated.status_code == 200
    assert updated.json()["cartItem"]["quantity"] == 3
    assert any(x["_id"] == item_id and x["quantity"] == 3 for x in api("GET", "/cart", headers=headers).json())
    assert api("DELETE", f"/cart/remove/{item_id}", headers=headers).status_code == 200
    assert all(x["_id"] != item_id for x in api("GET", "/cart", headers=headers).json())


def test_empty_order_rejected(api, auth):
    res = api("POST", "/orders/create", headers=auth["headers"], json={
        "products": [], "totalPrice": 0, "shippingAddress": "Oak 7, City, 10115"
    })
    assert res.status_code == 400
    assert res.json()["message"] == "must contain products"
