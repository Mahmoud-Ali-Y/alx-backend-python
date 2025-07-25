import sqlite3
import functools
import logging
from datetime import datetime

#### decorator to lof SQL queries

 """ YOUR CODE GOES HERE"""

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sql_logger")

# --- Decorator to log SQL queries ---
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)
        logger.info(f"Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print users