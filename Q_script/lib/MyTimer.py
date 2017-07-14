import time

def measure_time(func):
    def wrapped(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            runtime = time.time() - start
            print "Execution time: %.6f seconds" % runtime
    return wrapped
