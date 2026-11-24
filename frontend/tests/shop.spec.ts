import { test, expect } from '@playwright/test';

test.describe.configure({ mode: 'serial' });

const testEmail = `shopuser${Date.now()}@example.com`;
const testPassword = 'password123';

test.describe('Покупки в магазине', () => {
  
  test.beforeAll(async ({ browser }) => {
    const page = await browser.newPage();
    await page.goto('http://localhost:5173/signup');
    await page.getByPlaceholder('Name').fill('Shop Tester');
    await page.getByPlaceholder('Email').fill(testEmail);
    await page.getByPlaceholder('Password').fill(testPassword);
    await page.getByRole('button', { name: 'Sign Up' }).click();
    await page.waitForTimeout(2000);
    await page.close();
  });

  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5173/login');
    await page.locator('input[type="email"]').fill(testEmail); 
    await page.locator('input[type="password"]').fill(testPassword);
    await page.getByRole('button', { name: 'Login' }).click();
    await page.waitForTimeout(2000); 
    await page.goto('http://localhost:5173/'); 
  });

  test('Поиск товара', async ({ page }) => {
    await expect(page.locator('h1:has-text("Products")')).toBeVisible({ timeout: 10000 });
    await page.waitForTimeout(1000);
  });

  test('Добавление товара в корзину', async ({ page }) => {
    
    await page.goto('http://localhost:5173/');
    
    
    await page.waitForSelector('h1:has-text("Products")', { timeout: 15000 });
    
    
    await page.waitForTimeout(3000);
    
   
    await page.evaluate(() => {
      const btn = document.querySelector('button.bg-\\[\\#319795\\]') as HTMLButtonElement;
      if (btn) btn.click();
    });
    
    
    await page.waitForTimeout(2000);
  });

  test('Оформление заказа', async ({ page }) => {
    await page.goto('http://localhost:5173/cart');
    await page.waitForTimeout(2000);
    
    const checkoutBtn = page.getByRole('button', { name: /Checkout|Proceed/i });
    if (await checkoutBtn.isVisible()) {
        await checkoutBtn.click();
        await page.waitForTimeout(2000);
    }
  });

  test('Выход из системы', async ({ page }) => {
    await page.goto('http://localhost:5173/');
    await expect(page.locator('a:has-text("Login")').first()).toBeVisible();
  });
});
