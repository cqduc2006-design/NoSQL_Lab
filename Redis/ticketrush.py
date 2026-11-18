import time
import uuid
from concurrent.futures import ThreadPoolExecutor

import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def race(fn, n=50):
    """Run fn(i) from n threads at once and return the list of results."""
    with ThreadPoolExecutor(max_workers=n) as pool:
        return list(pool.map(fn, range(n)))


def hold_naive(event, seat, user):
    key = f"hold:{event}:{seat}"
    if r.get(key) is None:
        time.sleep(0.01)                 # widen the window so the bug is easy to see
        r.set(key, user, ex=300)
        return True
    return False


r.flushdb()
wins = race(lambda i: hold_naive("c1", "A1", f"user{i}"))
print("winners:", sum(wins))             # expect 1, you will see many more


def hold_nx(event, seat, user, ttl=300):
    return bool(r.set(f"hold:{event}:{seat}", user, nx=True, ex=ttl))

r.flushdb()
wins = race(lambda i: hold_nx("c1", "A1", f"user{i}"))
print("winners:", sum(wins))             # always 1