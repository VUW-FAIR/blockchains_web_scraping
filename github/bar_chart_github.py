import numpy as np
import matplotlib.pyplot as plt
import json
import os
import time


rootdir = '.\GitHubScraping'
number_of_commits = {}

'''
Iterates over all files in directory and outputs number of commits (from json file)
as a bar chart. This uses file structure from the github API scraper. 
'''
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        dir_to_file = os.path.join(subdir, file)
        print (dir_to_file)
        if "commits_at" in dir_to_file:
            data = json.load(open(dir_to_file))
            string_in_slashes = dir_to_file.split('\\')[2].strip()
            print(string_in_slashes)
            commit_amount = 0
            if number_of_commits.get(string_in_slashes) is not None:
                commit_amount = number_of_commits.get(string_in_slashes)
                print(commit_amount)
            number_of_commits.update({string_in_slashes: commit_amount + len(data)})


plt.bar(range(len(number_of_commits)), number_of_commits.values(), align='center')
plt.xticks(range(len(number_of_commits)), number_of_commits.keys())

plt.show()
