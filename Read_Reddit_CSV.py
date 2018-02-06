import os
import pandas as pd
import csv

'''
This script goes through a reddit CSV file and searches based on particular subreddit terms.
It then extracts the particular subreddit posts into a new CSV file. This is meant to be used in 
conjunction with the json to csv reddit converter which takes the json reddit file and makes it 
into a flattened CSV. 
'''

def main():
    terms = ['bitcoin', 'bigcoinbeginners', 'bitcoinmarkets', 'jobs4bitcoins', 'cryptocurrency', 'iota', 'darknetmarkets',
             'dogecoin', 'btc', 'litecoin', 'reddcoin', 'ripple', 'cardano', 'stratisplatform', 'siacoin', 'golemproject',
             'dashpay', 'icocrypto', 'fastcoin', 'litecointraders'
             'cryptomarkets', 'altcoin',  'bitcoinmining', 'btc', 'bitcoinxt', 'ethereum', 'ethtrader', 'ethermining', 'ethdev']

    dir = "/home/STUDENT/kumardyla/2013"
    for file in os.listdir(dir):
        if file.endswith(".csv"):
            print(os.path.join(dir, file))
            read_file_and_output_sorted(terms, file)

def read_file_and_output_sorted(terms, filename):

    #reading in chunks in order to not overwhelm system
    chunksize = 10 ** 6
    try:

        w = open('converted_' + filename, 'a', encoding='utf-8', newline="")  # a
        out = csv.writer(w)

        for input in pd.read_csv(filename, chunksize=chunksize):

            l = []
            for i in range(0, len(input)):
                for term in terms:
                    if((str(input.subreddit[i])).lower() == (str(term)).lower()):
                        print(input.loc[i])
                        l.append(input.loc[i])
                        out.writerow(input.loc[i])

    except Exception as e:
        print(e)

main()
