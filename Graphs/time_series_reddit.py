import json
from datetime import datetime, date
import matplotlib.pyplot as plt
from glob import glob
from collections import Counter
import csv
from dateutil.parser import parse

'''
Time series for reddit posts
'''

dates = []
for f_name in glob('.\\reddit\\*.csv'):
    # print(f_name)
    with open(f_name, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            try:

                b = datetime.fromtimestamp(int(row[7])).strftime('%Y-%m-%d') #Add this for time as well as day: %H:%M:%S
                print(b)
                dates.append(b)  # only take the date (not datetime as we don't need the time)
            except Exception as e:
                print("couldn't parse date" )
                print(e)

dates.sort()
dates_dict = Counter(dates)
print(dates_dict)

dates1 = []
for d in dates_dict.keys():
    dates1.append(d)
print(dates1)

plt.plot_date(dates1, dates_dict.values(), "-") #, '-'



plt.xlabel('Time')
plt.ylabel('Number of reddit posts/comments/replies etc')
plt.title('Reddit posts time series for cryptocurrency subreddits, e.g. bitcoin\n')
plt.legend("Number")
plt.xticks(rotation=30)
plt.show()

