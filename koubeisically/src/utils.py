import functools


def log(message):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"{message}: {func.__name__} is running")
            return func(*args, **kwargs)

        return wrapper

    return decorator
