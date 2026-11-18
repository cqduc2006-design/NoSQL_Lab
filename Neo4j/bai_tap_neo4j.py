import os
from neo4j import GraphDatabase

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
AUTH = (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "learnneo4j"))
driver = GraphDatabase.driver(URI, auth=AUTH)


def run(cypher, **params):
    return driver.execute_query(cypher, params).records



def setup():
    run("MATCH (n) DETACH DELETE n")
    run("""
        CREATE (linh:Person {name: "Linh", city: "Hanoi",   age: 21}),
               (nam:Person  {name: "Nam",  city: "Da Nang", age: 22}),
               (mai:Person  {name: "Mai",  city: "Hanoi",   age: 20}),
               (hung:Person {name: "Hung", city: "Hue",     age: 23}),
               (py:Book  {title: "Python Basics",   price: 120000}),
               (sql:Book {title: "SQL in Practice", price: 150000}),
               (viz:Book {title: "Data Viz",        price: 135000}),
               (linh)-[:FRIEND {since: 2023}]->(nam),
               (nam)-[:FRIEND {since: 2024}]->(mai),
               (mai)-[:FRIEND {since: 2025}]->(hung),
               (linh)-[:BOUGHT {year: 2026}]->(py),
               (linh)-[:BOUGHT {year: 2026}]->(sql),
               (nam)-[:BOUGHT {year: 2025}]->(sql),
               (nam)-[:BOUGHT {year: 2026}]->(viz),
               (mai)-[:BOUGHT {year: 2026}]->(py),
               (mai)-[:BOUGHT {year: 2026}]->(viz)
    """)
    print("Đã tạo đồ thị cửa hàng.")


# 1 
NEW_PEOPLE = [
    {"name": "Tuan",  "city": "Hanoi", "age": 22},
    {"name": "Lan",   "city": "Hanoi", "age": 21},
    {"name": "Khoa",  "city": "HCMC",  "age": 23},
    {"name": "Ha",    "city": "Hanoi", "age": 20},
    {"name": "Phong", "city": "Hue",   "age": 22},
]
NEW_FRIENDS = [
    ["Nam", "Tuan", 2025],
    ["Nam", "Lan", 2024],
    ["Linh", "Khoa", 2022],
    ["Khoa", "Ha", 2025],
    ["Khoa", "Phong", 2023],
]


def lab_1(name="Linh", city="Hanoi"):
    run("""
        UNWIND $rows AS row
        MERGE (p:Person {name: row.name})
        SET p.city = row.city, p.age = row.age
    """, rows=NEW_PEOPLE)

    run("""
        UNWIND $rows AS f
        MATCH (a:Person {name: f[0]}), (b:Person {name: f[1]})
        MERGE (a)-[r:FRIEND]->(b)
        SET r.since = f[2]
    """, rows=NEW_FRIENDS)

    records = run("""
        MATCH (me:Person {name: $name})-[:FRIEND]-(:Person)-[:FRIEND]-(fof:Person)
        WHERE fof.city = $city
          AND fof <> me
          AND NOT (me)-[:FRIEND]-(fof)
        RETURN DISTINCT fof.name AS name
        ORDER BY name
    """, name=name, city=city)
    return [r["name"] for r in records]


# 2
def lab_2_1(name="Mai"):
    records = run("""
        MATCH (me:Person {name: $name})-[:FRIEND]-(friend:Person)-[:BOUGHT]->(book:Book)
        WHERE NOT (me)-[:BOUGHT]->(book)
        RETURN book.title AS title, count(DISTINCT friend) AS friends
        ORDER BY friends DESC, title
    """, name=name)
    return [(r["title"], r["friends"]) for r in records]


def lab_2_2():
    records = run("""
        MATCH (p:Person)
        OPTIONAL MATCH (p)-[:BOUGHT]->(b:Book)
        RETURN p.name AS name, sum(b.price) AS total
        ORDER BY total DESC, name
    """)
    return [(r["name"], r["total"]) for r in records]


# 3
METRO = [
    ["A", "B", 3], ["B", "C", 2], ["C", "D", 4], ["D", "E", 3],
    ["F", "C", 3], ["C", "G", 6], ["G", "H", 4], ["E", "H", 2],
]


def lab_3(start="A", goal="H"):
    run("""
        UNWIND $rows AS r
        MERGE (a:Station {name: r[0]})
        MERGE (b:Station {name: r[1]})
        MERGE (a)-[n:NEXT]->(b)
        SET n.minutes = r[2]
    """, rows=METRO)

    records = run("""
        MATCH (s:Station {name: $start}), (g:Station {name: $goal}),
              p = shortestPath((s)-[:NEXT*..20]-(g))
        RETURN [x IN nodes(p) | x.name] AS route,
               reduce(t = 0, r IN relationships(p) | t + r.minutes) AS minutes
    """, start=start, goal=goal)
    if not records:
        return [], 0
    return records[0]["route"], records[0]["minutes"]



JOBS = [
    {"person": "Linh", "company": "FPT",     "position": "Intern",           "start": "2023-06-01", "end": "2023-12-31"},
    {"person": "Linh", "company": "Viettel", "position": "Data Analyst",     "start": "2024-01-15", "end": None},
    {"person": "Nam",  "company": "FPT",     "position": "Developer",        "start": "2022-03-01", "end": "2024-05-31"},
    {"person": "Nam",  "company": "VNG",     "position": "Senior Developer", "start": "2024-06-15", "end": None},
    {"person": "Mai",  "company": "Viettel", "position": "Tester",           "start": "2023-09-01", "end": None},
]





# 4
def lab_4():
    run("""
        UNWIND $rows AS row
        MATCH (p:Person {name: row.person})
        MERGE (c:Company {name: row.company})
        MERGE (p)-[w:WORKED_AT {position: row.position, start: date(row.start)}]->(c)
        SET w.end = date(row.end)
    """, rows=JOBS)

    run("""
        UNWIND $rows AS row
        MATCH (p:Person {name: row.person})
        MERGE (c:Company {name: row.company})
        MERGE (p)-[:HAS_JOB]->(j:Job {position: row.position, start: date(row.start)})-[:AT]->(c)
        SET j.end = date(row.end)
    """, rows=JOBS)

    run("""
        UNWIND $rows AS r
        MATCH (:Person {name: r[0]})-[:HAS_JOB]->(j:Job {position: r[1]})
        MERGE (s:Skill {name: r[2]})
        MERGE (j)-[:USES]->(s)
    """, rows=[["Linh", "Data Analyst", "Python"],
               ["Linh", "Data Analyst", "SQL"],
               ["Nam", "Senior Developer", "Python"]])


def lich_su_cach_1(name):
    records = run("""
        MATCH (:Person {name: $name})-[w:WORKED_AT]->(c:Company)
        RETURN c.name AS company, w.position AS position, w.start AS start, w.end AS end
        ORDER BY w.start
    """, name=name)
    return [(r["company"], r["position"], str(r["start"]), str(r["end"])) for r in records]


def dang_lam_tai(company):
    records = run("""
        MATCH (p:Person)-[w:WORKED_AT]->(:Company {name: $company})
        WHERE w.end IS NULL
        RETURN p.name AS name ORDER BY name
    """, company=company)
    return [r["name"] for r in records]


def dong_nghiep():
    records = run("""
        MATCH (a:Person)-[w1:WORKED_AT]->(c:Company)<-[w2:WORKED_AT]-(b:Person)
        WHERE a.name < b.name
          AND w1.start <= coalesce(w2.end, date())
          AND w2.start <= coalesce(w1.end, date())
        RETURN a.name AS a, b.name AS b, c.name AS company
        ORDER BY a, b
    """)
    return [(r["a"], r["b"], r["company"]) for r in records]


def lich_su_cach_2(name):
    records = run("""
        MATCH (:Person {name: $name})-[:HAS_JOB]->(j:Job)-[:AT]->(c:Company)
        RETURN c.name AS company, j.position AS position, j.start AS start, j.end AS end
        ORDER BY j.start
    """, name=name)
    return [(r["company"], r["position"], str(r["start"]), str(r["end"])) for r in records]


def ai_dung_ky_nang(skill):
    records = run("""
        MATCH (p:Person)-[:HAS_JOB]->(j:Job)-[:USES]->(:Skill {name: $skill}),
              (j)-[:AT]->(c:Company)
        RETURN p.name AS name, j.position AS position, c.name AS company
        ORDER BY name
    """, skill=skill)
    return [(r["name"], r["position"], r["company"]) for r in records]


# So sánh hai cách:
# - Cách 1 (property trên relationship): ít node, truy vấn ngắn; đủ để xem lịch
#   sử làm việc, ai đang làm ở đâu, ai là đồng nghiệp cùng thời gian.
#   Nhưng không gắn thêm được node khác (kỹ năng, phòng ban, quản lý) vào một công việc.
# - Cách 2 (node :Job): thêm một bước nhảy, nhưng mỗi công việc là một thực thể
#   riêng nên nối được tới Skill, Department, Manager... => trả lời được câu hỏi
#   kiểu "ai đã dùng Python, ở công ty nào".


# 5
def profile_tim_linh():
    """Chạy PROFILE, trả về (operator đầu tiên, tổng db hits)."""
    _, summary, _ = driver.execute_query(
        "PROFILE MATCH (p:Person {name: $name}) RETURN p", {"name": "Linh"})

    ops = []
    stack = [summary.profile]
    while stack:
        op = stack.pop()
        ops.append(op)
        stack.extend(op.get("children", []))

    first = ops[-1]["operatorType"].split("@")[0]
    total_hits = sum(op.get("dbHits", 0) for op in ops)
    return first, total_hits


def bai_5():
    run("DROP CONSTRAINT person_name IF EXISTS")
    before = profile_tim_linh()

    run("""CREATE CONSTRAINT person_name IF NOT EXISTS
           FOR (p:Person) REQUIRE p.name IS UNIQUE""")
    after = profile_tim_linh()
    return before, after

# Giải thích:
# - Chưa có constraint: NodeByLabelScan (+ Filter). Neo4j đọc MỌI node :Person rồi
#   so name với "Linh", nên db hits tăng theo số người trong database.
# - Có constraint: NodeUniqueIndexSeek. Constraint tạo sẵn index trên Person.name,
#   Neo4j nhảy thẳng tới Linh, db hits rất ít và gần như không đổi dù có 100.000 người.
# - Constraint còn chặn việc tạo hai Person trùng tên.



if __name__ == "__main__":
    try:
        setup()

        print("\n--- Bài 1 ---")
        print("Bạn của bạn của Linh ở Hà Nội:", lab_1())

        print("\n--- Bài 2 ---")
        print("Gợi ý sách cho Mai:", lab_2_1())
        print("Tổng tiền mỗi người:")
        for name, total in lab_2_2():
            print(f"  {name:6} {total:>8,}")

        print("\n--- Bài 3 ---")
        route, minutes = lab_3()
        print(f"Tuyến A -> H: {' -> '.join(route)} ({len(route)} ga, {minutes} phút)")

        print("\n--- Bài 4 ---")
        lab_4()
        print("Cách 1 – lịch sử của Linh:", lich_su_cach_1("Linh"))
        print("Cách 1 – đang làm ở Viettel:", dang_lam_tai("Viettel"))
        print("Cách 1 – đồng nghiệp:", dong_nghiep())
        print("Cách 2 – lịch sử của Linh:", lich_su_cach_2("Linh"))
        print("Cách 2 – ai dùng Python:", ai_dung_ky_nang("Python"))

        print("\n--- Bài 5 ---")
        before, after = bai_5()
        print(f"Chưa có constraint: {before[0]}, {before[1]} db hits")
        print(f"Đã có constraint:   {after[0]}, {after[1]} db hits")
    finally:
        driver.close()
