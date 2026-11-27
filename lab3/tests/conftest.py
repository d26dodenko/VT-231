import os
from pathlib import Path
from uuid import uuid4

import pytest
import requests
from playwright.sync_api import sync_playwright

API = os.getenv("API_URL", "http://127.0.0.1:5001/api")
WEB = os.getenv("WEB_URL", "http://127.0.0.1:5173")
REPORT = Path(__file__).resolve().parents[1] / "reports" / "ui"


def new_account():
    return {"fullName": "Lab QA", "email": f"qa-{uuid4().hex}@example.com", "password": uuid4().hex}


@pytest.fixture
def fresh_account():
    return new_account()


@pytest.fixture
def api():
    with requests.Session() as session:
        def call(method, path, **kwargs):
            return session.request(method, API + path, timeout=10, **kwargs)
        yield call


@pytest.fixture
def account(api):
    data = new_account()
    res = api("POST", "/users/register", json=data)
    assert res.status_code == 200, res.text
    return data


@pytest.fixture
def auth(api, account):
    res = api("POST", "/users/login", json={"email": account["email"], "password": account["password"]})
    assert res.status_code == 200, res.text
    data = res.json()
    return {"headers": {"Authorization": "Bearer " + data["token"]}, "user_id": data["userId"]}


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        instance = p.chromium.launch(
    headless=os.getenv("HEADED") != "1",
    channel=os.getenv("BROWSER_CHANNEL") or None
)
        yield instance
        instance.close()


@pytest.fixture
def page(browser, request):
    REPORT.mkdir(parents=True, exist_ok=True)
    context = browser.new_context(base_url=WEB, viewport={"width": 1440, "height": 1000})
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    yield page
    try:
        page.screenshot(path=str(REPORT / f"{request.node.name}.png"), full_page=True, timeout=5000)
    finally:
        context.tracing.stop(path=str(REPORT / f"{request.node.name}.zip"))
        context.close()
