
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
    if no_of_tweets<0 or no_of_tweets>200:
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
            i=0

            for tweet in data:
                analysis = TextBlob(tweet)
                if analysis.sentiment.polarity > 0: 
                    pos_pol=pos_pol+analysis.sentiment.polarity
                    pos.append(tweets[i])
                    pos_urls.append(f"https://twitter.com/user/status/{tweets[i].id}")
                elif analysis.sentiment.polarity == 0: 
                    neu_pol=neu_pol+analysis.sentiment.polarity
                    neu.append(tweets[i])
                    neu_urls.append(f"https://twitter.com/user/status/{tweets[i].id}")
                else: 
                    neg_pol=neg_pol+analysis.sentiment.polarity
                    neg.append(tweets[i])
                    neg_urls.append(f"https://twitter.com/user/status/{tweets[i].id}")
                i+=1
            overall=''
            pos_per=int((len(pos)/no_of_tweets)*100)
            neg_per=int((len(neg)/no_of_tweets)*100)
            neu_per=int((len(neu)/no_of_tweets)*100)
            if (pos_per+neg_per+neu_per)!=100:
                if pos_per==neu_per:
                    overall='TIE between POS & NEU'
                    pos_per+=0.5
                    neu_per+=0.5
                elif neg_per==neu_per:
                    overall='TIE between NEG & NEU'
                    neg_per+=0.5
                    neu_per+=0.5
                else:
                    if pos_pol> (0-neg_pol):
                        overall='POSITIVE'
                    else:
                        overall='NEGATIVE'


            else:
                c=max([pos_per,neg_per,neu_per])
                if c==pos_per:
                    overall='POSITIVE'
                elif c==neg_per:
                    overall='NEGATIVE'
                else:
                    overall='NEUTRAL'
            

            return jsonify({"test":0,
                            "no_of_tweets":no_of_tweets,
                            "overall":overall,
                            "search":topic,
                            "pos":len(pos),
                            "neg":len(neg),
                            "neu":len(neu),
                            "pos%":pos_per,
                            "neg%":neg_per,
                            "neu%":neu_per,
                            "urls":{"pos":pos_urls,
                                    "neg":neg_urls,
                                    "neu":neu_urls
                                    },
                            "tweets":{"pos":[tweet.full_text for tweet in pos],
                                      "neg":[tweet.full_text for tweet in neg],
                                      "neu":[tweet.full_text for tweet in neu]
                                      }})
        else:
            return jsonify({"test":2}) #topic error
            
    
    

if __name__ == "__main__":
    app.run(debug=True)
