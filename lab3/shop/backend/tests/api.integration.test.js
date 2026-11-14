
const { describe, test } = require("node:test");
const assert = require("node:assert/strict");
const { randomUUID } = require("node:crypto");

const baseUrl = process.env.API_BASE_URL || "http://127.0.0.1:5001";

describe("Интеграционное тестирование API магазина", { concurrency: false }, () => {
  const email = `artem.integration.${randomUUID()}@example.com`;
  const password = "TestPass123!";

  let token;
  let userId;
  let product;
  let cartItemId;

  test("1. Регистрация пользователя", async () => {
    const response = await fetch(`${baseUrl}/api/users/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        fullName: "Artem Integration",
        email,
        password
      })
    });

    assert.equal(response.status, 200);

    const data = await response.json();
    assert.equal(data.message, "Signup successful");
  });

  test("2. Авторизация и получение токена", async () => {
    const response = await fetch(`${baseUrl}/api/users/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    assert.equal(response.status, 200);

    const data = await response.json();
    assert.ok(data.token);
    assert.ok(data.userId);

    token = data.token;
    userId = data.userId;
  });

  test("3. Получение товаров из MongoDB", async () => {
    const response = await fetch(`${baseUrl}/api/products`);

    assert.equal(response.status, 200);

    const data = await response.json();
    assert.ok(Array.isArray(data));

    product = data.find((item) => item.title === "Everyday Hoodie");

    assert.ok(product, "Тестовый товар Everyday Hoodie не найден");
    assert.equal(product.price, 60);
  });

  test("4. Добавление товара в корзину", async () => {
    const response = await fetch(`${baseUrl}/api/cart/add`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        userId,
        productId: product._id,
        images: product.images,
        title: product.title,
        price: product.price,
        quantity: 1,
        size: "M"
      })
    });

    assert.equal(response.status, 201);

    const data = await response.json();
    assert.ok(data.cartItem._id);

    cartItemId = data.cartItem._id;
  });

  test("5. Получение корзины пользователя", async () => {
    const response = await fetch(`${baseUrl}/api/cart`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    assert.equal(response.status, 200);

    const data = await response.json();
    assert.ok(Array.isArray(data));

    const cartItem = data.find((item) => item._id === cartItemId);

    assert.ok(cartItem, "Добавленный товар не найден в корзине");
    assert.equal(cartItem.title, "Everyday Hoodie");
  });

  test("6. Создание заказа", async () => {
    const response = await fetch(`${baseUrl}/api/orders/create`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        products: [{
          productId: product._id,
          images: product.images,
          title: product.title,
          quantity: 1,
          price: product.price
        }],
        totalPrice: product.price,
        shippingAddress: "Test Street 10, Test City"
      })
    });

    assert.equal(response.status, 201);

    const data = await response.json();
    assert.ok(data.order._id);
    assert.equal(data.order.totalPrice, 60);
    assert.equal(data.order.paymentStatus, "Pending");
  });
});
