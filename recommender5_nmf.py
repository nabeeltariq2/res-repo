# from __future__ import absolute_import, division, print_function, unicode_literals

# from surprise import evaluate, print_perf, dump, Reader, Dataset
#import algorithms from surprise
from surprise import evaluate, print_perf, Reader, Dataset, accuracy

# from surprise import KNNBasic, KNNWithMeans, KNNWithZScore, AlgoBase, SlopeOne, CoClustering, NormalPredictor,NMF, SVD, BaselineOnly

import time
start_time = time.time()

from surprise import NMF

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
# from surprise import dump
# from model import add_pageview


# algorithm = NMF(n_epochs=10)




def compute_recommendations(user_id, prediction_table, numeric_prediction_table):


    algo = 'NMF'

    algorithm = NMF()



    # add_pageview(user_id=user_id, item_id=None, page="Model Predictions", activity_type="Initialize Predictions - " + algo, rating=None) #pageview



    engine = create_engine(config.DB_URI, echo=True)
    session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))



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




    reader = Reader(line_format='user item rating', sep=',', rating_scale=(1, 10))
    data = Dataset.load_from_df(df_ratings, reader=reader)

    trainset = data.build_full_trainset()


#     algorithm = eval(algo + "()")# set the algorithm...............................................


    algorithm.train(trainset)

    items = pd.read_sql('SELECT distinct id FROM items;', con = engine)
    df_user_items = df_ratings.loc[df_ratings['user_id'] == user_id]
    total_items = items.id.unique()
    user_items = df_user_items.item_id.unique()
    # user_id = str(user_id)
    prediction_items = [x for x in total_items if x not in user_items]

    predictions = pd.DataFrame(columns=['user_id', 'item_id', 'prediction'])


    predicted_ratings = []

    for i in prediction_items:
        a = user_id
        b = i
        est = algorithm.predict(a, b)
        predicted_ratings.append(est[3])

    predictions['item_id'] = prediction_items
    predictions['user_id'] = pd.Series([user_id for x in range(len(predictions.index))], index=predictions.index)


    predictions['prediction'] = predicted_ratings


    predictions = predictions.sort_values('prediction', ascending=False)
    test_prediction = predictions
    predictions = predictions.head(n=10)


    cols =['pred_1', 'pred_2','pred_3','pred_4',
                                   'pred_5','pred_6','pred_7','pred_8',
                                  'pred_9','pred_10']




    df_pred = predictions[['item_id']].T

    df_pred.columns = cols

    df_pred['id'] = user_id



    df_pred = df_pred[['id','pred_1', 'pred_2','pred_3','pred_4',
                                       'pred_5','pred_6','pred_7','pred_8',
                                      'pred_9','pred_10']]

    df_pred['id'] = df_pred['id'].astype(int)



    df_pred.to_sql(prediction_table, engine,if_exists='append', index=False)#if_exists='append'
    session.commit()


    df_num_ratings = test_prediction

    df_num_ratings = df_num_ratings.head(n=20)

    df_num_ratings['algorithm'] = algo
    df_num_ratings.rename(columns={'prediction':'predicted_rating'}, inplace=True)


    df_num_ratings.to_sql('numeric_predictions',engine,if_exists='append', index=False)#if_exists='append'
    session.commit()


    predcols =['num_1', 'num_2','num_3','num_4',
                                       'num_5','num_6','num_7','num_8',
                                      'num_9','num_10']

    df_num_ratings_transpose = predictions[['prediction']].T
    df_num_ratings_transpose.columns = predcols




    df_num_ratings_transpose['id'] = user_id

    df_num_ratings_transpose = df_num_ratings_transpose[['id','num_1', 'num_2','num_3','num_4',
                                       'num_5','num_6','num_7','num_8',
                                      'num_9','num_10']]

    df_num_ratings_transpose['id'] = df_num_ratings_transpose['id'].astype(int)








    df_num_ratings_transpose.to_sql(numeric_prediction_table,engine,if_exists='append', index=False)#if_exists='append'
    session.commit()




    # add_pageview(user_id=user_id, item_id=None, page="Model Predictions", activity_type="Finish Computing Predictions - " + algo, rating=None) #pageview
