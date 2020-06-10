
from flask import Flask,request,jsonify
import tweepy
from textblob import TextBlob 
import re

app = Flask(__name__)
def clean_tweet(tweet): 
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|(_[A-Za-z0-9]+)|(&[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

@app.route('/')
def home():
    consumer_key = 'GujYFuaLVvmLYQH7tBbFM43ZX'
    consumer_secret = 'YCimJhchoxTDJwjHcATZADsGrSStP0kMsVOlSUsUMm45ERolTz'
    access_token = '1216916794671108096-hwDO1jHSbbN9VpEjP1TuHygvjV4WPq'
    access_token_secret = 'TJDlpMFNpx93sw1KiDa3EC7jN0adVT1JOwqpkglzIQgEb'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    tweets = api.search('BJP -filter:retweets', result_type="recent", lang="en",tweet_mode="extended",count=100)
    data=[clean_tweet(tweet.full_text) for tweet in tweets]
    pos=0
    neg=0
    neu=0
    
    for tweet in data:
        analysis = TextBlob(tweet)
        if analysis.sentiment.polarity > 0: 
            pos=pos+1
        elif analysis.sentiment.polarity == 0: 
            neg=neg+1
        else: 
            neu=neu+1
    overall=''
    if pos>neg:
        if pos>neu:
            overall='positive'
    else:
        if neg>neu:
            overall='negative'
        else:
            overall='neutral'
    return jsonify({"overall":overall,
                    "tweets":data})

# POST
@app.route('/api/post_some_data', methods=['POST'])
def get_text_prediction():
    json = request.get_json()
    topic=json['topic']
    no_of_tweets=json['no']
    no_of_tweets=int(no_of_tweets)
    if no_of_tweets<0 or no_of_tweets>100:
        return jsonify({"test":1}) #limit error
    else:
        consumer_key = 'GujYFuaLVvmLYQH7tBbFM43ZX'
        consumer_secret = 'YCimJhchoxTDJwjHcATZADsGrSStP0kMsVOlSUsUMm45ERolTz'
        access_token = '1216916794671108096-hwDO1jHSbbN9VpEjP1TuHygvjV4WPq'
        access_token_secret = 'TJDlpMFNpx93sw1KiDa3EC7jN0adVT1JOwqpkglzIQgEb'
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
    
        api = tweepy.API(auth)
        search=topic+' -filter:retweets'
        tweets = api.search(search, result_type="mixed", lang="en",tweet_mode="extended",count=no_of_tweets)
        if len(tweets)==no_of_tweets:
            data=[clean_tweet(tweet.full_text) for tweet in tweets]
            pos=[]
            neg=[]
            neu=[]
            pos_pol=0
            neg_pol=0
            neu_pol=0
            pos_urls=[]
            neg_urls=[]
            neu_urls=[]
            pos_likes=[]
            neg_likes=[]
            neu_likes=[]
            pos_retweets=[]
            neg_retweets=[]
            neu_retweets=[]
            
            
            i=0

            for tweet in data:
                analysis = TextBlob(tweet)
                if analysis.sentiment.polarity > 0: 
                    pos_pol=pos_pol+analysis.sentiment.polarity
                    pos.append(tweets[i])
                    pos_urls.append(f"https://twitter.com/user/status/{tweets[i].id}")
                    pos_likes.append(str(tweets[i].favorite_count))
                    pos_retweets.append(str(tweets[i].retweet_count))
                elif analysis.sentiment.polarity == 0: 
                    neu_pol=neu_pol+analysis.sentiment.polarity
                    neu.append(tweets[i])
                    neu_urls.append(f"https://twitter.com/user/status/{tweets[i].id}")
                    neu_likes.append(str(tweets[i].favorite_count))
                    neu_retweets.append(str(tweets[i].retweet_count))
                else: 
                    neg_pol=neg_pol+analysis.sentiment.polarity
                    neg.append(tweets[i])
                    neg_urls.append(f"https://twitter.com/user/status/{tweets[i].id}")
                    neg_likes.append(str(tweets[i].favorite_count))
                    neg_retweets.append(str(tweets[i].retweet_count))
                i+=1
            overall=''
            pos_per=int((len(pos)/no_of_tweets)*100)
            neg_per=int((len(neg)/no_of_tweets)*100)
            neu_per=int((len(neu)/no_of_tweets)*100)
            c=max([pos_per,neg_per,neu_per])
            if c==pos_per:
                overall='POSITIVE'
            elif c==neg_per:
                overall='NEGATIVE'
            else:
                overall='NEUTRAL'
            if (c==pos_per and pos_per==neg_per):
                if pos_pol> (0-neg_pol):
                    overall='POSITIVE'
                    
                else:
                    overall='NEGATIVE'
            elif c==pos_per and pos_per == neu_per:
                overall='TIE between POS & NEU'
            elif c==neg_per and neg_per == neu_per:
                overall='TIE between NEG & NEU'
                
            
            if (pos_per+neg_per+neu_per)!=100:
                if pos_per==33 and neg_per==33 and neu_per==33:
                    overall='TIE between POS, NEG & NEU'
                    neu_per+=0.33
                    if pos_pol> (0-neg_pol):
                        pos_per+=0.34
                        neg_per+=0.33
                    else:
                        neg_per+=0.34
                        pos_per+=0.33
                        
                    
                elif pos_per==neu_per:
                    pos_per+=0.5
                    neu_per+=0.5
                    if c==pos_per:
                        overall='TIE between POS & NEU'
                        
                elif neg_per==neu_per:
                    
                    neg_per+=0.5
                    neu_per+=0.5
                    if c==neg_per:
                        overall='TIE between NEG & NEU'
                elif pos_per==neg_per:
                    
            
                    if pos_pol> (0-neg_pol):
                        overall='POSITIVE'
                        pos_per+=1
                    else:
                        overall='NEGATIVE'
                        neg_per+=1
                else:
                    if overall=='POSITIVE':
                        pos_per+=1
                    elif overall=='NEGATIVE':
                        neg_per+=1
                    else:
                        neu_per+=1
                        
                
            

            return jsonify({"test":0,
                            "no_of_tweets":no_of_tweets,
                            "overall":overall,
                            "search":topic,
                            "pos_tweets":{"no of tweets":len(pos),
                                          "percentage":str(pos_per),
                                          "urls":pos_urls,
                                          "tweets":[tweet.full_text for tweet in pos],
                                          "likes":pos_likes,
                                          "retweets":pos_retweets,
                                          "polarity":pos_pol
                                          },
                            "neg_tweets":{"no of tweets":len(neg),
                                          "percentage":str(neg_per),
                                          "urls":neg_urls,
                                          "tweets":[tweet.full_text for tweet in neg],
                                          "likes":neg_likes,
                                          "retweets":neg_retweets,
                                          "polarity":neg_pol
                                          },
                            "neu_tweets":{"no of tweets":len(neu),
                                          "percentage":str(neu_per),
                                          "urls":neu_urls,
                                          "tweets":[tweet.full_text for tweet in neu],
                                          "likes":neu_likes,
                                          "retweets":neu_retweets
                                          }})
            
        else:
            return jsonify({"test":2,
                            "search topic":topic,
                            "search operator":search,
                            "number of tweets":len(tweets)}) #topic error
            
    
    

if __name__ == "__main__":
    app.run(debug=True)
