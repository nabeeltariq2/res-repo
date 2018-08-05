

from __future__ import (absolute_import, division, print_function, unicode_literals)

#import algorithms from surprise


import numpy as np
import pandas as pd
from sqlalchemy import create_engine
np.random.seed(101)
from collections import defaultdict
import os, io, sys
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import config
# from model import add_pageview


# disable print



def compute_recommendations(user_id,prediction_table,numeric_prediction_table):

    # numeric_prediction_table=0
    #connecting to the database
    # engine = create_engine("mysql://root:sesame@localhost/ratingsx?charset=utf8", echo=True)
    engine = create_engine(config.DB_URI, echo=True)
    session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))


    algo = 'Most Popular Items'

    # add_pageview(user_id=user_id, item_id=None, page="Model Predictions", activity_type="Initialize Predictions - " + algo, rating=None) #pageview



    #reading in the database

    df_ratings = pd.read_sql('SELECT * FROM ratings;', con = engine)
    df_ratings=df_ratings[['user_id','item_id','rating']]
    df_ratings = df_ratings.dropna()
    df_ratings = df_ratings.drop_duplicates()


    df_ratings2 = pd.read_csv('data/ratings.csv', low_memory=False)
    df_ratings2 = df_ratings2.rename(columns = {'movie_id': 'item_id'})
    df_ratings2 = df_ratings2[['user_id','item_id','rating']]
    df_ratings2 = df_ratings2.dropna()
    df_ratings2 = df_ratings2.drop_duplicates()

    df_ratings = pd.concat([df_ratings, df_ratings2], axis=0)


    df_items = pd.read_sql('SELECT * FROM items;', con = engine)

    item_filter = pd.DataFrame(df_ratings['item_id'])
    item_filter = item_filter.groupby('item_id').size()
    item_filter = item_filter.to_frame().reset_index()
    item_filter.columns.values[1] = 'count'
    item_filter = item_filter.sort_values('count', ascending=False)

    items_for_num_ratings = item_filter.head(n=30)

    item_filter = item_filter.head(n=10)
    item_filter = item_filter[['item_id']]


    df_pred = pd.DataFrame(item_filter.values.T[0:], columns= ['pred_1', 'pred_2','pred_3','pred_4',
                                   'pred_5','pred_6','pred_7','pred_8',
                                  'pred_9','pred_10'])

    df_pred['id'] = user_id

    df_pred = df_pred[['id','pred_1', 'pred_2','pred_3','pred_4',
                                   'pred_5','pred_6','pred_7','pred_8',
                                  'pred_9','pred_10']]

    df_pred['id'] = df_pred['id'].astype(int)

    df_pred.to_sql(prediction_table,engine,if_exists='append', index=False)#if_exists='append'
    session.commit()

    num_ratings = items_for_num_ratings

    num_ratings['user_id'] = user_id

    num_ratings['algorithm'] = algo

    num_ratings = num_ratings[['user_id', 'item_id', 'algorithm']]


    num_ratings.to_sql('numeric_predictions',engine,if_exists='append', index=False)#if_exists='append'
    session.commit()

    # add_pageview(user_id=user_id, item_id=None, page="Model Predictions", activity_type="Finish Computing Predictions - " + algo, rating=None) #pageview
