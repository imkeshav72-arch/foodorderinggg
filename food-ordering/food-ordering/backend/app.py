from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3, os
from datetime import datetime

app = Flask(__name__)
CORS(app)
DB = os.getenv("DB_PATH", "food.db")

def get_db():
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row; return c

def init_db():
    with get_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, category TEXT, price REAL,
            description TEXT, image_emoji TEXT, available INTEGER DEFAULT 1, rating REAL DEFAULT 4.5
        );
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT, customer_phone TEXT, address TEXT,
            items TEXT, total REAL, status TEXT DEFAULT 'placed',
            created TEXT
        );
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT, item_id INTEGER, qty INTEGER
        );
        """)
        # Seed menu if empty
        count = db.execute("SELECT COUNT(*) as c FROM menu").fetchone()["c"]
        if count == 0:
            items = [
                ("Margherita Pizza","Pizza",12.99,"Classic tomato & mozzarella","🍕",1,4.8),
                ("BBQ Chicken Pizza","Pizza",15.99,"Smoky BBQ with grilled chicken","🍕",1,4.7),
                ("Pepperoni Pizza","Pizza",14.99,"Loaded with pepperoni slices","🍕",1,4.9),
                ("Veggie Burger","Burger",9.99,"Fresh veggies with lettuce & tomato","🍔",1,4.5),
                ("Classic Beef Burger","Burger",11.99,"Juicy beef patty with special sauce","🍔",1,4.8),
                ("Double Smash Burger","Burger",13.99,"Double patty crispy smash style","🍔",1,4.9),
                ("Chicken Biryani","Rice",13.99,"Fragrant basmati with spiced chicken","🍛",1,4.9),
                ("Paneer Tikka","Starter",8.99,"Grilled cottage cheese with spices","🧀",1,4.6),
                ("Pasta Carbonara","Pasta",11.99,"Creamy egg & parmesan sauce","🍝",1,4.7),
                ("Caesar Salad","Salad",7.99,"Romaine, croutons, parmesan dressing","🥗",1,4.4),
                ("Chocolate Lava Cake","Dessert",6.99,"Warm cake with molten chocolate center","🍫",1,4.9),
                ("Mango Lassi","Drinks",3.99,"Creamy mango yogurt drink","🥭",1,4.8),
            ]
            db.executemany("INSERT INTO menu(name,category,price,description,image_emoji,available,rating) VALUES(?,?,?,?,?,?,?)", items)
        db.commit()

init_db()

@app.route("/api/menu")
def menu():
    cat = request.args.get("category","")
    with get_db() as db:
        q = "SELECT * FROM menu WHERE available=1"
        rows = db.execute(q + (" AND category=?" if cat else ""), ([cat] if cat else [])).fetchall()
    return jsonify({"success":True,"data":[dict(r) for r in rows]})

@app.route("/api/menu/categories")
def categories():
    with get_db() as db:
        rows = db.execute("SELECT DISTINCT category FROM menu WHERE available=1").fetchall()
    return jsonify({"success":True,"data":["All"]+[r["category"] for r in rows]})

@app.route("/api/orders", methods=["POST"])
def place_order():
    b = request.get_json(silent=True) or {}
    required = ["customer_name","customer_phone","address","items","total"]
    for f in required:
        if not b.get(f): return jsonify({"success":False,"error":f"{f} is required"}),400
    import json
    with get_db() as db:
        db.execute("INSERT INTO orders(customer_name,customer_phone,address,items,total,status,created) VALUES(?,?,?,?,?,?,?)",
            (b["customer_name"],b["customer_phone"],b["address"],
             json.dumps(b["items"]),b["total"],"placed",datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        db.commit()
        oid = db.execute("SELECT last_insert_rowid() as id").fetchone()["id"]
    return jsonify({"success":True,"data":{"order_id":oid,"status":"placed","estimated":"30-45 min"}}),201

@app.route("/api/orders/<int:oid>")
def get_order(oid):
    with get_db() as db:
        row = db.execute("SELECT * FROM orders WHERE id=?", (oid,)).fetchone()
    if not row: return jsonify({"success":False,"error":"Not found"}),404
    return jsonify({"success":True,"data":dict(row)})

@app.route("/api/health")
def health(): return jsonify({"status":"ok"})

if __name__ == "__main__":
    print("🍕 Food Ordering API on http://localhost:5000")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT",5000)), debug=True)
