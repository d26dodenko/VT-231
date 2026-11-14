
import { test, expect } from "@playwright/test";
import path from "path";

import { AuthPage } from "../pages/AuthPage";
import { ProductsPage } from "../pages/ProductsPage";
import { CartPage } from "../pages/CartPage";
import { CheckoutPage } from "../pages/CheckoutPage";

test("Оформление заказа", async ({ page }) => {
  const authPage = new AuthPage(page);
  const productsPage = new ProductsPage(page);
  const cartPage = new CartPage(page);
  const checkoutPage = new CheckoutPage(page);

  const email = `artem.order.${Date.now()}@example.com`;
  const password = "TestPass123!";

  // Регистрация и авторизация
  await authPage.openRegistration();
  await authPage.register("Artem Order", email, password);

  await expect(page).toHaveURL(/\/login$/);

  await authPage.login(email, password);
  await expect(page).toHaveURL("http://127.0.0.1:5173/");

  // Добавление товара
  await expect(
    productsPage.productTitle("Everyday Hoodie")
  ).toBeVisible();

  await productsPage.addProductToCart("Everyday Hoodie");

  // Переход в корзину
  await cartPage.open();

  await expect(
    cartPage.productTitle("Everyday Hoodie")
  ).toBeVisible();

  await cartPage.proceedToCheckout();

  // Проверка страницы оформления
  await expect(page).toHaveURL(/\/checkout$/);
  await expect(
    page.getByRole("heading", { name: "Checkout" })
  ).toBeVisible();

  // Заполнение адреса
  await checkoutPage.fillShippingDetails(email);

  // Контроль ответа API при создании заказа
  const orderResponsePromise = page.waitForResponse(
    response =>
      response.url().includes("/api/orders/create") &&
      response.request().method() === "POST"
  );

  await checkoutPage.placeOrder();

  const orderResponse = await orderResponsePromise;
  expect(orderResponse.status()).toBe(201);

  // Проверка подтверждения заказа
  await expect(page).toHaveURL(/\/placed$/);

  await expect(
    page.getByRole("heading", {
      name: "Order Placed Successfully!"
    })
  ).toBeVisible();

  await expect(
    page.getByText("Order Summary")
  ).toBeVisible();

  await expect(
    page.getByText("Everyday Hoodie")
  ).toBeVisible();

  // Скриншот результата
  await page.screenshot({
    path: path.resolve(
      process.cwd(),
      "../../screenshots/10_checkout.png"
    ),
    fullPage: true
  });
});
