# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 09:30:50 2017

@author: Sachin Bommale
"""
#twitter API
import tweepy
#to get start and end date
import datetime
#xlsx file writer
import xlsxwriter
import sys

# credentials from https://apps.twitter.com/
consumerKey = "nsNk9wYUdKQapcqamMc9D2gVb"
consumerSecret = "gcZbhqu40aBLNuzsa6wHEvrDYjDBUca0cpBF4OPp04kZlc1o2F"
accessToken = "621881521-AvSfiOMTnpml6AYSzVtTueSGgChnDOPqK9v9aAIu"
accessTokenSecret = "WzSeoxb00HBmEUJ2dy0k779U7Ded7kRhzEngZ3BdrtSdN"

#for authentication of the twitter user
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

api = tweepy.API(auth)

username = sys.argv[0]
#start and end date of tweets
startDate = datetime.datetime(2017, 1, 12, 0, 0, 0)
endDate =   datetime.datetime(2017, 2, 10, 0, 0, 0)

tweets = []
#Write the keyword to tweets
query= "Minecraft"
#tweepy api searches tweets related to query
tmpTweets = api.search(q=query)
for tweet in tmpTweets:
    #get the tweets between start and end date
    if tweet.created_at < endDate and tweet.created_at > startDate:
        tweets.append(tweet)

while (tmpTweets[-1].created_at > startDate):
    print("Last Tweet @", tmpTweets[-1].created_at, " - fetching some more")
    tmpTweets = api.search(q=query)
    for tweet in tmpTweets:
        if tweet.created_at < endDate and tweet.created_at > startDate:
            tweets.append(tweet)

workbook = xlsxwriter.Workbook(query + ".xlsx")
worksheet = workbook.add_worksheet()
row = 0
for tweet in tweets:
    worksheet.write_string(row, 0, str(tweet.id))
    worksheet.write_string(row, 1, str(tweet.created_at))
    worksheet.write(row, 2, tweet.text)
    worksheet.write_string(row, 3, str(tweet.in_reply_to_status_id))
    row += 1

workbook.close()
print("Excel file ready")