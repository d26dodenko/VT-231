
import { Page } from "@playwright/test";

export class ProductsPage {
  constructor(private readonly page: Page) {}

  async open() {
    await this.page.goto("/");
  }

  async searchProduct(name: string) {
    await this.page
      .getByRole("searchbox", { name: "Search products" })
      .fill(name);
  }


async addProductToCart(name: string) {
  const productCard = this.page
    .locator("div.group")
    .filter({
      has: this.productTitle(name)
    });

  await productCard
    .getByRole("button", { name: "Add Cart" })
    .click();
}

async openCart() {
  await this.page
    .locator("nav")
    .getByRole("link", { name: "Cart" })
    .click();
}


  productTitle(name: string) {
    return this.page.getByRole("heading", {
      name,
      exact: true
    });
  }
}

