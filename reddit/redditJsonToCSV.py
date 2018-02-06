import os
import pandas
from pandas.io.json import json_normalize
import json

'''
Based on file structure of reddit torrent. 
Goes over files and converts them to CSVs
'''

# def json_to_csv():
#     rootdir = '.\\reddit_data'
#
#     newpath = r'.\\' + "reddit_data_csv"
#     if not os.path.exists(newpath):
#         print("making dir")
#         os.makedirs(newpath)
#
#     for subdir, dirs, files in os.walk(rootdir):
#         for file in files:
#             dir_to_file = os.path.join(subdir, file)
#             print(dir_to_file)
#             output = ".\\reddit_data_csv\\" + (dir_to_file.split('\\')[3].strip()[0:-5]) + ".csv"
#             convert_to_csv(dir_to_file, output)

def convert_to_csv(filepath, output):
    data = []
    try:
        with open(filepath, "r") as f:
            for line in f:
                data.append(json.loads(line, encoding="utf-8"))
            df = pandas.io.json.json_normalize(data)
        df.to_csv(output)
    except:
        print("could not convert")
def main():
    dir = "/mnt/res/Dylan\ Kumar/torrents/reddit_data/2012"
    for file in os.listdir(dir):
        if file.endswith(""):
            print(os.path.join(dir, file))
            convert_to_csv(os.path.join(dir, file), os.path.join(dir, file))

main()
