import random
from datetime import datetime, timedelta, timezone

import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
bt = client.baitap_mongodb

pd.set_option("display.width", 140)
pd.set_option("display.max_columns", 20)



# 1
bt.orders.drop()

bt.orders.insert_many([

    {"_id": 2001,
     "customer": {"name": "Linh", "city": "Hanoi"},
     "status": "paid",
     "items": [
         {"sku": "BK-01", "title": "Python Basics",   "qty": 2, "price": 12.5},
         {"sku": "BK-07", "title": "SQL in Practice", "qty": 1, "price": 18.0},
     ]},


    {"_id": 2002,
     "customer": {"name": "Nam", "city": "Da Nang"},
     "status": "shipped",
     "coupon": "WELCOME10",
     "shipping": {"method": "express", "fee": 3.0},
     "items": [
         {"sku": "BK-03", "title": "Data Viz",      "qty": 1, "price": 22.0},
         {"sku": "BK-01", "title": "Python Basics", "qty": 1, "price": 12.5},
     ]},


    {"_id": 2003,
     "customer": {"name": "Mai", "city": "Hue"},
     "status": "cancelled",
     "cancel_reason": "out of stock",
     "cancelled_at": datetime(2026, 11, 10, 9, 30, tzinfo=timezone.utc),
     "items": [
         {"sku": "BK-07", "title": "SQL in Practice", "qty": 2, "price": 18.0},
     ]},


    {"_id": 2004,
     "customer": {"name": "Hung", "city": "Hanoi"},
     "status": "shipped",
     "gift": {"wrap": True, "message": "Happy 20/11!"},
     "tags": ["gift", "teacher-day"],
     "items": [
         {"sku": "BK-05", "title": "Statistics 101", "qty": 1, "price": 30.0},
     ]},


    {"_id": 2005,
     "customer": {"name": "Thao", "city": "Ho Chi Minh City", "phone": "0900000000"},
     "status": "paid",
     "payment": {"method": "momo",
                 "paid_at": datetime(2026, 11, 15, 14, 0, tzinfo=timezone.utc)},
     "items": [
         {"sku": "BK-01", "title": "Python Basics",    "qty": 3, "price": 12.5},
         {"sku": "BK-09", "title": "Machine Learning", "qty": 1, "price": 25.0,
          "variant": "hardcover"},
     ]},
])

print("Số đơn đã thêm:", bt.orders.count_documents({}))


def find_orders_by_sku(sku):
    return list(bt.orders.find(
        {"items.sku": sku},
        {"_id": 1, "customer.name": 1, "status": 1},
    ).sort("_id", 1))


SKU = "BK-01"
print(f"\nCác đơn chứa sku = {SKU}:")
for doc in find_orders_by_sku(SKU):
    print(" ", doc)

print(f"\nCác đơn có item {SKU} với qty >= 2 ($elemMatch):")
for doc in bt.orders.find(
        {"items": {"$elemMatch": {"sku": SKU, "qty": {"$gte": 2}}}},
        {"_id": 1, "items": {"$elemMatch": {"sku": SKU}}},
).sort("_id", 1):
    print(" ", doc)



# 2
revenue_pipeline = [
    {"$match": {"status": {"$in": ["paid", "shipped"]}}},             
    {"$addFields": {                                                  
        "order_total": {"$sum": {"$map": {
            "input": "$items", "as": "i",
            "in": {"$multiply": ["$$i.qty", "$$i.price"]}}}}}},
    {"$group": {                                                      
        "_id": "$customer.city",
        "revenue": {"$sum": "$order_total"},
        "orders": {"$sum": 1},
    }},
    {"$project": {"_id": 0, "city": "$_id",
                  "revenue": {"$round": ["$revenue", 2]}, "orders": 1}},
    {"$sort": {"revenue": -1}},                                    
]

df_revenue = pd.DataFrame(bt.orders.aggregate(revenue_pipeline))
print(df_revenue[["city", "revenue", "orders"]].to_string(index=False))



# 3
rng = random.Random(42)

CITIES = ["Hanoi", "Ho Chi Minh City", "Da Nang", "Hue", "Can Tho",
          "Hai Phong", "Nha Trang", "Vinh"]
STATUSES = ["paid", "shipped", "cancelled", "pending"]
NAMES = ["Linh", "Nam", "Mai", "Hung", "Thao", "Duc", "Minh", "Tan", "Lan", "Quan"]
PRODUCTS = [
    {"sku": "BK-01", "title": "Python Basics",    "price": 12.5},
    {"sku": "BK-03", "title": "Data Viz",         "price": 22.0},
    {"sku": "BK-05", "title": "Statistics 101",   "price": 30.0},
    {"sku": "BK-07", "title": "SQL in Practice",  "price": 18.0},
    {"sku": "BK-09", "title": "Machine Learning", "price": 25.0},
    {"sku": "BK-11", "title": "Econometrics",     "price": 28.0},
]
N = 10_000
START = datetime(2026, 1, 1, tzinfo=timezone.utc)


def random_order(i):
    items = []
    for _ in range(rng.randint(1, 4)):
        p = rng.choice(PRODUCTS)
        items.append({**p, "qty": rng.randint(1, 5)})
    doc = {
        "_id": 100_000 + i,
        "customer": {"name": rng.choice(NAMES), "city": rng.choice(CITIES)},
        "status": rng.choice(STATUSES),
        "created_at": START + timedelta(days=rng.randint(0, 320)),
        "items": items,
    }
    if rng.random() < 0.2:                      
        doc["coupon"] = f"SALE{rng.randint(5, 30)}"
    if rng.random() < 0.1:                       
        doc["tags"] = ["gift"]
    return doc


big = bt.orders_big
big.drop()                                     
big.insert_many([random_order(i) for i in range(N)])
print("Số document trong orders_big:", big.count_documents({}))


def explain(query):
    """Chạy lệnh explain ở mức executionStats cho một truy vấn find."""
    return bt.command({"explain": {"find": big.name, "filter": query},
                       "verbosity": "executionStats"})


def summarize(label, exp):
    """Rút gọn kết quả explain thành vài con số quan trọng.
    MongoDB 7/8 có thể bọc plan trong winningPlan.queryPlan (engine SBE)."""
    wp = exp["queryPlanner"]["winningPlan"]
    node = wp.get("queryPlan", wp)
    stages, index_name = [], None
    while node:
        stages.append(node["stage"])
        index_name = node.get("indexName", index_name)
        node = node.get("inputStage") or (node.get("inputStages") or [None])[0]
    s = exp["executionStats"]
    return {
        "lần đo": label,
        "plan": " -> ".join(stages),
        "index": index_name or "(không)",
        "nReturned": s["nReturned"],
        "keysExamined": s["totalKeysExamined"],
        "docsExamined": s["totalDocsExamined"],
        "ms": s["executionTimeMillis"],
    }


QUERY = {"customer.city": "Hanoi", "status": "paid"}


print("\nIndex hiện có:", [ix["name"] for ix in big.list_indexes()])
before = summarize("TRƯỚC index", explain(QUERY))


ix_name = big.create_index([("customer.city", 1), ("status", 1)])
print("Đã tạo index:", ix_name)


after = summarize("SAU index", explain(QUERY))

print(f"\nSo sánh explain() cho truy vấn {QUERY}:")
print(pd.DataFrame([before, after]).to_string(index=False))

ratio = before["docsExamined"] / max(after["docsExamined"], 1)
print(f"\n=> Số document phải đọc giảm từ {before['docsExamined']} xuống "
      f"{after['docsExamined']} (ít hơn khoảng {ratio:.1f} lần).")
print("=> TRƯỚC: COLLSCAN (quét toàn bộ). SAU: IXSCAN rồi FETCH đúng các document khớp.")


print("\n(Thêm) Quy tắc tiền tố của index ghép:")
print(pd.DataFrame([
    summarize("chỉ lọc city", explain({"customer.city": "Hanoi"})),  
    summarize("chỉ lọc status", explain({"status": "paid"})),         
]).to_string(index=False))

client.close()
