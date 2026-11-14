
require("dotenv").config();
const mongoose = require("mongoose");
const Product = require("../models/ProductModel");

const products = [
  {
    title: "Basic Cotton T-Shirt",
    category: "Clothing",
    description: "Comfortable cotton T-shirt for everyday wear.",
    brand: "Clothify",
    price: 25,
    rating: 4.5,
    reviews: "18",
    images: ["https://placehold.co/600x800/e0f2f1/115e59.png?text=Cotton+T-Shirt"],
    quantity: 30,
    size: "M",
    sizes: ["S", "M", "L", "XL"]
  },
  {
    title: "Everyday Hoodie",
    category: "Clothing",
    description: "Warm and comfortable casual hoodie.",
    brand: "Clothify",
    price: 60,
    rating: 4.7,
    reviews: "24",
    images: ["https://placehold.co/600x800/dbeafe/1e3a8a.png?text=Everyday+Hoodie"],
    quantity: 20,
    size: "L",
    sizes: ["S", "M", "L", "XL"]
  },
  {
    title: "Classic Denim Jacket",
    category: "Clothing",
    description: "Classic denim jacket with a modern fit.",
    brand: "UrbanWear",
    price: 95,
    rating: 4.8,
    reviews: "32",
    images: ["https://placehold.co/600x800/e5e7eb/374151.png?text=Denim+Jacket"],
    quantity: 15,
    size: "M",
    sizes: ["S", "M", "L", "XL"]
  },
  {
    title: "Casual Sneakers",
    category: "Footwear",
    description: "Lightweight sneakers for daily use.",
    brand: "StreetStep",
    price: 80,
    rating: 4.6,
    reviews: "15",
    images: ["https://placehold.co/600x800/fef3c7/78350f.png?text=Casual+Sneakers"],
    quantity: 25,
    size: "M",
    sizes: ["S", "M", "L", "XL"]
  }
];

async function seedProducts() {
  try {
    await mongoose.connect(process.env.MONGO_URI);

    for (const product of products) {
      await Product.findOneAndUpdate(
        { title: product.title },
        { $set: product },
        { upsert: true, runValidators: true }
      );
    }

    console.log("Added or updated 4 test products");
  } catch (error) {
    console.error(error);
    process.exitCode = 1;
  } finally {
    await mongoose.disconnect();
  }
}

seedProducts();
  