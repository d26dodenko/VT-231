
import { test, expect } from "@playwright/test";
import path from "path";
import { ProductsPage } from "../pages/ProductsPage";

test("Поиск товара по названию", async ({ page }) => {
  const productsPage = new ProductsPage(page);

  await productsPage.open();

  // Проверяем, что каталог загружен
  await expect(
    productsPage.productTitle("Basic Cotton T-Shirt")
  ).toBeVisible();

  // Ищем конкретный товар
  await productsPage.searchProduct("Hoodie");

  // Нужный товар остался в каталоге
  await expect(
    productsPage.productTitle("Everyday Hoodie")
  ).toBeVisible();

  // Остальные товары скрыты
  await expect(
    productsPage.productTitle("Classic Denim Jacket")
  ).toHaveCount(0);

  await expect(
    productsPage.productTitle("Casual Sneakers")
  ).toHaveCount(0);

  // Сохраняем скриншот
  await page.screenshot({
    path: path.resolve(
      process.cwd(),
      "../../Screenshots/06_search.png"
    ),
    fullPage: true
  });
});
