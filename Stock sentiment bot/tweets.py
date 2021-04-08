from __future__ import division
import shutil
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import csv 
import os.path
import numpy as np
import pandas as pd
import tweepy as tw
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import nltk

log=pd.read_csv(r"C:\Users\voraa\Desktop\DATA SCIENCE\login.csv")

consumerKey=log['keys'][0]
consumerSecret=log['keys'][1]
accessToken=log['keys'][2]
accessTokenSecret=log['keys'][3]
authenticate=tw.OAuthHandler(consumerKey,consumerSecret) #creating authenticatio object
authenticate.set_access_token(accessToken,accessTokenSecret) #create access token secret
#create api
api=tw.API(authenticate,wait_on_rate_limit=True)

class twitter_analyze:

    def __init__(self):
        pass

            
    def analyze_feelings(self,stock):
        
        # tweets_file = 'data/%s_tweets.csv' %stock

        tweets = self.analyze_stock(stock)

        sentiment = []
        for index, row in tweets.iterrows():
            value = 0.0
            if isinstance(row['polarity'], float):
                value = round(row['polarity'], 3)
            else:
                x = float(row['polarity'])
                value = round(x, 3)
            if value < 0.0:
                sentiment.append('negative')
            elif value == 0.0:
                sentiment.append('neutral')
            else:
                sentiment.append('positive')

        tweets['sentiment'] = sentiment
        # tweets['sentiment'].value_counts().plot(kind='bar')
        # tweets['sentiment'].value_counts().plot(kind='pie')
        # plt.show()
        #print (tweets)
        counts_list = []
        pos=(tweets['sentiment'].value_counts()['positive'])
        neg=(tweets['sentiment'].value_counts()['negative'])
        neu=(tweets['sentiment'].value_counts()['neutral'])
        tot=pos+neg+neu
        ppos=round(((pos/tot)*100),2)
        pneg=round(((neg/tot)*100),2)
        pneu=round(((neu/tot)*100),2)
        data_string=' positive tweets: '+str(ppos)+'%'+'\n negative tweets: '+str(pneg)+'%'+'\n neutral tweets: '+str(pneu)+'%'
        counts_list.append(tweets['sentiment'].value_counts()['positive'])
        counts_list.append(tweets['sentiment'].value_counts()['negative'])
        counts_list.append(tweets['sentiment'].value_counts()['neutral'])
        cl=pd.Series(counts_list)            
        #plt.title("Sentiment analysis")
        #plt.xlabel("sentiment")
        #plt.ylabel("Count")
        #tweets['sentiment'].value_counts().plot(kind='bar')
        #plt.show()
            
        
        return data_string

    def analyze_stock(self, stock):
        all_tweets = self.get_tweets(stock)
        all_tweets=np.array(all_tweets['text'])
        tweets = pd.DataFrame()
        analysis_list = []
        polarity_list = []
        subjectivity_list = []
        tweet_text = []
        tweet_dates = []
        for tweet in range(len(all_tweets)):
            tweet_text.append(all_tweets[tweet])
            
            analysis = TextBlob(str(all_tweets[tweet]))
            # prints-Sentiment(polarity=0.0, subjectivity=0.0), polarity is how positive or negative, subjectivity is if opinion or fact
            # analysis_list.append('polarity:' + str(analysis.se 1ntiment.polarity) + ' subjectivity:' + str(analysis.sentiment.subjectivity))
            polarity_list.append(str(analysis.sentiment.polarity))
            subjectivity_list.append(str(analysis.sentiment.subjectivity))
           # tweet_dates.append(all_tweets[0].iloc[tweet])
        print(tweet_text)
        tweets['text'] = np.array(tweet_text)
        # tweets['analysis'] = np.array(analysis_list)
        tweets['polarity'] = np.array(polarity_list)
        tweets['subjectivity'] = np.array(subjectivity_list)
        #tweets['date'] = np.array(tweet_dates)
        # tweets = tweets.sort_values(by=['subjectivity'], ascending=0)
        #print (tweets)
        return tweets

    def get_tweets(self, stock):
        alltweets = []  
        public_tweets = api.search(stock)
        alltweets.extend(public_tweets)
        oldest = alltweets[-1].id - 1

        while len(public_tweets) > 0:
            #print ("getting tweets before %s" % (oldest))
            public_tweets = api.search(stock,count=200,max_id=oldest)
            
            alltweets.extend(public_tweets)
            
            oldest = alltweets[-1].id - 1
            
            #print ("...%s tweets downloaded so far" % (len(alltweets)))

            if len(alltweets) > 500:
                break

        #transform the tweepy tweets into a 2D array that will populate the csv 
        #outtweets = pd.DataFrame([[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in public_tweets])
        outtweets = pd.DataFrame([[tweet.id_str, tweet.created_at, tweet.text] for tweet in public_tweets])
        outtweets=outtweets.rename(columns={0:'id',1:'date',2:'text'})
        outtweets['text']=outtweets['text'].apply(self.clean_text)
        outtweets['text']=outtweets['text'].apply(self.tokenization)
        outtweets['text']=outtweets['text'].apply(self.remove_stopwords)
        outtweets['text']=outtweets['text'].apply(self.stemming)
        outtweets['text']=outtweets['text'].apply(self.lemmatizer)

        #outtweets[3]=outtweets[2].apply(lambda x: self.clean_text(x))
        #outtweets[3]=outtweets[3].apply(lambda x: self.tokenization(x))
        #outtweets[3]=outtweets[3].apply(lambda x: self.remove_stopwords(x))
        #outtweets[3]=outtweets[3].apply(lambda x: self.stemming(x))
        #outtweets[3]=outtweets[3].apply(lambda x: self.lemmatizer(x))
        #outtweets=outtweets.values.tolist()
        print(outtweets)
        return outtweets

    def clean_text(self,text):
          #text.decode('utf-8')
          text = re.sub(r'@[A-Za-z0-9_:]+','',text) #to remove @s
          text = re.sub(r'#','',text)#to remove #
          text = re.sub(r'RT[\s]+','',text) #remove retweets
          text = re.sub(r'http\S+', "", text,flags=re.MULTILINE)#remove any links and whitespeaces post that
  
          return text
        
    
    
    def remove_stopwords(self,text):
          stopword = nltk.corpus.stopwords.words('english')
          text = [word for word in text if word not in stopword]
          return text

    def tokenization(self,text):
          text.encode('utf-8')
          text = re.split('\W+', text)
          return text

 

    def stemming(self,text):
          ps = nltk.PorterStemmer()
          text = [ps.stem(word) for word in text]
          return text


    def lemmatizer(self,text):
          wn = nltk.WordNetLemmatizer()
          text = [wn.lemmatize(word) for word in text]
          return text

        
if __name__ == "__main__":
    analyze = twitter_analyze()
    #analyze.analyze_stock('$AAPL')
    print (analyze.analyze_feelings('HDFC'))
    #analyze.analyze_feelings('$AAPL')
    # analyze.analyze_feelings('$GOOGL')
