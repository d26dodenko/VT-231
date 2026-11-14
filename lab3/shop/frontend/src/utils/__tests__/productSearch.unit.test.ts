
import { describe, expect, it } from "vitest";
import { filterProducts } from "../productSearch";

const products = [
  { id: 1, title: "Basic Cotton T-Shirt" },
  { id: 2, title: "Everyday Hoodie" },
  { id: 3, title: "Classic Denim Jacket" },
  { id: 4, title: "Casual Sneakers" }
];

describe("Фильтрация товаров", () => {
  it("Находит товар по полному названию", () => {
    const result = filterProducts(products, "Everyday Hoodie");

    expect(result).toHaveLength(1);
    expect(result[0].id).toBe(2);
  });

  it("Находит товар по части названия", () => {
    const result = filterProducts(products, "Denim");

    expect(result[0].title).toBe("Classic Denim Jacket");
  });

  it("Не учитывает регистр символов", () => {
    const result = filterProducts(products, "hoodie");

    expect(result).toHaveLength(1);
  });

  it("Удаляет пробелы по краям запроса", () => {
    const result = filterProducts(products, "  sneakers  ");

    expect(result[0].id).toBe(4);
  });

  it("Возвращает все товары при пустом запросе", () => {
    const result = filterProducts(products, "");

    expect(result).toHaveLength(4);
  });

  it("Возвращает все товары при запросе из пробелов", () => {
    const result = filterProducts(products, "   ");

    expect(result).toHaveLength(4);
  });

  it("Возвращает пустой массив, если совпадений нет", () => {
    const result = filterProducts(products, "Laptop");

    expect(result).toEqual([]);
  });

  it("Корректно обрабатывает пустой каталог", () => {
    const result = filterProducts([], "Hoodie");

    expect(result).toEqual([]);
  });

  it("Находит несколько подходящих товаров", () => {
    const result = filterProducts(products, "a");

    expect(result.length).toBeGreaterThan(1);
  });

  it("Не изменяет исходный массив", () => {
    const result = filterProducts(products, "Hoodie");

    expect(products).toHaveLength(4);
    expect(result).not.toBe(products);
  });

  it("Находит товар при смешанном регистре", () => {
  const result = filterProducts(products, "hOoDiE");

  expect(result).toHaveLength(1);
  expect(result[0].title).toBe("Everyday Hoodie");
});

it("Находит совпадение в середине названия", () => {
  const result = filterProducts(products, "tton");

  expect(result).toHaveLength(1);
  expect(result[0].title).toBe("Basic Cotton T-Shirt");
});
});
