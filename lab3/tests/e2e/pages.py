import re

from playwright.sync_api import expect


class AuthPage:
    def __init__(self, page):
        self.page = page

    def register(self, account):
        self.page.goto("/signup")
        self.page.get_by_placeholder("Name", exact=True).fill(account["fullName"])
        self.page.get_by_placeholder("Email", exact=True).fill(account["email"])
        self.page.get_by_placeholder("Password", exact=True).fill(account["password"])
        self.page.get_by_role("button", name="Sign Up", exact=True).click()
        expect(self.page).to_have_url(re.compile(r"/login$"), timeout=15000)

    def login(self, account):
        self.page.goto("/login")
        self.page.locator('input[type="email"]').fill(account["email"])
        self.page.locator('input[type="password"]').fill(account["password"])
        self.page.get_by_role("button", name="Login", exact=True).click()
        expect(self.page).to_have_url(re.compile(r"^https?://[^/]+/$"), timeout=15000)
        expect(self.page.locator("nav").get_by_role("button", name="Logout")).to_be_visible(timeout=15000)

    def logout(self):
        self.page.locator("nav").get_by_role("button", name="Logout").click()
        expect(self.page).to_have_url(re.compile(r"/login$"))


class CatalogPage:
    def __init__(self, page):
        self.page = page

    def search(self, query):
        self.page.goto("/products")
        self.page.get_by_role("searchbox", name="Search products").fill(query)

    def open_product(self, title):
        self.search(title)
        self.page.get_by_role("img", name=title, exact=True).click()
        expect(self.page.get_by_role("heading", name=title, exact=True)).to_be_visible()

    def add(self, title, quantity=1):
        self.open_product(title)
        self.page.get_by_role("button", name="M", exact=True).click()
        for _ in range(quantity - 1):
            self.page.get_by_role("button", name="+", exact=True).click()
        with self.page.expect_response(lambda r: r.url.endswith("/api/cart/add") and r.request.method == "POST") as response:
            self.page.get_by_role("button", name="Add to Cart", exact=True).click()
        assert response.value.status == 201


class CartPage:
    def __init__(self, page):
        self.page = page

    def open(self):
        self.page.locator("nav").get_by_role("link", name="Cart", exact=True).click()
        expect(self.page.get_by_role("heading", name="Your Cart")).to_be_visible()

    def check_item(self, title, quantity, total):
        expect(self.page.get_by_role("heading", name=title)).to_be_visible()
        expect(self.page.get_by_text(f"Qty: {quantity}", exact=True)).to_be_visible()
        expect(self.page.get_by_text(f"$ {total}", exact=True)).to_be_visible()

    def checkout(self):
        self.page.get_by_role("button", name="Proceed to Checkout").click()
        expect(self.page.get_by_role("heading", name="Checkout", exact=True)).to_be_visible()


class CheckoutPage:
    def __init__(self, page):
        self.page = page

    def place(self, email):
        fields = {"firstName": "Lab", "lastName": "Tester", "email": email,
                  "address": "Oak 7", "city": "Berlin", "pinCode": "10115"}
        for name, value in fields.items():
            self.page.locator(f'input[name="{name}"]').fill(value)
        with self.page.expect_response(lambda r: r.url.endswith("/api/orders/create") and r.request.method == "POST") as response:
            self.page.get_by_role("button", name="Place Order").click()
        assert response.value.status == 201
        expect(self.page.get_by_role("heading", name="Order Placed Successfully!")).to_be_visible()
        expect(self.page.get_by_text("Oak 7, Berlin, 10115", exact=False)).to_be_visible()
