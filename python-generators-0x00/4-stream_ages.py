from itertools import islice

def stream_user_ages():
    stream_users = __import__('0-stream_users')
    count = 0
    for user in islice(stream_users()):
        yield user.age
        count += 1
        total_age += user.age
    return count, total_age

def Average_age_of_users():
    average_parameters = stream_user_ages()
    average_age = average_parameters.total_age / average_parameters.count