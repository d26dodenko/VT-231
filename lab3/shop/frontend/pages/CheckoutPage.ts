
import { Page } from "@playwright/test";

export class CheckoutPage {
  constructor(private readonly page: Page) {}

  async fillShippingDetails(email: string) {
    await this.page.locator('[name="firstName"]').fill("Artem");
    await this.page.locator('[name="lastName"]').fill("Test");
    await this.page.locator('[name="email"]').fill(email);
    await this.page.locator('[name="address"]').fill("Test Street 10");
    await this.page.locator('[name="city"]').fill("Test City");
    await this.page.locator('[name="pinCode"]').fill("123456");
  }

  async placeOrder() {
    await this.page.getByRole("button", {
      name: "Place Order"
    }).click();
  }
}
