
export function filterProducts<T extends { title: string }>(
  products: T[],
  query: string
): T[] {
  const searchText = query.trim().toLowerCase();

  return products.filter((product) =>
    product.title.toLowerCase().includes(searchText)
  );
}
