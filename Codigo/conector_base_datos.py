# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 12:35:49 2022

@author: Dell 3000
"""

import configparser

import sqlite3
from sqlite3 import Error

class Controlador():    
    config = configparser.ConfigParser()
    config.read(r'config.ini')
    ruta_base = config['BaseDatos']['ruta_base']
    
    def __init__(self):        
        self.sql_connection()
        
    def sql_connection(self):
        try:
            con = sqlite3.connect(self.ruta_base+'tweets.db')
            self.con = con
        except Error:
            print(Error)
            
    def insertar_tweets(self, tweet):
        try:
            if not  self.valida_tweet_id(tweet['tweet_id']):
                self.sql_connection()
                cursorObj = self.con.cursor()    
                #fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursorObj.execute(f"""INSERT INTO tweets(palabra_clave,created_at,full_text,link_tweet,retweet_count,retweeted,source,tweet_id,user_created_at,user_id,user_name,user_screen_name)
                                  VALUES('{tweet['palabra_clave']}', '{tweet['created_at']}', '{tweet['full_text']}', '{tweet['link_tweet']}', '{tweet['retweet_count']}', '{tweet['retweeted']}', '{tweet['source']}', '{tweet['tweet_id']}', '{tweet['user_created_at']}', '{tweet['user_id']}', '{tweet['user_name']}', '{tweet['user_screen_name']}')""")
                self.con.commit()
                self.con.close()
        except Exception as error:
            self.con.close()
            print(error)

    def valida_tweet_id(self, tweet_id):
        try:
            self.sql_connection()
            cursorObj = self.con.cursor()
            cursorObj.execute(f"SELECT tweet_id FROM tweets where tweet_id='{tweet_id}'")
            rows = cursorObj.fetchall()
            self.con.close()
            return True if len(rows)>0 else False
        except Exception as error:
            self.con.close()
            print(error)            
            
#objdb = Controlador()

#objdb.sql_connection()

#objdb.insertar_tweets(data)
