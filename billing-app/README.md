# 🛒 Billing System - Mallow Technologies (100% Production Ready)

## 🎯 Features Implemented
✅ Product management with stock tracking  
✅ Dynamic billing form (Add New button)  
✅ Tax calculations per item  
✅ Denomination-based payment tracking  
✅ Automatic change calculation (greedy algorithm)  
✅ Bill history by customer email  
✅ PostgreSQL database  
✅ FastAPI + Jinja2 templates  
✅ Production-grade error handling  

## 🛠️ Prerequisites (Install First)
1. **Python 3.11+**
2. **PostgreSQL 14+** (localhost:5432)
3. **Poetry** (`pip install poetry`)

## 🚀 A-Z Setup Instructions (5 Minutes)

### Step 1: Clone & Navigate
```bash
git clone <your-repo-url>
cd billing-app
```

### Step 2: Install Dependencies
```bash
poetry install
poetry shell
```

### Step 3: Setup PostgreSQL Database
```sql
CREATE DATABASE billing_db;
CREATE USER interview_user WITH PASSWORD 'interview_password';
GRANT ALL PRIVILEGES ON DATABASE billing_db TO interview_user;
```

### Step 4: Configure Environment
```bash
cp .env.example .env
```
Edit `.env`:
```
DATABASE_URL=postgresql://interview_user:interview_password@localhost:5432/billing_db
```

### Step 5: Initialize Database & Seed Products
```bash
# Terminal 1: Server still running

# Terminal 2: Add products
curl -X POST "http://localhost:8000/api/products" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "P001", "name": "Laptop", "stock": 10, "price": 50000, "tax_pct": 18}'

curl -X POST "http://localhost:8000/api/products" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "P002", "name": "Mouse", "stock": 50, "price": 500, "tax_pct": 18}'

curl -X POST "http://localhost:8000/api/products" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "P003", "name": "Keyboard", "stock": 25, "price": 2500, "tax_pct": 18}'

```

### Step 6: Start Server
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 7: Open Application
🌐 http://localhost:8000  
📚 http://localhost:8000/docs

## 📱 API Endpoints
POST /api/generate-bill → Generate bill  
GET /api/bills/{email} → Bill history  
GET / → Billing page

## 📈 Production Deployment
```bash
poetry export -f requirements.txt --output requirements.txt
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🚀 QUICK START
```bash
mkdir billing-app && cd billing-app
poetry install && poetry shell
poetry run uvicorn app.main:app --reload
```

### ♻️ Reset Tables
```bash
# Browser: http://localhost:8000

# Test 1
# Fill form:
Email: test@gmail.com
Product: {P002, Qty: 2}
Payment Details: {500: 2, 50: 2, 10: 3}
Cash: 1180

# Result: Page 2 Success ✅

# Test 2
# Fill form:
Email: test@gmail.com
Product: P001, Qty: 1
Product: P002, Qty: 1
Product: P003, Qty: 1
Payment Details: 500: 125, 50: 0, 10: 4
Cash: 62540

# Result: Page 2 Success ✅
```

### ♻️ Reset Tables
```bash
DROP TABLE IF EXISTS bill_items CASCADE;
DROP TABLE IF EXISTS bills CASCADE;
DROP TABLE IF EXISTS products CASCADE;

CREATE TABLE products (
    id VARCHAR PRIMARY KEY,
    product_id VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL,
    stock INTEGER NOT NULL,
    price FLOAT NOT NULL,
    tax_pct FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE bills (
    id VARCHAR PRIMARY KEY,
    customer_email VARCHAR NOT NULL,
    total_pre_tax FLOAT NOT NULL,
    total_tax FLOAT NOT NULL,
    net_total FLOAT NOT NULL,
    rounded_total FLOAT NOT NULL,
    cash_paid FLOAT NOT NULL,
    change_due FLOAT NOT NULL,
    balance_denominations VARCHAR,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE bill_items (
    id VARCHAR PRIMARY KEY,
    bill_id VARCHAR NOT NULL REFERENCES bills(id),
    product_id VARCHAR NOT NULL,
    unit_price FLOAT NOT NULL,
    quantity INTEGER NOT NULL,
    tax_pct FLOAT NOT NULL,
    subtotal FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()  
);
```
