import csv
import requests
from bs4 import BeautifulSoup


'''
A simple script to extract some information from sites:
in this case extracts from weusecoins
'''
html=requests.get("https://www.weusecoins.com/en/whos-who/")
soup = BeautifulSoup(html.content, "html.parser")
names = soup.findAll('div',attrs={'class':'name'})
position = soup.findAll('div',attrs={'class':'position'})

for i in range(0, len(names)):
    print(names[i].text)
    print(position[i].text)


csv_file = open("people.csv", "a", encoding="utf-8")
writer = csv.writer(csv_file)
for i in range(0, len(names)):
    writer.writerow((names[i].text, position[i].text))
csv_file.close()

