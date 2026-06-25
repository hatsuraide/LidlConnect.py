import time
from functools import wraps


def ttl_cache(seconds: int):
    """Per-instance TTL cache decorator."""
    def decorator(method):
        cache_attr = f'_ttlc_{method.__qualname__.replace(".", "_")}'

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            now = time.monotonic()
            cache: dict = getattr(self, cache_attr, {})
            key = (args, tuple(sorted(kwargs.items())))
            if key in cache:
                value, ts = cache[key]
                if now - ts < seconds:
                    return value
            result = method(self, *args, **kwargs)
            cache[key] = (result, now)
            setattr(self, cache_attr, cache)
            return result

        wrapper._cache_attr = cache_attr
        return wrapper
    return decorator


def invalidate_cache(instance, method):
    """Clear the TTL cache for a cached method on an instance."""
    attr = getattr(method, '_cache_attr', None)
    if attr and hasattr(instance, attr):
        delattr(instance, attr)
