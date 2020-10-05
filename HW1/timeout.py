from concurrent.futures import ProcessPoolExecutor

# Warning: this does not terminate function if timeout
def timeout_five(fnc, *args, **kwargs):
    with ProcessPoolExecutor() as p:
        f = p.submit(fnc, *args, **kwargs)
        return f.result(timeout=5)