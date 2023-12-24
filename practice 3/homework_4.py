import json
import xml.etree.ElementTree as ET


def getInfo(fileName):
    with open(fileName, "rb") as f:
        contents = f.read()
    root = ET.fromstring(contents)
    clothing_items = []
    for clothing_element in root.findall("clothing"):
        clothing_item = {}

        clothing_item["id"] = clothing_element.findtext("id", default="").strip()
        clothing_item["name"] = clothing_element.findtext("name", default="").strip()
        clothing_item["category"] = clothing_element.findtext("category", default="").strip()
        clothing_item["size"] = clothing_element.findtext("size", default="").strip()
        clothing_item["color"] = clothing_element.findtext("color", default="").strip()
        clothing_item["material"] = clothing_element.findtext("material", default="").strip()
        clothing_item["price"] = clothing_element.findtext("price", default="").strip()
        clothing_item["rating"] = clothing_element.findtext("rating", default="").strip()
        clothing_item["reviews"] = clothing_element.findtext("reviews", default="").strip()
        clothing_item["new"] = clothing_element.findtext("new", default="").strip()
        clothing_item["exclusive"] = clothing_element.findtext("exclusive", default="").strip()

        clothing_items.append(clothing_item)
    return clothing_items


result = []
for i in range(1, 100):
    result.extend(getInfo(f"resources/4/{i}.xml"))

copyResult = result

result = sorted(result, key=lambda x: float(x["rating"]), reverse=True)

result = list(filter(lambda x: x["exclusive"] == "yes", result))

reviews = [int(item["reviews"]) for item in copyResult]
_max = max(reviews)
_min = min(reviews)
avg = int(sum(reviews) / len(reviews))

print(f"Статистика по reviews:")
print(f"Максимум: {_max}")
print(f"Минимум: {_min}")
print(f"В среднем: {avg}")
print("-------------------------")

materials = [item.get("material", "NoNe") for item in copyResult]
freqRes = {}
for res in materials:
    freqRes[res] = freqRes.get(res, 0) + 1
for res, freq in freqRes.items():
    print(f"{res}: {freq}")
print("-------------------------")

print(f"Всего записей получилось: {len(result)}")

with open('results/result_4.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=4)