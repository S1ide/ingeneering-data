import json
import pymongo


def create_collection(url):
    client = pymongo.MongoClient(url)
    db = client['db']
    db.drop_collection('workers')
    collection = db['workers']
    return collection


def add_data(table, data):
    objects = []

    for item in data:
        record = {'id': item['id'], 'job': item['job'], 'age': item['age'], 'city': item['city'],
                  'salary': item['salary'], 'year': item['year']}
        objects.append(record)

    table.insert_many(objects)


def save_sorted_salary(table):
    result = list(table.find().sort('salary', pymongo.DESCENDING).limit(10))

    with open("results/salary_sorted.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(result, ensure_ascii=False, default=str))


def save_filtered_age(table):
    result = list(table.find({'age': {'$lt': 30}}).sort('salary', pymongo.DESCENDING).limit(15))

    with open("results/age_filtered.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(result, ensure_ascii=False, default=str))


def save_filtered_city(table):
    query = {"city": "Вроцлав",
             "job": {"$in": ["Врач", "Бухгалтер", "Водитель"]}
             }
    result = list(table.find(query, limit=10).sort({"age": 1}))

    with open("results/filtered_by_city.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(result, ensure_ascii=False, default=str))


def save_complex_filtered(table):
    query = {
        "age": {"$gt": 18, "$lt": 35},
        "year": {"$in": [2019, 2020, 2021, 2022]},
        "$or": [{"salary": {"$gt": 50000, "$lte": 75000}},
                {"salary": {"$gt": 125000, "$lt": 150000}}]
    }
    result = len(list(table.find(query)))

    with open("results/complex_filter.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(result, ensure_ascii=False, default=str))


data = []

with open('resources/task_1_item.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

table = create_collection("mongodb://localhost:27017")

save_sorted_salary(table)

save_filtered_age(table)

save_filtered_city(table)

save_complex_filtered(table)