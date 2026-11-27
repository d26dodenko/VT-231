export interface PricedItem {
  price: number;
  quantity: number;
}

export function cartSubtotal(items: readonly PricedItem[]): number {
  let total = 0;
  for (const item of items) {
    total += item.price * item.quantity;
  }
  return total;
}

export function cartTotal(items: readonly PricedItem[]): number {
  return Math.round(cartSubtotal(items));
}

export function removeCartItem<T extends { _id: string }>(items: readonly T[], id: string): T[] {
  return items.filter(item => item._id !== id);
}

export function shippingAddress(address: string, city: string, pin: string): string {
  return [address.trim(), city.trim(), pin.trim()].join(", ");
}
