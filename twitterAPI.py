#!/usr/bin/env python
# encoding: utf-8
import os
from glob import glob

import tweepy  # https://github.com/tweepy/tweepy
import csv

# Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""
folder_name = "tweets"

'''
Based on script written by Yanofsky at: https://gist.github.com/yanofsky/5436496
'''
def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    try:
        # make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name=screen_name, count=200)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        # keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            print ("getting tweets before %s" % (oldest))

            # all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

            # save most recent tweets
            alltweets.extend(new_tweets)

            # update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1

            print("...%s tweets downloaded so far" % (len(alltweets)))

        # transform the tweepy tweets into a 2D array that will populate the csv
        outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

        # write the csv
        with open('.\\' + folder_name + '\\' + '%s_tweets.csv' % screen_name, 'w', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "created_at", "text"])
            writer.writerows(outtweets)

        pass
    except Exception as exc:
        print(exc)


def main():

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    with open('cb.csv', encoding="utf8") as f:
        reader = csv.reader(x.replace('\0', '') for x in f)
        csv_list = list(reader)

    twitter_usernames = []
    for row in csv_list:
        print(row[11])
        if(len(row[11]) > 1):
            try:
                print(row[11].split('/')[3])
                twitter_usernames.append(row[11].split('/')[3])
            except Exception:
                print(Exception)
    #
    # twitter_usernames = ['_jonasschnelli_', 'markfriedenbach', 'TheBlueMatt', 'petertoddbtc', 'pwuille', 'orionwl', 'adam3us',
    #                      'TraceMayer', 'brian_armstrong', 'satoshilite', 'fehrsam', 'ericlarch', 'btchip', 'brianchoffman',
    #                      'chrispacia', 'samuelpatt', 'drwasho', 'aantonop', 'balajis', 'jamesgdangelo', 'TraceMayer', 'VitalikButerin'
    #                      'Zulfikar_Ramzan', 'DannyLScott', 'tonygallippi', 'rogerkver', 'jgarzik', 'petermkirby', 'gmaxwell', 'reggiemiddleton',
    #                      'colortwits', 'zooko', 'mperklin', 'jespow', 'etotheipi', 'erikvoorhees', 'boazeb', 'nvk', 'dochex']
    #
    for username in twitter_usernames:
        get_all_tweets(username)




if __name__ == '__main__':
    main()


