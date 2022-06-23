# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 16:15:09 2022

@author: Dell 3000
"""

import configparser
import tweepy
from pysentimiento import create_analyzer
from pysentimiento.preprocessing import preprocess_tweet

import conector_base_datos as obdc

objdb = obdc.Controlador()
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

palabras_clave = config['twitter']['palabras_clave']


def obtiene_tweets():
    search_term = [palabras_clave]   
    tweets = []
    for tweet in tweepy.Cursor(api.search_tweets,
                           q=search_term,
                           tweet_mode="extended",
                           #since='2017-02-16', until='2017-02-17',
                           count=10,
                           #result_type='recent',
                           #include_entities=True,
                           #monitor_rate_limit=True, 
                           #wait_on_rate_limit=True,
                           lang="es"
                           ).items(30):
        data = {}
        data['palabra_clave'] = palabras_clave
        data['tweet_id'] = tweet.id
        data['created_at'] = tweet.created_at
        data['full_text'] = tweet.full_text
        data['retweeted'] = tweet.retweeted
        data['retweet_count'] = tweet.retweet_count
        try:        
            data['full_text'] = tweet.retweeted_status.full_text
        except AttributeError:  # Not a Retweet        
            data['full_text'] = tweet.full_text
        data['source'] = tweet.source        
            
        data['user_id'] = tweet.user.id
        data['user_created_at'] = tweet.user.created_at
        data['user_screen_name'] = tweet.user.screen_name
        data['user_name'] = tweet.user.name
        data['link_tweet'] = f'https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}'
        #tweets.append(data)
        objdb.insertar_tweets(data)
        
        #print(tweet.full_text)
        #print(tweet.created_at)    
        #print(tweet.user.id)
        #print(tweet.user.created_at)
        #print(tweet.user.screen_name)
        #print(tweet.user.name)
        #print('\n\n')
    
if __name__ == '__main__':
    
    analyzer = create_analyzer(task="sentiment", lang="es")
    cadena = """Es culiosa la afición de Cristiano Ronaldo a palticipar en plomociones de timos y estafas. Desde que te aluines al póker como a tilar tu dinero en el casino online

                     Lo único que le faltaba era timar a sus seguidoles con los NFT. Ahora con #Binance ya tiene el sueño cumplido"""
    cadena = preprocess_tweet(cadena, lang="es")
    sentimiento = analyzer.predict(cadena)
    print(sentimiento.probas)
    print(sentimiento.output)




        
# public_tweets = api.search_tweets(q=['CAPG_HACK3', 'CAPG_NO_HACK3'], count=5)

# for tweet in public_tweets:
#     print(tweet.text)
#     print(tweet.created_at)
#     print(tweet.user.id)
#     print(tweet.user.created_at)
#     print(tweet.user.screen_name)
#     print(tweet.user.name)
