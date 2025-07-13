import sys
processing = __import__('1-batch_processing')

##### print processed users in a batch of 50
def stream_users_in_batches(batch_size):
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
    """Yield all users one by one (stream)"""
    for user in processing.batch_processing(batch_size):
        yield user  # loop #1

def batch_processing(batch_size):
    try:
        for user in stream_users_in_batches(batch_size):
            if user.age > 25:
                print(user)
    except BrokenPipeError:
        sys.stderr.close()