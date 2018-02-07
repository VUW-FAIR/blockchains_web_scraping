import re
import os
import requests
import time
from bs4 import BeautifulSoup
import csv

'''
This script downloads all the IRC comments from http://bitcoinstats.com/.
Start it at the last page (most recent set of IRC comments).
Script goes through all days in the month and saves IRC discussion into CSV file.
Then goes to previous month, and continues until no more months with IRC data exist. 
'''

folder_name = "bitcoin_stats_bitcoin_core_dev_output"
def main():
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    parse_pages('http://bitcoinstats.com/irc/bitcoin-dev/logs/2018/01')

def parse_pages(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    time_links = soup.find_all("a")

    for link in time_links:
        time_links1 = link['href']
        if( re.match("^[0-9]", time_links1)):
            print(time_links1)
            new_url = url + "/" + str(time_links1).split("/")[1]
            #making name of file url name (removing characters that aren't allowed such as '/')
            name = (new_url.replace("/", "_").replace(":", "").replace("-", "_").replace(".", "")) + ".csv"
            time.sleep(4)
            parse_page(new_url, name = name)
    try:
        back_button = soup.find('li',attrs={'class':'previous'})
        back_button_url = "http://bitcoinstats.com" + (back_button.find('a')['href'])
        print(back_button_url)
        time.sleep(60)
        parse_pages(back_button_url)
    except Exception as ex:
        print(ex)
        print("No more pages to parse")


def parse_page(url, name):
    time.sleep(10)
    html = requests.get(url)
    time.sleep(5)
    soup = BeautifulSoup(html.content, "html.parser")

    rows = soup.find_all("tr")
    csv_file = open(folder_name + "/" + name, "w", encoding="utf-8")

    for row in rows: #tr is row, td is col
        cols = row.find_all('td')
        print(cols[0].text)
        print(cols[1].text)
        print(cols[2].text)

        writer = csv.writer(csv_file)
        writer.writerow((cols[0].text, cols[1].text, cols[2].text))

    csv_file.close()

main()
