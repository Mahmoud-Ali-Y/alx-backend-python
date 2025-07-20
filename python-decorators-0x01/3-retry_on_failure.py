import time
import sqlite3 
import functools

#### paste your with_db_decorator here

# --- Reuse from previous task ---
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # Open DB connection
        try:
            return func(conn, *args, **kwargs)  # Pass connection to function
        finally:
            conn.close()  # Ensure connection is closed
    return wrapper

""" your code goes here"""

# --- Retry decorator ---
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt >= retries:
                        raise  # Re-raise after final attempt
                    time.sleep(delay)  # Wait before retrying
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)