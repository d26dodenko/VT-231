
import { test, expect } from "@playwright/test";
import path from "path";
import { AuthPage } from "../pages/AuthPage";
import { ProductsPage } from "../pages/ProductsPage";
import { CartPage } from "../pages/CartPage";

test("Добавление товара в корзину", async ({ page }) => {
  const authPage = new AuthPage(page);
  const productsPage = new ProductsPage(page);
  const cartPage = new CartPage(page);

  const email = `artem.cart.${Date.now()}@example.com`;
  const password = "TestPass123!";

  // Регистрируем нового пользователя
  await authPage.openRegistration();
  await authPage.register("Artem Cart", email, password);

  await expect(page).toHaveURL(/\/login$/);

  // Входим в аккаунт
  await authPage.login(email, password);
  await expect(page).toHaveURL("http://127.0.0.1:5173/");

  // Ждём загрузки каталога
  await expect(
    productsPage.productTitle("Everyday Hoodie")
  ).toBeVisible();

  // Проверяем ответ API при добавлении товара
  const responsePromise = page.waitForResponse(
    response =>
      response.url().includes("/api/cart/add") &&
      response.request().method() === "POST"
  );

  await productsPage.addProductToCart("Everyday Hoodie");

  const response = await responsePromise;
  expect(response.status()).toBe(201);

  // Открываем корзину
  await productsPage.openCart();

  await expect(
    page.getByRole("heading", { name: "Your Cart" })
  ).toBeVisible();

  // Проверяем, что товар находится в корзине
  await expect(
    cartPage.productTitle("Everyday Hoodie")
  ).toBeVisible();

  await expect(
    page.getByRole("button", { name: "Proceed to Checkout" })
  ).toBeVisible();

  // Сохраняем скриншот
  await page.screenshot({
    path: path.resolve(
      process.cwd(),
      "../../screenshots/08_cart.png"
    ),
    fullPage: true
  });
});
