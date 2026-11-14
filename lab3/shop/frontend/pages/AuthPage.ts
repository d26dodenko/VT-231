import { Page } from "@playwright/test";

export class AuthPage {
  constructor(private readonly page: Page) {}

  async openRegistration() {
    await this.page.goto("/signup");
  }

  async openLogin() {
    await this.page.goto("/login");
  }

  async register(
    name: string,
    email: string,
    password: string
  ) {
    await this.page.getByPlaceholder("Name").fill(name);
    await this.page.getByPlaceholder("Email").fill(email);
    await this.page.getByPlaceholder("Password").fill(password);

    await this.page.getByRole("button", {
      name: "Sign Up"
    }).click();
  }

  async login(email: string, password: string) {
    await this.page.locator('input[type="email"]').fill(email);
    await this.page.locator('input[type="password"]').fill(password);

    await this.page.locator('form button[type="submit"]').click();
  }
}