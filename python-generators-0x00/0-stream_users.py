from itertools import islice
"""
def fetch_users():
    # Connect to the database (change 'your_database.db' to your file)
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # Write the query
    query = "SELECT * FROM user_data"
    
    # Execute the query
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    return rows
    """
def stream_users():
    stream_users = __import__('0-stream_users')
    for user in islice(stream_users(), 6):
        print(user)