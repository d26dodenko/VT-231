const mongoose = require('mongoose');
require('dotenv').config();

const Product = require('./models/ProductModel');

const products = [
  { 
    title: "T-Shirt", 
    name: "T-Shirt",
    description: "Cool t-shirt", 
    price: 20, 
    category: "Men", 
    brand: "Nike",       
    quantity: 10,        
    size: "M",           
    image: "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500" 
  },
  { 
    title: "Jeans", 
    name: "Jeans",
    description: "Blue jeans", 
    price: 50, 
    category: "Men",
    brand: "Levi's",     
    quantity: 5,         
    size: "L",           
    image: "https://images.unsplash.com/photo-1542272604-787c3835535d?w=500" 
  },
  { 
    title: "Sneakers", 
    name: "Sneakers",
    description: "Sport shoes", 
    price: 80, 
    category: "Unisex",
    brand: "Adidas",     
    quantity: 15,        
    size: "42",          
    image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500" 
  }
];

async function seedDB() {
  try {
    await mongoose.connect(process.env.MONGO_URI);
    console.log("Connected to DB for seeding");
    await Product.deleteMany({}); 
    await Product.insertMany(products); 
    console.log("Products added successfully!");
    process.exit();
  } catch (error) {
    console.error("Error:", error);
    process.exit(1);
  }
}

seedDB();