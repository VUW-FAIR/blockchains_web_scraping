import json
from datetime import datetime, date
import matplotlib.pyplot as plt
from glob import glob
from collections import Counter
import csv
from dateutil.parser import parse

'''
Time series for tweets from twitter
'''

dates = []
for f_name in glob('.\\twitter\\*.csv'):
    # print(f_name)
    with open(f_name, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            try:
                b = parse(row[1])
                print(b)
                dates.append(b.date())  # only take the date (not datetime as we don't need the time)
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
plt.ylabel('Number of tweets')
plt.title('Tweets from cryptocurrency related Twitter accounts\n')
plt.legend("Number")
plt.xticks(rotation=30)
plt.show()

