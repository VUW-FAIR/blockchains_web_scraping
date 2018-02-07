import json
from datetime import datetime
import matplotlib.pyplot as plt
from glob import glob
from collections import Counter
import csv
from dateutil.parser import parse

'''
For eth forum at website: http://bitcoingarden.org/forum/
'''

dates = []
for f_name in glob('.\\btcgarden\\*.csv'):
    # print(f_name)
    with open(f_name, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(x.replace('\0', '') for x in csvfile)
        for row in csvreader:
            if(len(row) > 3):
                if(len(row[3]) > 1): #aka not empty string for date
                    print((row[3])[:-1])
                    try:
                        b = parse((row[3])[:-1])
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
plt.title('http://bitcoingarden.org/forum/ post time series\n')
plt.legend("Number")
plt.xticks(rotation=30)
plt.show()

