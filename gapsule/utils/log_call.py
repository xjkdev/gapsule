import functools


def log_call(log_func=None):
    if log_func is None:
        log_func = print

    def _decorator(f):
        @functools.wraps(f)
        def _wrapper(*args, **kwargs):
            nonlocal log_func
            name = f.__name__ if hasattr(
                f, '__name__') else '<Anonymous Function>'
            sarg = ', '.join(repr(a) for a in args)
            skarg = ', '.join('%s=%s' % (k, repr(v))
                              for k, v in kwargs.items())
            if len(skarg) > 0:
                tmp = ', '.join((sarg, skarg))
            else:
                tmp = sarg
            result = f(*args, **kwargs)
            log_func('Function Called {}({}) -> {}'.format(
                name, tmp, str(result)))
            return result
        return _wrapper
    return _decorator
