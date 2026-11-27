require("dotenv").config();
const mongoose = require("mongoose");
const Product = require("../models/ProductModel");

const items = [
  ["Linen Shirt", "Clothing", "Northwind", 35],
  ["Canvas Backpack", "Accessories", "Trail", 48],
  ["Wool Scarf", "Accessories", "Northwind", 22],
  ["Running Shoes", "Footwear", "Sprint", 75]
];

async function seed() {
  await mongoose.connect(process.env.MONGO_URI);
  try {
    for (const [title, category, brand, price] of items) {
      await Product.findOneAndUpdate({ title }, { $set: {
        title, category, brand, price, description: `Demo product: ${title}`,
        images: ["/lab-product.svg"], quantity: 20, rating: 4.5,
        reviews: "10", size: "M", sizes: ["S", "M", "L", "XL"]
      } }, { upsert: true, runValidators: true });
    }
    console.log("Test catalog ready");
  } finally { await mongoose.disconnect(); }
}
seed().catch(error => { console.error(error); process.exitCode = 1; });
