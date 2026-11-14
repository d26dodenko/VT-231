import { test, expect } from "@playwright/test";
import path from "path";
import { AuthPage } from "../pages/AuthPage";

test("Регистрация нового пользователя", async ({ page }) => {
  const authPage = new AuthPage(page);

  const email = `artem.lab3.${Date.now()}@example.com`;

  await authPage.openRegistration();

  await expect(
    page.getByRole("heading", { name: "Sign Up" })
  ).toBeVisible();

  await authPage.register(
    "Artem Test",
    email,
    "TestPass123!"
  );

  await expect(
    page.locator(".Toastify__toast--success")
  ).toBeVisible();

  await page.screenshot({
    path: path.resolve(
      process.cwd(),
      "../../screenshots/02_registration.png"
    ),
    fullPage: true
  });

  await expect(page).toHaveURL(/\/login$/);
});


test("Вход зарегистрированного пользователя", async ({ page }) => {
  const authPage = new AuthPage(page);

  const email = `artem.login.${Date.now()}@example.com`;
  const password = "TestPass123!";

  // Создаём отдельного пользователя для теста входа
  await authPage.openRegistration();
  await authPage.register("Artem Login", email, password);

  await expect(page).toHaveURL(/\/login$/);

  // Выполняем вход через Page Object
  await authPage.login(email, password);

  // Проверяем, что приложение сохранило токен
  await expect.poll(async () => {
    return await page.evaluate(() => localStorage.getItem("token"));
  }).toMatch(/\S+/);

  // Проверяем переход на главную страницу
  await expect(page).toHaveURL("http://127.0.0.1:5173/");

  // Сохраняем доказательство успешного входа
  await page.screenshot({
    path: "../../screenshots/04_login.png",
    fullPage: true
  });
});


test("Выход пользователя из системы", async ({ page }) => {
  const authPage = new AuthPage(page);

  const email = `artem.logout.${Date.now()}@example.com`;
  const password = "TestPass123!";

  // Регистрируем пользователя
  await authPage.openRegistration();
  await authPage.register("Artem Logout", email, password);

  await expect(page).toHaveURL(/\/login$/);

  // Входим в систему
  await authPage.login(email, password);
  await expect(page).toHaveURL("http://127.0.0.1:5173/");

  // Проверяем наличие авторизации
  await expect(
    page.getByRole("button", { name: "Logout" })
  ).toBeVisible();

  // Выходим из аккаунта
  await page.getByRole("button", {
    name: "Logout"
  }).click();

  // Проверяем переход на Login
  await expect(page).toHaveURL(/\/login$/);

  // Проверяем удаление токена
  const token = await page.evaluate(() => {
    return localStorage.getItem("token");
  });

  expect(token).toBeNull();

  await page.screenshot({
    path: path.resolve(
      process.cwd(),
      "../../screenshots/11_logout.png"
    ),
    fullPage: true
  });
});
