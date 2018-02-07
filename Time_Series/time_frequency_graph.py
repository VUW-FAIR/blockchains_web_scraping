import collections
import csv
import glob
from operator import itemgetter

import matplotlib.pyplot as plt
import sys

unwanted_chars = ".,-_\n"

def main():

    total_freq = {}

    csv_text = ""

    for file in glob.glob("csv_files/*.csv"):
        print(file)
        with open(file, encoding="utf8") as f:
            reader = csv.reader(x.replace('\0', '') for x in f)
            csv_list = list(reader)
        print(csv_list)

        for elements in csv_list:
            if(len(elements) > 0):
                print(elements[2])
                csv_text += " " + elements[2]

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
        if i > 20:
            break


    plotGraph(sorted_top)


def countOccurrences(text):
    words = text.split()
    freq = {}

    count = 0
    for word in words:
        word = word.strip(unwanted_chars)
        print(word)
        if word not in freq:
            freq[word] = 0
        freq[word] += 1
        count = count + 1
    print(freq)

    return [freq, count]


def plotGraph(dict):
    plt.bar(range(len(dict)), dict.values(), align='center')
    plt.xticks(range(len(dict)), dict.keys(), rotation=30)

    plt.xlabel('username')
    plt.ylabel('number of comments/posts')
    plt.title('Top usernames Graph for Ethereum Forum\n')

    plt.show()

main()