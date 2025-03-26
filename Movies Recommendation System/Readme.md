# 🎬 Movie Recommendation System

A Python-based movie recommendation system that uses **user similarity** to suggest movies. This project follows the **SOLID principles** for clean and scalable architecture.

## 📌 Features
- Supports user-based **movie rating system**.
- Recommends movies for both **new users** and **existing users**.
- Implements **user similarity scoring** for better recommendations.
- Uses **clean code structure** with interface-based design.

## 🏗️ Design Patterns & Principles Used
### **1️⃣ Single Responsibility Principle (SRP)**
- `RatingRegister` handles movie ratings.
- `MovieRecommendation` is responsible for recommendations.

### **2️⃣ Open/Closed Principle (OCP)**
- The recommendation system can support **multiple algorithms**.

### **3️⃣ Liskov Substitution Principle (LSP)**
- The `IMovieRecommender` interface ensures interchangeable recommendation strategies.

### **4️⃣ Interface Segregation Principle (ISP)**
- `IRatingRegister` and `IMovieRecommender` keep interfaces **lightweight and focused**.

### **5️⃣ Dependency Inversion Principle (DIP)**
- The system depends on **abstractions**, not concrete classes.

## 🚀 How It Works
1. Users rate movies from **1 to 5 stars**.
2. The system recommends:
   - **For new users** → The highest-rated movie.
   - **For existing users** → A movie liked by a similar user.

