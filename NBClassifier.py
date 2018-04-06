# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 09:30:50 2017

@author: Sachin Bommale
"""
#to consider each tweet as regular expression
import re
#csv file reader
import csv
#to plot the graghs, charts in python
from matplotlib import pyplot as plt
#to classinfy tweets by using ML algorithms
import nltk.classify

#storing results to plot graph
eresult=['neutral','neutral','neutral','neutral','neutral',
         'positive','neutral','neutral','positive','neutral',
         'neutral','neutral','neutral','neutral','positive',
         'positive','neutral','positive','neutral','neutral',
         'neutral','negative','neutral','neutral','neutral',
         'neutral','neutral','neutral','positive','neutral',
         'neutral','neutral','neutral','neutral','neutral',
         'neutral','neutral','neutral','neutral','neutral',
         'neutral','neutral','neutral','neutral','neutral',
         'neutral','neutral','neutral','neutral','neutral',
         'neutral','neutral','positive','neutral','neutral',
         'neutral','neutral','neutral','neutral','positive',
         'positive','neutral','neutral','positive','neutral',
         'neutral','neutral','neutral','positive','positive']
result=[]
count=0
tcount=0
accuracy=0
epcount=0
pcount=0
encount=0
ncount=0
entcount=0
ntcount=0
#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL) 
    return pattern.sub(r"\1\1", s)

#start process_tweet
def processTweet(tweet):
    # process the tweets
    
    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)    
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet  


#start getStopWordList
def getStopWordList(stopWordListFileName):
    #read the stopwords
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords
#end

#start getfeatureVector
def getFeatureVector(tweet, stopWords):
    #feature words list
    featureVector = [] 
    #split each tweet
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences 
        w = replaceTwoOrMore(w) 
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if it consists of only words
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", w)
        #ignore if it is a stopWord
        if(w in stopWords or val is None):
            continue
        else:
            #append feature words in lower case latters
            featureVector.append(w.lower())
    return featureVector    


#start extract_features
def extract_features(tweet):
    tweet_words = set(tweet)
    #featurewords list
    features = {}
    for word in featureList:
        #extract the feature words
        features['contains(%s)' % word] = (word in tweet_words)
    return features
   

#Read the tweets one by one and process it
inpTweets = csv.reader(open('C:\\Users\\Sachin Bommale\\Desktop\\Algorithms\\mysenti\\datasets\\Train_Minecraft.csv', 'r',encoding='utf8'), delimiter=',',quotechar="|")
stopWords = getStopWordList('C:\\Users\\Sachin Bommale\\Desktop\\Algorithms\\mysenti\\Feature_extractor\\stopwords.txt')
count = 0;
featureList = []
tweets = []
for row in inpTweets:
    #assign row[0] of tweets data to sentiment
    sentiment = row[0]
    #assign row[1] of tweets data to actual tweets
    tweet = row[1]
    #print(tweet)
    #processing of tweets
    processedTweet = processTweet(tweet)
    #print(processedTweet)
    #getting feature vector from processed tweets and stopwords
    featureVector = getFeatureVector(processedTweet, stopWords)
    #print(featureVector)
    featureList.extend(featureVector)
    #appending feature vector and sentiment to tweets list
    tweets.append((featureVector, sentiment))
    #print(tweets)


# Remove featureList duplicates
featureList = list(set(featureList))
#print(featureList)

# Generate the training set
training_set = nltk.classify.util.apply_features(extract_features, tweets)

#Train the Naive Bayes classifier
NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

# Test the classifier
#open the input tweets which are in csv format
inputTweets = csv.reader(open('C:\\Users\\Sachin Bommale\\Desktop\\Algorithms\\mysenti\\datasets\\Test_Minecraft.csv', 'r',encoding='utf8'), delimiter=',',quotechar='|')
#for each line(row) in input Tweets
for line in inputTweets:
    testTweet=line
    #processing of Tweets
    processedTestTweet = processTweet(testTweet[0])
    #print(processedTestTweet)
    #findout sentiment by classifying tweets using NBClassifier
    sentiment = NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet, stopWords)))
    result.append(sentiment)
    #print testing tweets and related sentiment value
    print ("TESTING TWEET = %s\nRelated SENTIMENT = %s\n" % (processedTestTweet, sentiment))

#count the length of expected result
ecount=len(eresult)
for i in range(ecount):
    #compare if expected sentiment matches with resulting sentiment
    if(result[i]==eresult[i]):
        #if matches increment the count by 1
        count=count+1
        
#calculating accuracy by using (resulting count / total expected count)*100
accuracy=(count/ecount)*100

#print the accuracy of tweets 
print("The accuracy of the algorithm is",accuracy)
#for all tweets in expected result
for i in range(len(eresult)):
    #check if expected result is positive
    if eresult[i]=='positive':
        #increment count by 1
        epcount=epcount+1
    #check if expected result is negative
    elif eresult[i]=='negative':
        #increment count by 1
        encount=encount+1
    else:
        #increment neutral count by 1
        entcount=entcount+1
#for all tweets in result(outcome)
for i in range(len(result)):
    #check if expected result is positive
    if result[i]=='positive':
         #increment count by 1
        pcount=pcount+1
    #check if expected result is negative
    elif result[i]=='negative':
         #increment count by 1
        ncount=ncount+1
    else:
        #increment neutral count by 1
        ntcount=ntcount+1
        

left = [1, 2]
#hieght as expected positive count and resulting positive count 
height = [epcount, pcount]
#labels of bar chart
tick_label = ['Expected', 'Outcome']
#plot bar chart with 0.5 width and colored as expected positive count red and resulting positive count blue
plt.bar(left, height, tick_label = tick_label,width = 0.5, color = ['red', 'blue'])
#assign x label and y label
plt.xlabel('')
plt.ylabel('count')
#tittle of chart
plt.title('Positive tweets')
#shows the bar chart
plt.show()

#hieght as expected negative count and resulting negative count 
height = [encount, ncount]
#labels of bar chart
tick_label = ['Expected', 'Outcome']
#plot bar chart with 0.5 width and colored as expected positive count red and resulting positive count blue
plt.bar(left, height, tick_label = tick_label,width = 0.5, color = ['red', 'blue'])
#assign x label and y label
plt.xlabel('')
plt.ylabel('count')
#tittle of chart
plt.title('Negative tweets')
#shows the bar chart
plt.show()

#hieght as expected neutral count and resulting neutral count
height = [entcount, ntcount]
#labels of bar chart
tick_label = ['Expected', 'Outcome']
#plot bar chart with 0.5 width and colored as expected positive count red and resulting positive count blue
plt.bar(left, height, tick_label = tick_label,width = 0.5, color = ['red', 'blue'])
#assign x label and y label
plt.xlabel('')
plt.ylabel('count')
#tittle of chart
plt.title('Neutral tweets')
#shows the bar chart
plt.show()