import sqlite3 
import functools

"""your code goes here"""

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # Open DB connection
        try:
            result = func(conn, *args, **kwargs)  # Pass connection to the function
            return result
        finally:
            conn.close()  # Always close the connection
    return wrapper

def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)  # Run DB operation
            conn.commit()  # Commit if successful
            return result
        except Exception:
            conn.rollback()  # Rollback on error
            raise  # Re-raise the exception to propagate it
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
cursor = conn.cursor() 
cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')