
seed = __import__('seed')
def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

import sys
lazy_paginator = __import__('2-lazy_paginate').lazy_pagination

def lazy_paginate(page_size):
    offset = 0
    for user in paginate_users(page_size, offset):
        yield user

try:
    for page in lazy_paginator(100):
        for user in page:
            print(user)

except BrokenPipeError:
    sys.stderr.close()