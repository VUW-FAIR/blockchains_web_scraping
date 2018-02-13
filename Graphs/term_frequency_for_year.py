import collections
import csv
import glob
from operator import itemgetter
from collections import Counter
import matplotlib.pyplot as plt
import sys
from dateutil.parser import parse

unwanted_chars = ".,-_\n"

## SET YOU YEAR HERE:
year = 2018

def main():

    total_freq = {}
    dates = []
    csv_text = ""

    for file in glob.glob("forumbitcoincom/*.csv"):
        print(file)
        with open(file, encoding="utf8") as f:
            reader = csv.reader(x.replace('\0', '') for x in f)
            #csv_list = list(reader)

            for row in reader:

                try:
                    print(row[2])
                    b = parse(row[2])
                    print(b)
                    dates.append(b.date())  # only take the date (not datetime as we don't need the time)

                    if(b.date().year == year):
                        if (len(row) > 0):
                            #print(row[3])
                            csv_text += " " + row[3]

                except:
                    print("couldn't parse date")

        #print(csv_list)

    text = csv_text

    occurrences = countOccurrences(text)
    number_of_words = occurrences[1]

    total_freq.update(occurrences[0])
    print(total_freq)

    TF = {}
    for key, value in total_freq.items():
        TF[key] = value/number_of_words

    print(TF)

    ordered_total = collections.OrderedDict(sorted(total_freq.items(), key=itemgetter(1), reverse=True))
    sorted_top = {}
    print(ordered_total)
    i = 0
    for key, value in ordered_total.items():
        print(key, value)
        sorted_top[key] = value
        i+=1
        #CHOOSE THE NUMBER OF WORDS YOU WANT HERE:
        if i > 100:
            break

    plotGraph(sorted_top)


def countOccurrences(text):
    words = text.split()
    freq = {}

    count = 0
    for word in words:
        word = word.strip(unwanted_chars)
        #print(word)
        if word not in freq:
            freq[word] = 0
        freq[word] += 1
        count = count + 1
    #print(freq)

    return [freq, count]


def plotGraph(dict):
    plt.bar(range(len(dict)), dict.values(), align='center')
    plt.xticks(range(len(dict)), dict.keys(), rotation=90)

    plt.xlabel('word')
    plt.ylabel('number of occurrences')
    plt.title('Occurrences for words on forumbitcoincom: \n' + str(year))
    #plt.savefig( str(year) + ".png")
    plt.show()


main()