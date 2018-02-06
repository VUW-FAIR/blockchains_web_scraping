import os
import requests
import time

folder_name = "botbotme_bitcoin_core_dev"

#if the folder doesn't exist, make it
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

url = "https://botbot.me/freenode/bitcoin-core-dev/2018-01-01.log?page=1"

'''
This script scrapes all IRC chat logs for the specified IRC chatroom.
Supply the start url of a botbotme IRC chat log (end time) and script will go through and request all
previous logs, saving as txt file. 
'''

try:
    while True:
        r=requests.get(url)
        f_name = url.split("/")[len(url.split("/"))-1].replace("-","_").replace("?", "_")
        print(f_name)
        with open(folder_name + "/" + f_name +".txt", "w", encoding="utf-8") as out:
            out.write(r.text)
            print(r.text)
        print(r.headers['X-PrevPage'])
        url = "https://botbot.me" + r.headers['X-PrevPage']
        time.sleep(1)
except Exception as e:
    print("finished" + (e))