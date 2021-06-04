from functools import wraps
from django.core.cache import caches


class ColdCacheException(Exception):
    pass


def cached_function(ttl, prefix=""):

    cache = caches["default"]

    def _get_cache_key(function_name, *args, **kwargs):
        arr = [function_name]
        arr.extend([str(arg) for arg in args])
        for key, value in kwargs.items():
            arr.extend([str(key), str(value)])
        return "{}:{}".format(prefix, ":".join(arr))

    def cached_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            cache_key = _get_cache_key(func.__name__, *args, **kwargs)
            lock_key = "Lock:{}".format(cache_key)

            cached_value = cache.get(cache_key)

            if cached_value is not None:
                # value fresh enough
                return cached_value

            try:
                with cache.lock(lock_key, timeout=5 * 60, blocking_timeout=None):
                    calculated_value = func(*args, **kwargs)
            except Exception:
                if cached_value is not None:
                    return cached_value
                else:
                    calculated_value = func(*args, **kwargs)

            cache.set(cache_key, calculated_value, ttl)
            return calculated_value

        return func_wrapper

    return cached_decorator
