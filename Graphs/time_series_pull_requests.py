import json
from datetime import datetime
import matplotlib.pyplot as plt
from glob import glob
from collections import Counter


'''
Time series for Github pull requests
'''
dates = []
for f_name in glob('.\\pull_requests\\*.json'):
    print(f_name)
    data = json.loads(open(f_name).read())
    for d in data:
        print(d['created_at'][:10])
        dates.append(d['created_at'][:10])


dates.sort()
dates_dict = Counter(dates)
print(dates_dict)

dates1 = []
for d in dates_dict.keys():
    dates1.append(datetime.strptime(d, "%Y-%m-%d"))
print(dates1)

plt.plot_date(dates1, dates_dict.values(), "-") #, '-'

plt.xlabel('Time')
plt.ylabel('Number of pull requests')
plt.title('Github Bitcoin pull requests\n')
plt.legend("pull requests")
plt.xticks(rotation=30)
plt.ylim(ymin=0) #not starting from 0, very odd
plt.show()


