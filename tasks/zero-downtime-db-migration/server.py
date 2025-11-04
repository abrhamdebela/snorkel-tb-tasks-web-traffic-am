import os
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()

# Configuration from environment variables
DUAL_WRITE = os.getenv('DUAL_WRITE', 'false').lower() == 'true'
PRIMARY_DB = os.getenv('PRIMARY_DB', 'old-db')

# Database connection strings
DB_CONFIGS = {
    'old-db': {
        'host': 'old-db',
        'port': 5432,
        'database': 'appdb',
        'user': 'admin',
        'password': 'admin123'
    },
    'new-db': {
        'host': 'new-db',
        'port': 5432,
        'database': 'appdb',
        'user': 'admin',
        'password': 'admin123'
    }
}

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str

class OrderCreate(BaseModel):
    user_id: int
    product_name: str
    amount: float
    status: Optional[str] = 'pending'

def get_db_connection(db_name):
    """Get database connection based on name"""
    config = DB_CONFIGS.get(db_name)
    if not config:
        raise ValueError(f"Unknown database: {db_name}")
    return psycopg2.connect(**config)

def execute_write(query, params):
    """Execute write operation with dual-write support"""
    results = {}

    # Write to primary database
    try:
        conn = get_db_connection(PRIMARY_DB)
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        cur.close()
        conn.close()
        results[PRIMARY_DB] = 'success'
    except Exception as e:
        results[PRIMARY_DB] = f'error: {str(e)}'

    # If dual-write is enabled, write to secondary database
    if DUAL_WRITE:
        secondary_db = 'new-db' if PRIMARY_DB == 'old-db' else 'old-db'
        try:
            conn = get_db_connection(secondary_db)
            cur = conn.cursor()
            cur.execute(query, params)
            conn.commit()
            cur.close()
            conn.close()
            results[secondary_db] = 'success'
        except Exception as e:
            results[secondary_db] = f'error: {str(e)}'

    return results

@app.get('/health')
def health():
    """Health check endpoint"""
    return {'status': 'healthy', 'primary_db': PRIMARY_DB, 'dual_write': DUAL_WRITE}

@app.get('/users')
def get_users():
    """Get all users from primary database"""
    try:
        conn = get_db_connection(PRIMARY_DB)
        cur = conn.cursor()
        cur.execute("SELECT id, username, email FROM users")
        users = [{'id': row[0], 'username': row[1], 'email': row[2]} for row in cur.fetchall()]
        cur.close()
        conn.close()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/users', status_code=201)
def create_user(user: UserCreate):
    """Create a new user"""
    try:
        query = "INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id"
        params = (user.username, user.email)
        results = execute_write(query, params)
        return {'message': 'User created', 'write_results': results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/orders')
def get_orders():
    """Get all orders from primary database"""
    try:
        conn = get_db_connection(PRIMARY_DB)
        cur = conn.cursor()
        cur.execute("SELECT id, user_id, product_name, amount, status FROM orders")
        orders = [
            {
                'id': row[0],
                'user_id': row[1],
                'product_name': row[2],
                'amount': float(row[3]),
                'status': row[4]
            }
            for row in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/orders', status_code=201)
def create_order(order: OrderCreate):
    """Create a new order"""
    try:
        query = "INSERT INTO orders (user_id, product_name, amount, status) VALUES (%s, %s, %s, %s) RETURNING id"
        params = (order.user_id, order.product_name, order.amount, order.status)
        results = execute_write(query, params)
        return {'message': 'Order created', 'write_results': results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)
