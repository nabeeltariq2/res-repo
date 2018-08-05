

import config
from sqlalchemy.ext.declarative import declarative_base



def auto_truncate_description(val):
    return val[:1024]
def auto_truncate_title(val):
    return val[:255]


from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import numpy as np
import pandas as pd
import datetime




def auto_truncate_description(val):
    return val[:1024]
def auto_truncate_title(val):
    return val[:255]



df_ratings = pd.read_csv("data/ratings.csv", low_memory=False)


# subsetting dataframe
df_ratings = df_ratings[["user_id", "movie_id", "rating", "timestamp"]]
df_ratings.timestamp = pd.to_datetime(df_ratings["timestamp"],unit = 's')



#changing column names
df_ratings = df_ratings.rename(columns={'movie_id': 'item_id'})

#extracting top rated items from the ratings dataframe

item_filter = pd.DataFrame(df_ratings['item_id'])
item_filter = item_filter.groupby('item_id').size()
item_filter = item_filter.to_frame().reset_index()
item_filter.columns.values[1] = 'count'
item_filter = item_filter.sort_values('count', ascending=False)

# item_filter = item_filter.head(n=8000)
item_filter = item_filter.sample(frac=1)


item_filter = item_filter[['item_id']]

df_ratings = pd.merge(left=df_ratings,right=item_filter, left_on='item_id', right_on='item_id')



# creating keys
df_ratings = df_ratings.sort_values("user_id")



df_ratings.user_id = df_ratings.user_id.astype("category")

df_ratings["userid_key"] = df_ratings["user_id"].cat.codes
df_ratings["userid_key"] = df_ratings["userid_key"] + 1

df_ratings = df_ratings.rename(columns={'user_id': 'old_user_id'})

df_ratings = df_ratings.rename(columns={'userid_key': 'user_id'})

# reading in items
# df_items = pd.read_csv("data/meta.csv", low_memory= False, converters={'description': auto_truncate_description,'title': auto_truncate_title})

df_items = pd.read_csv("data/movies_with_meta.csv",low_memory=False)

# extracting specific columns

# df_items = df_items[["movieId", "title", "genres"]]



df_items = df_items.rename(columns={'movieId': 'id'})

df_items = pd.merge(left=df_items,right=item_filter, left_on='id', right_on='item_id')

# df_items = df_items[["id", "title", "genres"]]
df_items.drop(['item_id'], axis=1, inplace=True)


df_users = pd.DataFrame()

df_users["id"] = df_ratings.user_id.unique()
df_users = pd.merge(df_users,df_ratings , left_on="id", right_on= "user_id")

df_users = df_users[['id', 'old_user_id']]
df_users = df_users.drop_duplicates()

df_ratings = df_ratings[['user_id', 'item_id', 'rating']]



for i in df_items.columns:
    df_items[i] = df_items[i].astype('str')
    df_items[i] = df_items[i].apply(lambda x: x.decode('unicode_escape').\
                                          encode('ascii', 'ignore').\
                                          strip())


df_items['id'] = df_items['id'].astype(int)
# df_items['year'] = df_items['year'].astype(int)

# df_items['id'] = df_items['id'].astype(int)



df_current_algo = pd.DataFrame(columns = ['id', 'algorithm'])

df_current_algo.loc[1] = [1, 'recommender1_random']
df_current_algo.loc[2] = [2, 'recommender2_topitems']



engine = create_engine(config.DB_URI, echo=False)


# engine = create_engine(config.DB_URI, echo=False)

session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))


# Append users
df_users.to_sql('users',engine,if_exists='append', index=False) #if_exists='append'
session.commit()

#Append items
df_items.to_sql('items',engine,if_exists='append', index=False)#if_exists='append'
session.commit()


df_current_algo.to_sql('Current_algo',engine,if_exists='append', index=False)#if_exists='append'
session.commit()

# # Append ratings
# df_ratings.to_sql('ratings',engine,if_exists='append', index=False)#if_exists='append'
# session.commit()
