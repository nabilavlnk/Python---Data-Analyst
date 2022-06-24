#!/usr/bin/env python
# coding: utf-8

# ## Scraping Instagram menggunakan Instaloader

# In[2]:


# Library
import getpass
from instaloader import Instaloader, Profile
import instaloader
from datetime import datetime
from dateutil import parser
from itertools import dropwhile, takewhile
import pandas as pd
import processing
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials
pd.options.mode.chained_assignment = None  # default='warn'
L = Instaloader()


# ## Function Login

# In[3]:


def Login(USER,PASSWORD):
    # login setup and process
    USER = USER
    PASSWORD = PASSWORD
    L.login(USER,PASSWORD)


# In[4]:


# Login
print("Login Instagram")
Login(input("Username : "), getpass.getpass("Password : "))
print("Berhasil Login")


# ## Function Get Data

# In[ ]:


# Data yang diambil :
# - Date
# - Username
# - Post Type
# - Likes
# - Comments
# - Caption
# - Date


# In[5]:


# read csv
dataUser = pd.read_excel('data_akun.xlsx') 
listUser = dataUser['username'].values.tolist()
#print(listUser)


# In[6]:


# Function Get Data
data = []
def get_data(username, date):
    df = pd.DataFrame()
    SINCE = date
    profil = instaloader.Profile.from_username(L.context, username)
    posts = instaloader.Profile.from_username(L.context, username).get_posts()
    for post in takewhile(lambda p: p.date_utc > SINCE, posts):
        post_type = ""
        folls = profil.followers
        caption = post.caption
        owner = post.owner_username
        like = post.likes
        com = post.comments
        date = post.date
        url = "https://www.instagram.com/p/" + post.shortcode + "/"
                    
        if (post.typename == 'GraphImage') :
            post_type = "Single"
        elif (post.typename == 'GraphVideo') :
            post_type = "Video"
        elif (post.typename == 'GraphSidecar') :
            post_type = "Carousel"
        else :
            post_type = post.typename
        
        temp = [date, owner, folls, post_type, like, com, caption, url]
        data.append(temp)
        col = ['date', 'user_id', 'followers', 'post_type', 'total_likes', 'total_comments', 'caption', 'url']
        df = pd.DataFrame(data, columns = col)
    return df


# In[7]:


# Get Data
print("Ambil Data")
date = parser.parse(input("Dari tanggal (YYYY, M, D): "))
for akun in listUser:
    df = get_data(akun, date)
    print("Pengambilan data akun " + akun + " berhasil.")
print("Program selesai.")


# ###### Dari 32 data akun instagram, terdapat 3 akun yang hasil scraping tidak muncul dikarenakan data tidak ada dalam rentang Date. Serta beberapa akun tidak muncul hasil scraping tetapi belum tau penyebabnya.

# # Transformation Code

# In[8]:


def transform(df):
    temp_df = processing.duplicate(df)
    temp_df = processing.handleMistake(df)
    temp_df = processing.handleNull(df)
    temp_df = processing.split(df)
    temp_df = processing.eksperimen1(df)
    return temp_df


# In[9]:


result = transform(df)


# # Save Excel

# In[10]:


#simpan ke excel
def saveExcel(result):
    result.to_excel("hasil_sort_akun.xlsx")
    print("Data berhasil disimpan")


# In[11]:


saveExcel(result)


# In[ ]:




