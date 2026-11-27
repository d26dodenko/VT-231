import assert from 'node:assert/strict';
import { test } from 'node:test';
import { cartSubtotal, cartTotal, removeCartItem, shippingAddress } from '../src/utils/cartPricing.ts';

const line = (price, quantity) => ({ price, quantity });
const a = { _id: 'a', title: 'Shirt' };
const b = { _id: 'b', title: 'Scarf' };

const subtotalCases = [
  ['empty subtotal', [], 0],
  ['one item', [line(35, 1)], 35],
  ['multiple quantity', [line(35, 3)], 105],
  ['different items', [line(35, 2), line(22, 3)], 136],
  ['zero quantity', [line(35, 0)], 0],
  ['free item', [line(0, 4)], 0],
  ['fractional price', [line(12.5, 2)], 25],
  ['large quantity', [line(75, 100)], 7500],
];
for (const [name, items, expected] of subtotalCases) {
  test(name, () => assert.equal(cartSubtotal(items), expected));
}

const totals = [
  ['empty total', [], 0],
  ['round down', [line(10.49, 1)], 10],
  ['round half up', [line(10.5, 1)], 11],
  ['round after summing', [line(0.4, 1), line(0.4, 1)], 1],
];
for (const [name, items, expected] of totals) {
  test(name, () => assert.equal(cartTotal(items), expected));
}

test('remove one item', () => assert.deepEqual(removeCartItem([a, b], 'a'), [b]));
test('missing id keeps items', () => assert.deepEqual(removeCartItem([a, b], 'x'), [a, b]));
test('remove last item', () => assert.deepEqual(removeCartItem([a], 'a'), []));
test('remove from empty', () => assert.deepEqual(removeCartItem([], 'a'), []));
test('removal does not mutate input', () => {
  const items = Object.freeze([a, b]);
  removeCartItem(items, 'b');
  assert.deepEqual(items, [a, b]);
});
test('normal address', () => assert.equal(shippingAddress('Oak 7', 'Berlin', '10115'), 'Oak 7, Berlin, 10115'));
test('trim address components', () => assert.equal(shippingAddress(' Oak 7 ', ' Berlin ', ' 10115 '), 'Oak 7, Berlin, 10115'));
test('preserve postal leading zero', () => assert.equal(shippingAddress('Oak 7', 'City', '01234'), 'Oak 7, City, 01234'));
