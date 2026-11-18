# 1
import redis
import json
import time


r = redis.Redis(host="localhost", port=6379, decode_responses=True)

r.delete("board")

r.zadd("board", {"linh": 1200, "nam": 950, "mai": 1430, "hoa": 1100, "tuan": 800})

r.zincrby("board", 300, "nam") 

top3 = r.zrevrange("board", 0, 2, withscores=True)

print("TOP 3")
rank = 1
for player, score in top3:
    print(f"Hạng {rank}: {player} - {int(score)} điểm")
    rank += 1

print("Hạng của hoa:", r.zrevrank("board", "hoa") + 1)



# 2
users = [
    {"id": "1", "name": "Linh", "city": "hanoi", "age": "21"},
    {"id": "2", "name": "Nam", "city": "hcm", "age": "22"},
    {"id": "3", "name": "Mai", "city": "hanoi", "age": "20"},
    {"id": "4", "name": "Tuan", "city": "danang", "age": "23"},
    {"id": "5", "name": "Hoa", "city": "hcm", "age": "21"},
]

for u in users:
    r.delete(f"user:{u['id']}")
r.delete("city:hanoi", "city:hcm", "city:danang")

for u in users:
    r.hset(f"user:{u['id']}", mapping=u)   
    r.sadd(f"city:{u['city']}", u["id"])  


def find_by_city(city):
    ids = r.smembers(f"city:{city}")
    result = []
    for user_id in sorted(ids):
        result.append(r.hgetall(f"user:{user_id}"))
    return result


print("Hồ sơ user 1:", r.hgetall("user:1"))
print("Chỉ lấy tên user 2:", r.hget("user:2", "name"))

for city in ["hanoi", "hcm", "danang"]:
    print(f"\nUser ở {city}:")
    for u in find_by_city(city):
        print(f"  {u['id']}. {u['name']}, {u['age']} tuổi")



# 3
N = 100          
DELAY = 0.1


def slow_query(product_id):
    time.sleep(DELAY) 
    return {"id": product_id, "title": "Python Basics", "price": 12.5}


def get_product(product_id):
    key = f"product:{product_id}"
    cached = r.get(key)
    if cached is not None:
        return json.loads(cached)               
    product = slow_query(product_id)            
    r.set(key, json.dumps(product), ex=300)      
    return product


start = time.perf_counter()
for _ in range(N):
    slow_query(7)
no_cache = time.perf_counter() - start

r.delete("product:7")
start = time.perf_counter()
for _ in range(N):
    get_product(7)
with_cache = time.perf_counter() - start

print(f"Không cache : {no_cache:.3f} s")
print(f"Có cache    : {with_cache:.3f} s")
print(f"Tăng tốc    : {no_cache / with_cache:.1f} lần")

