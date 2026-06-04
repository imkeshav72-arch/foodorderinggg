# 🍕 FoodRush — Online Food Ordering System

Full-stack food ordering app with Python Flask backend and a clean HTML/CSS/JS frontend.

## Features
- 🍔 Browse menu by category
- 🛒 Add to cart with quantity control
- 📦 Place orders with delivery details
- 🎉 Order confirmation with ID
- 📱 Mobile responsive

## Structure
```
food-ordering/
├── backend/   app.py, requirements.txt
├── frontend/  index.html
└── README.md
```

## Quick Start
```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py          # http://localhost:5000

# Frontend (new terminal)
cd frontend
python -m http.server 8080   # http://localhost:8080
```

## API Endpoints
| Method | Route | Description |
|--------|-------|-------------|
| GET | /api/menu | Get all menu items |
| GET | /api/menu/categories | Get categories |
| POST | /api/orders | Place an order |
| GET | /api/orders/:id | Get order status |

## Tech Stack
Python 3.9+, Flask, SQLite, HTML5, CSS3, Vanilla JS
