
import { Page } from "@playwright/test";

export class CartPage {
  constructor(private readonly page: Page) {}

  async open() {
    await this.page.goto("/cart");
  }

  productTitle(name: string) {
    return this.page.getByRole("heading", {
      name,
      exact: true
    });
  }

  async proceedToCheckout() {
    await this.page
      .getByRole("button", { name: "Proceed to Checkout" })
      .click();
  }
}
