import sys
processing = __import__('1-batch_processing')

##### print processed users in a batch of 50
def stream_users_in_batches(batch_size):
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