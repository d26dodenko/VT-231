import { test, expect } from '@playwright/test';


test.describe.configure({ mode: 'serial' });

let testEmail: string;

test.describe('Авторизация и Регистрация', () => {
  
  test('Успешная регистрация нового пользователя', async ({ page }) => {
    testEmail = `test${Date.now()}@example.com`;
    console.log('Регистрируем:', testEmail);

    await page.goto('http://localhost:5174/signup'); 
    
    await page.getByPlaceholder('Name').fill('Auto Tester');
    await page.getByPlaceholder('Email').fill(testEmail); 
    await page.getByPlaceholder('Password').fill('password123');
    
    await page.getByRole('button', { name: 'Sign Up' }).click();
    await page.waitForTimeout(2000);
  });

  test('Успешный вход в систему', async ({ page }) => {
    
    await page.goto('http://localhost:5174/login');
    
    await page.locator('input[type="email"]').fill(testEmail); 
    await page.locator('input[type="password"]').fill('password123');
    
    await page.getByRole('button', { name: 'Login' }).click();
    
    await page.waitForTimeout(2000);
  });

});