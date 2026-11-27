import re

from playwright.sync_api import expect

from .pages import AuthPage, CartPage, CatalogPage, CheckoutPage


def test_registration(page, fresh_account, api):
    AuthPage(page).register(fresh_account)
    res = api("POST", "/users/login", json={"email": fresh_account["email"], "password": fresh_account["password"]})
    assert res.status_code == 200 and res.json()["token"]


def test_login(page, account):
    AuthPage(page).login(account)
    expect(page.get_by_role("heading", name="Products", exact=True)).to_be_visible()


def test_search(page):
    CatalogPage(page).search("linen")
    expect(page.get_by_role("heading", name="Linen Shirt")).to_be_visible()
    expect(page.get_by_role("heading", name="Running Shoes")).to_have_count(0)
    expect(page.get_by_role("heading", name="Wool Scarf")).to_have_count(0)


def test_add_to_cart(page, account):
    AuthPage(page).login(account)
    CatalogPage(page).add("Linen Shirt", quantity=2)
    cart = CartPage(page)
    cart.open()
    cart.check_item("Linen Shirt", 2, 70)


def test_checkout(page, account):
    AuthPage(page).login(account)
    CatalogPage(page).add("Canvas Backpack", quantity=2)
    cart = CartPage(page)
    cart.open()
    cart.check_item("Canvas Backpack", 2, 96)
    cart.checkout()
    CheckoutPage(page).place(account["email"])
    expect(page.get_by_text("Canvas Backpack", exact=True)).to_be_visible()
    expect(page.get_by_text("₹96", exact=True)).to_be_visible()


def test_logout(page, account):
    auth = AuthPage(page)
    auth.login(account)
    auth.logout()
    assert page.evaluate("localStorage.getItem('token')") is None
    assert page.evaluate("localStorage.getItem('userId')") is None
    page.goto("/cart")
    expect(page).to_have_url(re.compile(r"/login$"))
