#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install selenium


# In[2]:


pip install beautifulsoup4


# In[1]:


a = "hello world"
print(a)


# In[19]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep

# create a new chrome session
# Chrome(chrome_options=options, ..로 하면
# chrome_options를 options로 바꾸라는 오류 표시됨
# DeprecationWarning: use options instead of chrome_options

driver = webdriver.Chrome(options=options, executable_path="/home/bitai/proj_my/test_Wandoo_2/crawling_driver/chromedriver_linux64/chromedriver")
driver.maximize_window()


# Navigate to the application home page
driver.get('https://www.youtube.com/user/BuzzBean11/videos')

# 1.25초간 sleep
sleep(1.25)

page = driver.page_source
page


# In[24]:


# 영상 제목 추출

from bs4 import BeautifulSoup

soup = BeautifulSoup(page,'lxml')

all_title = soup.find_all('a', 'yt-simple-endpoint style-scope ytd-grid-video-renderer')
title = [soup.find_all('a', 'yt-simple-endpoint style-scope ytd-grid-video-renderer')
         [n].string for n in range(0, len(all_title))]

sleep(1.53)

title


# In[38]:


# 영상 길이 추출

import time
import random

# all_video_time = 30개
all_video_time = soup.find_all('span', 'style-scope ytd-thumbnail-overlay-time-status-renderer')
# video_time
video_time = [soup.find_all('span', 'style-scope ytd-thumbnail-overlay-time-status-renderer')
              [n].string.strip() for n in range(0, len(all_video_time))]


# sleep(1.97)

# 1~5초 사이 랜덤한 시간으로 휴식 후 데이터 긁어옴
time.sleep(random.uniform(1, 5))

# print(all_video_time)
# print("====================================")

# print 넣은 값과 그냥 뿌린 값의 출력모양이 다르다(수평, 수직)
print(video_time)
print("=============================================================")
video_time


# In[57]:


# 채널명
channel_name = soup.find('yt-formatted-string', 'style-scope ytd-channel-name').string

# 구독자 수
subscribe_num = soup.find('yt-formatted-string', 'style-scope ytd-c4-tabbed-header-renderer').string[0:6]

# 조회수, 업로드 시점
c = soup.find_all('span', 'style-scope ytd-grid-video-renderer')
views_num = [soup.find_all('span', 'style-scope ytd-grid-video-renderer')[n].string for n in range(0, len(c))]


# In[45]:


from time import localtime, strftime

# 현재 시간
present_datetime = strftime("%Y/%m/%d %H:%M:%S", localtime())

present_datetime


# In[58]:


youtube_video_list = []


x = 0       # 조회수 index
y = 1       # 업로드 index

for i in range(0, len(all_title)):
    vid_row = []
    
    vid_row.append(channel_name)
    vid_row.append(title[i])
    vid_row.append(video_time[i].strip())    
    vid_row.append(subscribe_num)
    vid_row.append(views_num[x])
    x += 2                        # 조회수만 append
    vid_row.append(views_num[y])
    y += 2                        # 업로드 시점만 append
    vid_row.append(present_datetime)
    youtube_video_list.append(vid_row)
    
    # 너무느림
    # time.sleep(random.uniform(2, 5))
    
    time.sleep(random.uniform(1, 3))
    
youtube_video_list


# In[60]:


import csv

vid_csv_file = open("/home/bitai/proj_my/test_Wandoo_2/crawling_driver/videostack.csv", "w", newline="")

vid_csv_writer = csv.writer(vid_csv_file)
for vs_row in youtube_video_list:
    vid_csv_writer.writerow(vs_row)
    
vid_csv_file.close()


# In[61]:


pip install pymysql


# In[64]:


# mysql로 DB 만들기

CREATE TABLE video_crawl_table(
    `video_id` INT NOT NULL AUTO_INCREMENT, # PK
    `youtuber_name` VARCHAR(100),
    `video_play_time` VARCHAR(30),
    `subscribe_num` VARCHAR(100),
    `views_num` VARCHAR(100),
    `upload_time` VARCHAR(80),
    `crwaling_time` VARCHAR(80),
    PRIMARY KEY(video_id)
) CHARSET = utf8;


# In[65]:





# In[66]:


import pymysql 

class DBConnect:
    
    # 생성자 선언
    def __init__(self):
        self.conn = pymysql.connect(host = 'localhost', 
                                    user = 'bitai', 
                                    password = '456123', 
                                    db = 'video_crawl_db', 
                                    charset = 'utf8')
        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)
        
    # insert 메서드 정의
    def video_insert(self, tag_dict):
        try:
            # insert 쿼리 작성
            sql = """insert into video_crawl_table (video_id, youtuber_name, video_play_time, subscribe_num, views_num, upload_time, crwaling_time)"""
            
            for col_0, col_1, col_2, col_3, col_4, col_5, col_6 in tag_dict:
                # insert 쿼리 실행
                self.curs.execute(sql, "{}{}{}{}{}{}{}".format(col_0, col_1, col_2, col_3, col_4, col_5, col_6))
                
            # DML문 완료 후 커밋
            self.conn.commit()
            
        except Exception as e:
            print(e)
            
        finally:
            # 커넥트 인스턴스 닫기
                self.conn.close()


# In[67]:


from db_connect import DBConnect

db = DBConnect()
db.insert(range(0, len(all_title)))


# In[ ]:




