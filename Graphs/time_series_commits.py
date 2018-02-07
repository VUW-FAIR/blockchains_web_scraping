import json
from datetime import datetime
import matplotlib.pyplot as plt
from glob import glob
from collections import Counter


'''
Time series for Github commits
'''
dates = []
for f_name in glob('.\\commits\\*.json'):
    print(f_name)
    data = json.loads(open(f_name).read())
    for d in data:
        print(d['commit']['author']['date'][:10]) #.author.date']
        dates.append(d['commit']['author']['date'][:10])


dates.sort()
dates_dict = Counter(dates)
print(dates_dict)

dates1 = []
for d in dates_dict.keys():
    dates1.append(datetime.strptime(d, "%Y-%m-%d"))
print(dates1)

plt.plot_date(dates1, dates_dict.values(), "-") #, '-'



plt.xlabel('Time')
plt.ylabel('Number of commits')
plt.title('Github Bitcoin Commits\n')
plt.legend("commit num")
plt.xticks(rotation=30)
plt.show()

