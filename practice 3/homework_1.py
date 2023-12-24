import json
from bs4 import BeautifulSoup


def getChessInfo(fileName):
    with open(fileName, "rb") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')

    chess_info = {}
    chess_info['тип'] = soup.find('div', {'class': 'chess-wrapper'}).find('div').span.text.split(":")[1].strip()
    chess_info['название'] = soup.find('h1', {'class': 'title'}).text.split('Турнир:')[1].strip().split(' ')[0]
    chess_info['год'] = soup.find('h1', {'class': 'title'}).text.split('Турнир:')[1].strip().split(' ')[1]

    address_data = soup.find('p', {'class': 'address-p'}).text.split('Начало:')
    chess_info['город'] = address_data[0].replace('\r\n', '').replace('Город: ', '').strip()
    chess_info['дата начала'] = address_data[1].strip()
    chess_info['количество туров'] = soup.find('span', {'class': 'count'}).text.split(': ')[1].strip()
    chess_info['время в минутах'] = soup.find('span', {'class': 'year'}).text.strip().split(' ')[2].strip()
    chess_info['минимальный рейтинг для участия'] = soup.find_all('span')[-3].text.split(':')[1].strip()
    chess_info['рейтинг'] = soup.find('div', {'class': 'chess-wrapper'}).find_all('span')[-2].text.split(': ')[
        1].strip()
    chess_info['просмотры'] = soup.find('div', {'class': 'chess-wrapper'}).find_all('span')[-1].text.split(': ')[
        1].strip()

    return chess_info


result = []
for i in range(1, 999):
    result.append(getChessInfo(f"resources/1/{i}.html"))

copyResult = result

result = sorted(result, key=lambda x: float(x["рейтинг"]), reverse=True)

result = list(filter(lambda x: int(x["время в минутах"]) > 120, result))

views = [int(item["просмотры"]) for item in copyResult]
maxViews = max(views)
minViews = min(views)
avgViews = int(sum(views) / len(views))

print(f"Статистика по просмотрам:")
print(f"Максимум: {maxViews}")
print(f"Минимум: {minViews}")
print(f"В среднем: {avgViews}")
print("-------------------------")

cities = [item["город"] for item in copyResult]
freqCities = {}
for city in cities:
    freqCities[city] = freqCities.get(city, 0) + 1
for city, freq in freqCities.items():
    print(f"{city}: {freq}")
print("-------------------------")

print(f"Всего записей получилось: {len(result)}")

with open('results/result_1.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=4)
