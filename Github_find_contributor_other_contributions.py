import csv
import json
import os


contributors = {}

'''
This script goes over all the files in the github folder and finds which repos the contributor has contributed to. 
'''
def parse_contributors_page(name_of_repo, file_path):

    file = json.loads(open(file_path, encoding="utf-8").read())

    for c in file:
        try:
            print('a')
            print(c['login'])
            if (c['login']) in contributors: #if in the dictionary, aka already exists
                print('exists')
                print(contributors[c['login']])
                contributors[(c['login'])].append(name_of_repo)
            else:
                print('new')
                contributors[(c['login'])] = [name_of_repo] #add with one element in the list, initial set
        except Exception as ex:
            print(ex)
            print("no login/username on this line")
        print(contributors)


def iterate_through_folders():
    rootdir = '.\\GitHubScraping'

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            path = os.path.join(subdir).replace(str(os.path.join(subdir).split("\\", -1)[-1]), "")
            print(path)

            contibutor_path = path + "all_contributors\contributors_page_"
            if(contibutor_path in os.path.join(subdir, file)):
                print('a0')
                print(os.path.join(subdir, file))
                parse_contributors_page(name_of_repo=os.path.join(subdir, file), file_path=os.path.join(subdir, file))

    write_to_csv()


def write_to_csv():
    with open('github_contributors_output.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in contributors.items():
            writer.writerow([key, value])

iterate_through_folders()
