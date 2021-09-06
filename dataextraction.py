import requests
import json
from bs4 import BeautifulSoup
import re
import urllib.request
import os
from urllib.parse import urljoin
#import pandas as pd
import urllib3
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from googlesearch import search
import random
import psycopg2
from psycopg2.extras import LoggingConnection
# from datacollection import pdf_content 
# from datatagging import tagging 
# from datacollection import text_content
# from datatagging import score
# from datacollection import video_content
# from datacollection import code_snippet1
# from datacollection import code_snippet
from datacollection import Extraction
from datatagging import DataTag
import config as cfg
import logging
# query = input('Enter Your Query: ') #search query
# lang = input('Enter language ex:[en,fr,ar,jp,cn...]: ') #search language
# content_type = input('Enter your Format:[multi,pdf,videos,program or code,text,images...]:)

def readlogs():
        #Create and configure logger
    logging.basicConfig(level = logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s',filemode='a')
        # #Creating an object
    logger=logging.getLogger()
        # #Setting the threshold of logger to DEBUG
    db_settings = {
        "user": "postgres",
        "password": "aakashmak",
        "host": "localhost",
        "port":"5432",
        "database": "scraping_log",
    }
    conn = psycopg2.connect(connection_factory=LoggingConnection, **db_settings)
    conn.initialize(logger)
    cur = conn.cursor()
    cur.execute("SELECT * FROM audit_log")
    rows = cur.fetchall()
    arr =[]
    for i in rows:
        arr.append({'time':i[0],'message':i[1],'url':i[2]})
    return arr

class UrlExtract:
    def __init__(self, query,lang,content_type,search_engine,filename):
        self.content_type = content_type
        self.lang = lang
        self.query = query
        self.search_engine = search_engine
        self.filename = filename

    def google(self,content):
        #content =  what type of format whether it is pdf, videos, text, program
        my_dict=[]
        dict_temp={}
        url_ = cfg.url["search"].format(self.lang,self.query,content)#we get the language, query,content type for the url search
        headers = {'User-Agent': cfg.url["headers"]}#headers
        source=requests.get(url_, headers=headers).text # url source
        soup = BeautifulSoup(source, 'html.parser')
        search_div = soup.find_all(class_='yuRUbf') # find all divs tha contains search result
        for result in search_div:
            # loop result list
            print('title: %s'%result.h3.string) #geting h3 and printing the title for the specific url
            print('url: %s'%result.a.get('href')) #geting a.href and displaying the url 
            text = result.get_text()
            print(result.text)#getting the descrption for that url 
            print('\n')
            dict_temp['title']=result.h3.string
            dict_temp['url']=result.a.get('href')
            dict_temp['description']= result.text
            my_dict.append(dict_temp)
            dict_temp={}
        return my_dict

    def custom(self,content):
        #content =  what type of format whether it is pdf, videos, text, program
        # with open(self.filename)as outfile:
        urls = json.loads(self.filename)
        my_dict=[]
        dict_temp={}
        for a in urls:
            soup = BeautifulSoup(requests.get(a).text, 'html.parser')
            result = soup.title.string 
            result1 = soup.find_all('meta')
            try:
                result1 = [ meta.attrs['content'] for meta in result1 if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
            except Exception as e:
                try:
                    result1 = soup.select_one('meta[name ="description"][content]')['content']
                except Exception as e:
                    result1 = soup.title.string
            dict_temp['url']=a
            dict_temp['title']=result
            dict_temp['description']=result1
            my_dict.append(dict_temp)
            dict_temp={}
        return my_dict

    def bing(self,content):
    
        #content =  what type of format whether it is pdf, videos, text, program
        my_dict=[]
        dict_temp={}
        url_ = cfg.url["search_bing"].format(self.lang,self.query,content)#we get the language, query,content type for the url search
        headers = {'User-Agent': cfg.url["headers"]}#headers
        source=requests.get(url_, headers=headers).text # url source
        soup = BeautifulSoup(source, 'html.parser')
        search_div = soup.find_all('li',{"class":"b_algo"}) # find all divs tha contains search result

        for result in search_div: # loop result list
            print('title: %s'%result.h2.string) #geting h2 and printing the title for the specific url
            print('url: %s'%result.a.get('href')) #geting a.href and displaying the url 
            text = result.get_text()
            print(result.text)
            print('\n')
            dict_temp['title']=result.h2.string
            dict_temp['url']=result.a.get('href')
            dict_temp['description']= result.text
            my_dict.append(dict_temp)
            dict_temp={}
        return my_dict
    
    def duckduckgo(self,content):
        #content =  what type of format whether it is pdf, videos, text, program
        my_dict=[]
        dict_temp={}
        url_ = cfg.url["search_duckgo"].format(self.query,self.lang,content)#we get the language, query,content type for the url search
        headers = {'User-Agent': cfg.url["headers"]}#headers
        source=requests.get(url_, headers=headers).text # url source
        soup = BeautifulSoup(source, 'html.parser')
        search_div = soup.find_all('a',{'class':'result__a',},href=True) # find all divs tha contains search result
        for result in search_div: # loop result list
            text = result.get_text()
            print('title:%s'%result.text)# printing the title for the specific url
            # print('Title: %s'%result1) #geting h3 
            print('url: %s'%result['href']) #geting href and displaying the url 
            print('\n')
            dict_temp['title']=result.text
            dict_temp['url']=result['href']
            my_dict.append(dict_temp)
            dict_temp={}
        return my_dict
    
    def log(url):
        #Create and configure logger
        logging.basicConfig(level = logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s',filemode='a')
        #Creating an object
        logger=logging.getLogger()
        logging_level = logging.root.level
        logfile=''
        for urls in url:
            logfile = logfile+''+urls
        # print(logfile,type(logfile))
        #Setting the threshold of logger to DEBUG
        db_settings = {
            "user": "postgres",
            "password": "aakashmak",
            "host": "localhost",
            "port":"5432",
            "database": "scraping_log",
        }
        conn = psycopg2.connect(connection_factory=LoggingConnection, **db_settings)
        conn.initialize(logger)
        cur = conn.cursor()
        # cur.execute("SELECT * FROM public.audit_log")
        # insert records in employee table
        query = "INSERT INTO audit_log(time,message,url) VALUES (now(),'info','"+logfile+"')"
        cur.execute(query)
        conn.commit()
        logger.info("%s \n Running Successfully",urls)



    def content_type_multi(self):
        # In content_type_multi collect url for pdf,code,videos
        #  1.query: keyword to download the documents using search result
        #  2.Lang: language name
        #  3.content_type:type of format like pdf, program, videos,images etc..
        output=[]
        my_dict=[]
        dict_temp={}
        list_content=['pdf','videos','program']
        for content in list_content:
            my_dict.append(self.google(content) if (self.search_engine == "google") else self.bing(content) if (self.search_engine == "bing") else self.duckduckgo(content) if (self.search_engine == "duckduckgo") else self.custom(content))
            '''if(self.search_engine == "google"):
                my_dict.append(self.google(content))
            elif (self.search_engine == "bing"):
                my_dict.append(self.bing(content))
            else:
                my_dict.append(self.duckduckgo(content))'''
        
        url1=[]
        t1=[]
        desc1= []
        for j in range(len(list_content)):
            url=[]
            t=[]
            desc=[]
            for i in range(len(my_dict[j])):
                url.append(my_dict[j][i]['url'])
                t.append(my_dict[j][i]['title'])
                desc.append(my_dict[j][i]['description'])
            UrlExtract.log(url)
            url1.append(url)
            t1.append(t)
            desc1.append(desc)

        var = Extraction(self.content_type,self.query)
        for i in range(len(url1[0])):
            output1=var.pdf_content(url1[0][i])
            output.append(output1)
        for i in range(len(url1[1])):
            output2=var.video_content(url1[1][i])
            output.append(output2)
        for i in range(len(url1[2])):
            output3=var.code_snippet(url1[2][i],t1[2][i],list_content[2],desc1[2][i])
            output.append(output3)
        output = list(filter(lambda x: x, output))
        return output

    def content_type_individual(self):

    # In content_type_individual collect url for pdf,code,videos,text
    #  1.query: keyword to download the documents using search result
    #  2.Lang: language name
    #  3.content_type:type of format like pdf, program, videos,images etc..
        output=[]
        my_dict=[]
        dict_temp={}
        my_dict = self.google(self.content_type) if (self.search_engine == "google") else self.bing(self.content_type) if (self.search_engine == "bing") else self.duckduckgo(self.content_type) if (self.search_engine == "duckduckgo") else self.custom(self.content_type)
        '''if(self.search_engine == "google"):
            my_dict = self.google(self.content_type)
        elif (elf.seasrch_engine == "bing"):
            my_dict = self.bing(self.content_type)
        else:
            my_dict = self.duckduckgo(self.content_type)'''
        url=[]
        for i in range(len(my_dict)):
            url.append(my_dict[i]['url'])
        UrlExtract.log(url)
        t=[]
        for i in range(len(my_dict)):
            t.append(my_dict[i]['title'])
        desc=[]
        for i in range(len(my_dict)):
            desc.append(my_dict[i]['description'])

        var = Extraction(self.content_type,self.query)
        for i in range(len(url)):
            output.append(var.pdf_content(url[i]) if (self.content_type == "pdf") else var.video_content(url[i]) if (self.content_type == "videos") else var.code_snippet(url[i],t[i],self.content_type,desc[i]) if (self.content_type == "program") else var.text_content(url[i],i))
            '''if (self.content_type == "pdf"):
                output.append(var.pdf_content(url[i]))
            elif (self.content_type == "videos"):
                output.append(var.video_content(url[i]))
            elif (self.content_type == "program"):
                output.append(var.code_snippet(url[i],t[i],self.content_type))
            else:
                output.append(var.text_content(url[i],i))'''
        output = list(filter(lambda x: x, output))
        return output

    def url_collection(self):
        working_directory = cfg.url["working_directory"]
        return self.content_type_multi() if (self.content_type == "multi") else self.content_type_individual()
        '''if self.content_type == "multi":
            output=self.content_type_multi()

        else:
            output =self.content_type_individual()
        return output'''

        '''for i in range (len(url1)):
            for j in range(len(url1[i])):
                switcher = { 0 : }

        def pdf(url,query,content_type):
            for i in range(len(url[0])):
                output1=Extraction.pdf_content(url1[0][i], content_type,query)
                output.append(output1)
            return output
        switcher = {
            0:pdf(url1,query,content_type)
        }
        return switcher.get(0,"default")'''
