import os
import pandas
from pandas.io.json import json_normalize
import json

'''
Make new subdirectory of specified name
'''
def make_dir(name):
    newpath = r'.\\' + "json_to_csv" + '\\' + name
    if not os.path.exists(newpath):
        print("making dir")
        os.makedirs(newpath)

'''
Takes your root directory for github folder (after being parsed by github scraper to json)
and converts json files to csv of new folders of same structure. 
'''
def json_to_csv():
    rootdir = '.\GitHubScraping'

    for subdir, dirs, files in os.walk(rootdir):
        # print(str(subdir))
        for file in files:
            # print(file)
            dir_to_file = os.path.join(subdir, file)
            print(dir_to_file)
            userName = dir_to_file.split('\\')[2].strip()
            repoName = dir_to_file.split('\\')[3].strip()
            typeName = dir_to_file.split('\\')[4].strip()
            path = userName + "\\" + repoName + "\\" + typeName
            print((dir_to_file.split('\\')[5].strip())[0:-5])
            make_dir(path)
            convert_to_csv(dir_to_file, '.\\' + "json_to_csv" + '\\' + path + '\\' + str((dir_to_file.split('\\')[5].strip())[0:-5]) + ".csv")
            print(userName)


'''
Converts your json file to to CSV.
Normalizes data and then saves in output directory.
'''
def convert_to_csv(inputDir, outputDir):
    with open(inputDir, 'r', encoding="utf-8") as json_file:
        data = json.load(json_file)

    df = pandas.io.json.json_normalize(data)

    df.to_csv(outputDir)
    print(df)

'''
Joins multiple CSV files together (of same structure)
by finding all files of subdirectory and appending them
to one file.
'''
def join_files_together():
    rootdir = '.\json_to_csv'
    for subdir, dirs, files in os.walk(rootdir):
        print(str(subdir))
        print((subdir.split('\\')))
        if(len(subdir.split('\\')) > 4):
            with open(subdir + "\\" + subdir.split('\\')[4].strip() + "_combined_.csv", 'a', encoding="utf8") as fout:
                for i in range (0, len(files)):
                    if(i == 0):
                        for line in open(subdir + "\\" + files[i], encoding="utf8"):
                            fout.write(line)
                    else:
                        f = open(subdir + "\\" + files[i], encoding="utf8")
                        next(f) #skipping the header
                        for line in f:
                            fout.write(line)

json_to_csv()
join_files_together()
