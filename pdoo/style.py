from functools import wraps

mark = object()

def style(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        cache_key = (
            fn.__module__,
            fn.__name__,
            *args,
            mark,
            *kwargs.items()
        )
        return (cache_key, fn(*args, **kwargs))
    return wrapper