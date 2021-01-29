import requests
import configparser as cfg
import pandas as pd
import time
import datetime
from bs4 import BeautifulSoup as soup
import numpy as np

def read_token_from_config_file(config):
    parser = cfg.ConfigParser()
    parser.read(config)
    return parser.get('creds', 'token')
    
def parse_df(df):
    df = df.sort_values(by='time', ascending= True)
    this_list= df.values.tolist()
    return this_list
        
def send_message(base_url, base_url2, this_list, topic):
    if len(this_list) > 0:
        for i in this_list:
            msg = '**New {} Post Details*** \n Author: {} \n Title: {} \n Link: {} \n'.format(topic,i[0],i[3], i[4])
            url = base_url + "sendMessage?chat_id={}&text={}".format(631260160,msg)
            url2 = base_url2 + "sendMessage?chat_id={}&text={}".format(730041113,msg)
            if msg is not None:
                requests.get(url)
                requests.get(url2)
    else:
        pass

def request_page(url):
    now = datetime.datetime.now()
    today5 = now.replace(hour= 17, minute =0,second=0, microsecond=0)
    if now > today5:
        yesterday = datetime.date.today()
    else:
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
    today_date = yesterday.strftime("%Y/%m/%d")
    print('Scraping date', today_date)
    req = requests.get(url+today_date)
    return req

def soupReq(req):
    html = soup(req.content, 'lxml')
    container = html.find('div', class_= 'js-postStream u-marginTop25')
    each_list = container.find_all('div', class_= 'streamItem streamItem--postPreview js-streamItem')
    list_of_lists = []
    for i in each_list:
        try:
            post_series = i.find('div', class_= 'u-flexCenter').find('div', class_ = 'postMetaInline postMetaInline-authorLockup ui-captionStrong u-flex1 u-noWrapWithEllipsis').find('a', class_= 'ds-link ds-link--styleSubtle link--darken link--accent u-accentColor--textNormal').getText()
        except:
            post_series = np.nan
        try:
            time = i.find('div', class_= 'u-flexCenter').find('div', class_ = 'postMetaInline postMetaInline-authorLockup ui-captionStrong u-flex1 u-noWrapWithEllipsis').find('time')['datetime']
        except:
            time = np.nan
        try:
            title = i.find('h3').getText()
        except:
            title = np.nan
        try:
            link = i.find('a', class_= '')['href']
        except:
            link = np.nan
        try:
            author = i. find('a', class_= 'ds-link ds-link--styleSubtle link link--darken link--accent u-accentColor--textNormal u-accentColor--textDarken').getText()
        except:
            author = np.nan
            
        list_of_lists.append([author, post_series,time, title, link])

    df = pd.DataFrame(list_of_lists, columns = ['author', 'postSeries', 'time', 'title', 'link'])
    df['time'] =  pd.to_datetime(df['time'], format='%Y-%m-%dT%H:%M:%S')
    df = df.sort_values(by='time', ascending= False)
    return df