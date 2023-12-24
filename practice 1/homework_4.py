import csv

aver_salary = 0
items = list()

with open('resources/text_4_var_43', newline='\n', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=',')
    for stroka in reader:
        item = {
            'number': int(stroka[0]),
            'name': stroka[2] + " " + stroka[1],
            'age': stroka[3],
            'salary': stroka[4].replace("₽", "")  # УБИРАЕМ СИПВОЛ ₽
        }

        aver_salary += int(item['salary'])
        items.append(item)

aver_salary /= len(items)
filtered = list()
for item in items:
    if (float(item['salary']) > aver_salary) and int(item['age']) > 26:
        filtered.append(item)

filtreed = sorted(filtered, key=lambda i: i['number'])

with open('results/text_4_var_43_result.csv', 'w', encoding="utf-8", newline='') as result:
    writer = csv.writer(result, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for item in filtered:
        writer.writerow(item.values())