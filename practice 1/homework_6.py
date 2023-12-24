import requests
import pandas as pd


response = requests.get('https://randomuser.me/api/').json()['results'][0]
df = pd.DataFrame(data=response)
df = df.fillna(' ').T
html = df.to_html()
# print(df.to_html())
with open('results/r_text_43.html', 'w') as result:
    for item in html:
        result.write(item)
