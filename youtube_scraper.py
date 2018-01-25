import json
import os

import pandas as pandas
import requests
import time

folder_name = "youtube"
key = ""

'''
This script uses the youtube API to extract json information
Note: this only extracts 100 comments at present 
(none of the below videos have more than 100 comments)
'''

def download_from_youtube():

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


    # urls = ['https://www.youtube.com/watch?v=KkcK4ZpoFS0',
    #         'https://www.youtube.com/watch?v=mjmuPqkVwWc',
    #         'https://www.youtube.com/watch?v=MnkssdmlaWw',
    #         'https://www.youtube.com/watch?v=cTX5yY0DozQ',
    #         'https://www.youtube.com/watch?v=PhPZv8nOq5o',
    #         'https://www.youtube.com/watch?v=0lpeZ01H_Bk',
    #         'https://www.youtube.com/watch?v=YC13ttV8SfM',
    #         'https://www.youtube.com/watch?v=IavQ-Wc8S1U',
    #         'https://www.youtube.com/watch?v=tto-nDUdIeQ',
    #         'https://www.youtube.com/watch?v=YbZs4WtzdLE',
    #         'https://www.youtube.com/watch?v=8oeMsfm5D5s']

    #
    # urls = [ 'https://www.youtube.com/watch?v=kEHIOi8iXqE',
    #          'https://www.youtube.com/watch?v=L4iPCpmv678K',
    #          'https://www.youtube.com/watch?v=MsJdkHt3VQY',
    #          'https://www.youtube.com/watch?v=mD4L7xDNCmA',
    #          'https://www.youtube.com/watch?v=FN6Q--zqroM',
    #          'https://www.youtube.com/watch?v=yi4Vm2bqFJw'
    #          ]


    urls = ['https://www.youtube.com/watch?v=tjppPb23mpM',
            'https://www.youtube.com/watch?v=mZj-oQy4LbM',
            'https://www.youtube.com/watch?v=7POTBsvETWE',
            'https://www.youtube.com/watch?v=vmPD_YSQ--k',
            'https://www.youtube.com/watch?v=llKedWKdvU8',
            'https://www.youtube.com/watch?v=pDgQ7pv-cvg',
            'https://www.youtube.com/watch?v=sCFmzGknUew',
            'https://www.youtube.com/watch?v=x4SjmWJb5_A',
            'https://www.youtube.com/watch?v=Q7dV48cI19M',
            'https://www.youtube.com/watch?v=sCzsQECINMw',
            'https://www.youtube.com/watch?v=kH0idBZQP1g',
            'https://www.youtube.com/watch?v=infTiRNtSps',
            'https://www.youtube.com/watch?v=HNXNopodS6E',
            'https://www.youtube.com/watch?v=jBTglY83D_U',
            'https://www.youtube.com/watch?v=VIvIhWjS4f8',
            'https://www.youtube.com/watch?v=L33zlFBiXLk'
            ]


    for i in range(0, len(urls)):
        full_url = urls[i]
        video_id = full_url.split("=")[1]
        url_video = "https://www.youtube.com/oembed?url=" + full_url +"&format=json"
        url_comments = "https://www.googleapis.com/youtube/v3/commentThreads?key=" + key + "&textFormat=plainText&part=snippet&videoId=" + video_id  +"&maxResults=100"

        try:
            r1=requests.get(url_video)
            name = json.loads(r1.text)['title']
            print(str(name))
            r2=requests.get(url_comments)

            write_to_file(name + "_info", r1.text)
            write_to_file(name + "_comments", r2.text)
            convert_to_csv(name + "_info", r1.text)
            convert_to_csv(name + "_comments", r2.text)

        except Exception as e:
            print("finished" + str(e))

'''
Writes text to file of specified name
'''
def write_to_file(f_name, text):
    with open(folder_name + "/" + f_name + ".json", "w",
              encoding="utf-8") as out:  # "/"+ url.split("/")[len(url.split("/"))-1].replace("-","_")
        out.write(text)
        print(text)

'''
Converts json file to CSV
'''
def convert_to_csv(f_name, json_file):

    outputDir = folder_name + "/" + f_name + ".csv"

    data = json.loads(json_file)

    df = pandas.io.json.json_normalize(data)

    df.to_csv(outputDir)
    print(df)


download_from_youtube()