#!/usr/bin/env python
# coding: utf-8

# In[20]:


from datetime import datetime
from itertools import dropwhile, takewhile
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'


# In[21]:


# fungsi buat drop duplicate
def duplicate(df):
    df.drop_duplicates(inplace=True)


# In[22]:


# fungsi untuk handling mistaken data type
# headerList = ['date', 'username', 'post_type', 'total_likes', 'total_comments','caption', 'url']
def handleMistake(df):
    # kolom date
    # df['date'] = pd.to_datetime(df['date'],  errors='coerce')
    df['date'] = df['date'].astype(str)
    # kolom username
    df['user_id'][df['user_id'].astype(str).str.isdigit()] = np.NaN
    # kolom post_type
    df['post_type'][df['post_type'].astype(str).str.isdigit()] = np.NaN
    # kolom total_likes
    df['total_likes'] = pd.to_numeric(df['total_likes'], errors='coerce')
    # kolom komen
    df['total_comments'] = pd.to_numeric(df['total_comments'], errors='coerce')


# In[23]:


# fungsi untuk handling kasus null
# headerList = ['date', 'username', 'post_type', 'total_likes', 'total_comments','caption', 'url']
def handleNull(df):
    # kolom date
    df['date'] = df['date'].fillna(method='ffill').fillna(method='bfill')
    # kolom akun
    df['user_id'].fillna("undefined", inplace=True)  
    # kolom post_type
    df['post_type'].fillna("undefined", inplace=True)  
    # kolom likes
    df['total_likes'].fillna("-100", inplace=True)
    # kolom komen
    df['total_comments'].fillna("-100", inplace=True) 


# In[24]:


# fungsi untuk split date column
def split(df):
    df[['date', 'time']] = df['date'].str.split(' ', 1, expand=True)


# In[25]:


# ['date', 'username', 'post_type', 'total_likes', 'total_comments','caption', 'url']
# eksperimen 1 -> post dengan engagement tertinggi adalah jumlah total likes dan komen terbanyak
def eksperimen1(df):
    df['likes+komen'] = df['total_likes'] + df['total_comments']
    df['ER(%)'] = (df['likes+komen'] / df['followers']) *100
    df = df.sort_values(by= "ER(%)", ascending=False)
    return df.head(15)


# In[ ]:




