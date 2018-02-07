import json
from datetime import datetime
import matplotlib.pyplot as plt
from glob import glob
from collections import Counter
import csv
from dateutil.parser import parse

'''
For Forumbitcoincom at website: https://forum.bitcoin.com/
'''

dates = []
for f_name in glob('.\\forumbitcoincom\\*.csv'):
    # print(f_name)
    with open(f_name, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if(len(row) > 3):
                if(len(row[2]) > 1): #aka not empty string for date
                    print(row[2])
                    try:
                        b = parse(row[2])
                        print(b)
                        dates.append(b.date()) #only take the date (not datetime as we don't need the time)
                    except:
                        print("couldn't parse date")


dates.sort()
dates_dict = Counter(dates)
print(dates_dict)

dates1 = []
for d in dates_dict.keys():
    dates1.append(d)
print(dates1)

plt.plot_date(dates1, dates_dict.values(), "-") #, '-'


plt.xlabel('Time')
plt.ylabel('Number of posts/comments/replies etc')
plt.title('https://forum.bitcoin.com/ post time series\n')
plt.legend("Number")
plt.xticks(rotation=30)
plt.show()

