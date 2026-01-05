// ======================================================
// Task 2.2: MongoDB Operations for FlexiMart
// ======================================

// Operation 1: Load Data
// Use mongoimport to load the JSON file into the 'products' collection
// Command (Run in terminal): mongoimport --db fleximart --collection products --file products_catalog.json --jsonArray

// Operation 2: Basic Query
// Find "Electronics" category with price < 50,000 (INR)
db.products.find(
  { category: "Electronics", price: { $lt: 50000 } },
  { name: 1, price: 1, stock: 1, _id: 0 }
);

// Operation 3: Review Analysis
// Find products with average rating >= 4.0 using aggregation
db.products.aggregate([
  { 
    $project: { 
      name: 1, 
      avgRating: { $avg: "$reviews.rating" } 
    } 
  },
  { 
    $match: { avgRating: { $gte: 4.0 } } 
  }
]);

// Operation 4: Update Operation
// Add a new review to product "ELEC001"
db.products.updateOne(
  { product_id: "ELEC001" },
  { 
    $push: { 
      reviews: { 
        user: "U999", 
        rating: 4, 
        comment: "Good value", 
        date: new Date() 
      } 
    } 
  }
);

// Operation 5: Complex Aggregation
// Calculate average price by category, count products, sort by price DESC
db.products.aggregate([
  {
    $group: {
      _id: "$category",
      avg_price: { $avg: "$price" },
      product_count: { $sum: 1 }
    }
  },
  {
    $project: {
      category: "$_id",
      _id: 0,
      avg_price: 1,
      product_count: 1
    }
  },
  { $sort: { avg_price: -1 } }
]);