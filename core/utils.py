import random
import string


def get_random_str(n: int):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))