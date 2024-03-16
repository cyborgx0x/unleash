
from functools import wraps


def check_permission(func):

    @wraps(func)
    def decorated_view(*args, **kwargs):
        
        return func(*args, **kwargs)

    return decorated_view