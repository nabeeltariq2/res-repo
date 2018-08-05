
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime,Sequence, Numeric, Float
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import config
from sqlalchemy import text
# import recommender1
# import recommender2
from planout.experiment import SimpleExperiment
from planout.ops.random import *
from sqlalchemy_utils import database_exists, create_database
import datetime
from sqlalchemy.sql import func




engine = create_engine(config.DB_URI, echo=False)
if not database_exists(engine.url):
    create_database(engine.url)
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))



Base = declarative_base()
Base.query = session.query_property()


### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable = True)
    turk_id = Column(String(64), nullable = True)
    age = Column(String(64), nullable = True)
    gender = Column(String(64), nullable = True)
    occupation = Column(String(128), nullable = True)
    state = Column(String(64), nullable = True)
    country = Column(String(64), nullable = True)
    old_user_id = Column(String(64), nullable = True)
    user_add_time = Column(DateTime, server_default=func.now())

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key = True)
    # tmdb_id = Column(Integer, nullable=True)
    tmdb_id = Column(String(128), nullable=True)
    # genres = Column(String(256), nullable = True)
    youtubeId = Column(String(128), nullable = True)
    # adult = Column(String(64), nullable = True)
    # budget = Column(String(64), nullable = True)
    # homepage = Column(String(64), nullable = True)
    imdb_id = Column(String(64), nullable = True)
    original_language = Column(String(64), nullable = True)
    # original_title = Column(String(64), nullable = True)
    overview = Column(String(1280), nullable = True)
    popularity = Column(String(64), nullable = True)
    poster_path = Column(String(128), nullable = True)
    # release_date = Column(String(32), nullable = True)
    # revenue = Column(String(64), nullable = True)
    runtime = Column(String(64), nullable = True)
    tagline = Column(String(512), nullable = True)
    # video = Column(String(32), nullable = True)
    vote_average = Column(String(64), nullable = True)
    vote_count = Column(String(64), nullable = True)
    # status = Column(String(32), nullable = True)
    genres = Column(String(256), nullable = True)
    # production_companies = Column(String(512), nullable = True)
    # production_country_code = Column(String(64), nullable = True)
    # production_country = Column(String(256), nullable = True)
    # spoken_langauge_full = Column(String(64), nullable = True)
    # collection = Column(String(128), nullable = True)
    # Collection_poster_path = Column(String(128), nullable = True)
    # collection_backdrop_path = Column(String(128), nullable = True)

    # year = Column(String(32), nullable = True)
    year = Column(Integer, nullable = True)

    title = Column(String(128), nullable = True)
    item_time = Column(DateTime, server_default=func.now())



class Rating(Base):
### Association object
    __tablename__= "ratings"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    rating = Column(Integer,nullable=True)
    # rating = Column(Float,nullable=True)
    text_rating = Column(String(256), nullable = True)

    rating_time = Column(DateTime, server_default=func.now())

    user = relationship("User", backref=backref("ratings", order_by=id))
    item = relationship("Item", backref=backref("ratings", order_by=id))




# class Recommendations(Base):
# ### Association object
#     __tablename__= "recommendations"
#
#     id = Column(Integer, ForeignKey('users.id'),primary_key = True)
#     pred_1 = Column(String(128), nullable=True)
#     pred_2 = Column(String(128), nullable=True)
#     pred_3 = Column(String(128), nullable=True)
#     pred_4 = Column(String(128), nullable=True)
#     pred_5 = Column(String(128), nullable=True)
#     pred_6 = Column(String(128), nullable=True)
#     pred_7 = Column(String(128), nullable=True)
#     pred_8 = Column(String(128), nullable=True)
#     pred_9 = Column(String(128), nullable=True)
#     pred_10 = Column(String(128), nullable=True)
#
#     user = relationship("User", backref=backref("recommendations", order_by=id))
#


class Recommendations1(Base):
### Association object
    __tablename__= "recommendations1"

    id = Column(Integer, ForeignKey('users.id'),primary_key = True)
    pred_1 = Column(Integer, nullable=True)
    pred_2 = Column(Integer, nullable=True)
    pred_3 = Column(Integer, nullable=True)
    pred_4 = Column(Integer, nullable=True)
    pred_5 = Column(Integer, nullable=True)
    pred_6 = Column(Integer, nullable=True)
    pred_7 = Column(Integer, nullable=True)
    pred_8 = Column(Integer, nullable=True)
    pred_9 = Column(Integer, nullable=True)
    pred_10= Column(Integer, nullable=True)

    user = relationship("User", backref=backref("recommendations1", order_by=id))
    # item = relationship("Item", backref=backref("recommendations", order_by=id))


class Recommendations2(Base):
### Association object
    __tablename__= "recommendations2"

    id = Column(Integer, ForeignKey('users.id'),primary_key = True)
    pred_1 = Column(Integer, nullable=True)
    pred_2 = Column(Integer, nullable=True)
    pred_3 = Column(Integer, nullable=True)
    pred_4 = Column(Integer, nullable=True)
    pred_5 = Column(Integer, nullable=True)
    pred_6 = Column(Integer, nullable=True)
    pred_7 = Column(Integer, nullable=True)
    pred_8 = Column(Integer, nullable=True)
    pred_9 = Column(Integer, nullable=True)
    pred_10= Column(Integer, nullable=True)

    user = relationship("User", backref=backref("recommendations2", order_by=id))
    # item = relationship("Item", backref=backref("recommendations", order_by=id))


class Transposed_prediction1(Base):
### Association object
    __tablename__= "transposed_prediction1"

    id = Column(Integer, ForeignKey('users.id'),primary_key = True)
    num_1 = Column(Float, nullable=True)
    num_2 = Column(Float, nullable=True)
    num_3 = Column(Float, nullable=True)
    num_4 = Column(Float, nullable=True)
    num_5 = Column(Float, nullable=True)
    num_6 = Column(Float, nullable=True)
    num_7 = Column(Float, nullable=True)
    num_8 = Column(Float, nullable=True)
    num_9 = Column(Float, nullable=True)
    num_10= Column(Float, nullable=True)

    user = relationship("User", backref=backref("transposed_prediction1", order_by=id))
    # item = relationship("Item", backref=backref("recommendations", order_by=id))

class Transposed_prediction2(Base):
### Association object
    __tablename__= "transposed_prediction2"

    id = Column(Integer, ForeignKey('users.id'),primary_key = True)
    num_1 = Column(Float, nullable=True)
    num_2 = Column(Float, nullable=True)
    num_3 = Column(Float, nullable=True)
    num_4 = Column(Float, nullable=True)
    num_5 = Column(Float, nullable=True)
    num_6 = Column(Float, nullable=True)
    num_7 = Column(Float, nullable=True)
    num_8 = Column(Float, nullable=True)
    num_9 = Column(Float, nullable=True)
    num_10= Column(Float, nullable=True)

    user = relationship("User", backref=backref("transposed_prediction2", order_by=id))
    # item = relationship("Item", backref=backref("recommendations", order_by=id))



class Recrating(Base):
### Association object
    __tablename__= "recrating"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user_rating_1 = Column(Integer, nullable = True)
    user_rating_2 = Column(Integer, nullable = True)
    user_rating_3 = Column(Integer, nullable = True)
    user_rating_4 = Column(Integer, nullable = True)
    user_rating_5 = Column(Integer, nullable = True)
    user_rating_6 = Column(Integer, nullable = True)
    user_rating_7 = Column(Integer, nullable = True)
    user_rating_8 = Column(Integer, nullable = True)
    user_rating_9 = Column(Integer, nullable = True)
    user_rating_10 = Column(Integer, nullable = True)
    rec_rating_time = Column(DateTime, server_default=func.now())

    user = relationship("User", backref=backref("recrating", order_by=id))


class Userrating(Base):
### Association object
    __tablename__= "userrating"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    novel_rating_1 = Column(Integer, nullable = True)
    novel_rating_2 = Column(Integer, nullable = True)
    novel_rating_3 = Column(Integer, nullable = True)
    novel_rating_4 = Column(Integer, nullable = True)
    novel_rating_5 = Column(Integer, nullable = True)
    novel_rating_6 = Column(Integer, nullable = True)
    novel_rating_7 = Column(Integer, nullable = True)
    novel_rating_8 = Column(Integer, nullable = True)
    novel_rating_9 = Column(Integer, nullable = True)
    novel_rating_10 = Column(Integer, nullable = True)
    unexp_find_rating_1 = Column(Integer, nullable = True)
    unexp_find_rating_2 = Column(Integer, nullable = True)
    unexp_find_rating_3 = Column(Integer, nullable = True)
    unexp_find_rating_4 = Column(Integer, nullable = True)
    unexp_find_rating_5 = Column(Integer, nullable = True)
    unexp_find_rating_6 = Column(Integer, nullable = True)
    unexp_find_rating_7 = Column(Integer, nullable = True)
    unexp_find_rating_8 = Column(Integer, nullable = True)
    unexp_find_rating_9 = Column(Integer, nullable = True)
    unexp_find_rating_10 = Column(Integer, nullable = True)
    unexp_recom_rating_1 = Column(Integer, nullable = True)
    unexp_recom_rating_2 = Column(Integer, nullable = True)
    unexp_recom_rating_3 = Column(Integer, nullable = True)
    unexp_recom_rating_4 = Column(Integer, nullable = True)
    unexp_recom_rating_5 = Column(Integer, nullable = True)
    unexp_recom_rating_6 = Column(Integer, nullable = True)
    unexp_recom_rating_7 = Column(Integer, nullable = True)
    unexp_recom_rating_8 = Column(Integer, nullable = True)
    unexp_recom_rating_9 = Column(Integer, nullable = True)
    unexp_recom_rating_10 = Column(Integer, nullable = True)
    diversity_rating_1 = Column(Integer, nullable = True)
    diversity_rating_2 = Column(Integer, nullable = True)
    diversity_rating_3 = Column(Integer, nullable = True)
    diversity_rating_4 = Column(Integer, nullable = True)
    diversity_rating_5 = Column(Integer, nullable = True)
    diversity_rating_6 = Column(Integer, nullable = True)
    diversity_rating_7 = Column(Integer, nullable = True)
    diversity_rating_8 = Column(Integer, nullable = True)
    diversity_rating_9 = Column(Integer, nullable = True)
    diversity_rating_10 = Column(Integer, nullable = True)
    unexp_implic_1 = Column(Integer, nullable = True)
    unexp_implic_2 = Column(Integer, nullable = True)
    unexp_implic_3 = Column(Integer, nullable = True)
    unexp_implic_4 = Column(Integer, nullable = True)
    unexp_implic_5 = Column(Integer, nullable = True)
    unexp_implic_6 = Column(Integer, nullable = True)
    unexp_implic_7 = Column(Integer, nullable = True)
    unexp_implic_8 = Column(Integer, nullable = True)
    unexp_implic_9 = Column(Integer, nullable = True)
    unexp_implic_10 = Column(Integer, nullable = True)
    rating_time = Column(DateTime, server_default=func.now())

    user = relationship("User", backref=backref("userrating", order_by=id))







class Feedback(Base):
### Association object
    __tablename__= "feedback"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    novelty = Column(Integer, nullable = True)
    unexpectedness = Column(Integer, nullable = True)
    satisfaction = Column(Integer, nullable = True)
    recommendation = Column(Integer, nullable = True)
    overall_unexp_implicit = Column(Integer, nullable = True)
    feedback_time = Column(DateTime, server_default=func.now())

    user = relationship("User", backref=backref("feedback", order_by=id))



class Within_feedback(Base):
### Association object
    __tablename__= "within_feedback"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    within_unexp_find = Column(Integer, nullable = True)
    within_unexp_implicit = Column(Integer, nullable = True)
    within_novel = Column(Integer, nullable = True)
    within_diversity = Column(Integer, nullable = True)
    within_satisfaction = Column(Integer, nullable = True)
    any_feedback = Column(String(512), nullable = True)
    feedback_time = Column(DateTime, server_default=func.now())

    user = relationship("User", backref=backref("within_feedback", order_by=id))



# class Algo(Base):
#     __tablename__ = "algo"
#
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     algorithm = Column(String(128))
#     train_mae = Column(Float, nullable=True)
#     test_mae = Column(Float, nullable=True)
#     train_rmse = Column(Float, nullable=True)
#     test_rmse = Column(Float, nullable=True)
#     algo_time = Column(DateTime, server_default=func.now())
#
#     user = relationship("User", backref=backref("algo", order_by=id))



class Algo(Base):
    __tablename__ = "algo"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    algorithm = Column(String(128))
    algo_time = Column(DateTime, server_default=func.now())

    user = relationship("User", backref=backref("algo", order_by=id))


class Current_algo(Base):
### Association object
    __tablename__= "Current_algo"

    id = Column(Integer, primary_key = True)
    algorithm = Column(String(256), nullable = False)
    update_time = Column(DateTime, server_default=func.now())


class Training(Base):
    __tablename__ = "training"

    id = Column(Integer, primary_key=True)
    # user_id = Column(Integer, ForeignKey('users.id'))
    algorithm = Column(String(128))
    train_mae = Column(Float, nullable=True)
    test_mae = Column(Float, nullable=True)
    train_rmse = Column(Float, nullable=True)
    test_rmse = Column(Float, nullable=True)
    algo_train_time = Column(DateTime, server_default=func.now())
    # user = relationship("User", backref=backref("algo", order_by=id))


class Numeric_predictions(Base):
### Association object
    __tablename__= "numeric_predictions"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    predicted_rating = Column(Float,nullable=True)
    algorithm = Column(String(128))
    prediction_time = Column(DateTime, server_default=func.now())

    user = relationship("User", backref=backref("numeric_predictions", order_by=id))
    item = relationship("Item", backref=backref("numeric_predictions", order_by=id))


class PredictionLog(Base):
### Association object
    __tablename__= "predictionlogs"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    pred_1 = Column(String(128), nullable=True)
    pred_2 = Column(String(128), nullable=True)
    pred_3 = Column(String(128), nullable=True)
    pred_4 = Column(String(128), nullable=True)
    pred_5 = Column(String(128), nullable=True)
    pred_6 = Column(String(128), nullable=True)
    pred_7 = Column(String(128), nullable=True)
    pred_8 = Column(String(128), nullable=True)
    pred_9 = Column(String(128), nullable=True)
    pred_10 = Column(String(128), nullable=True)
    algorithm = Column(String(64), nullable=True)
    pred_time = Column(DateTime, server_default=func.now())

    user = relationship("User", backref=backref("predictionlogs", order_by=id))


class ShoppingCart(Base):
### Association object
    __tablename__= "shoppingcart"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    cart_time = Column(DateTime, server_default=func.now())

    user = relationship("User", backref=backref("shoppingcart", order_by=id))
    item = relationship("Item", backref=backref("shoppingcart", order_by=id))


class PageviewLog(Base):
    __tablename__ = "pageview"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable = True)
    item_id = Column(Integer, nullable = True)
    page = Column(String(128), nullable=True)
    activity_type = Column(String(128), nullable=True)
    rating = Column(Integer, nullable=True)

    activity_time = Column(DateTime, server_default=func.now())




### End class declarations
#start function declarations


def add_pageview(user_id, item_id, page, activity_type,rating):
    page_activity = PageviewLog(user_id=user_id,item_id=item_id, page=page, activity_type=activity_type,rating=rating)
    session.add(page_activity)
    session.commit()

#
# def add_algo(user_id, algorithm, train_mae, test_mae, train_rmse, test_rmse):
#     new_algo_usage = Algo(user_id=user_id, algorithm=algorithm, train_mae=train_mae,test_mae=test_mae, train_rmse=train_rmse,  test_rmse=test_rmse)
#     session.add(new_algo_usage)
#     session.commit()


def add_algo(user_id, algorithm):
    new_algo_usage = Algo(user_id=user_id, algorithm=algorithm)
    session.add(new_algo_usage)
    session.commit()


def add_training(algorithm, train_mae, test_mae, train_rmse, test_rmse):
    new_algo_train = Trainingz(algorithm=algorithm, train_mae=train_mae,test_mae=test_mae, train_rmse=train_rmse,  test_rmse=test_rmse)
    session.add(new_algo_train)
    session.commit()


def get_user_from_email(email):
    user = User.query.filter_by(email=email).first()
    return user

def get_user_from_id(id):
    user = User.query.filter_by(id=id).first()
    return user

def get_item_from_id(id):
    item = Item.query.filter_by(id=id).first()
    return item

def create_user(email, password,turk_id, age, gender, occupation, state, country):
    user = User(email=email, password=password,turk_id=turk_id, age=age, occupation=occupation, state=state, country=country, gender=gender)
    session.add(user)
    session.commit()
    added_user = User.query.filter_by(email=email, password=password, age=age, occupation=occupation, state=state, country=country, gender=gender).first()
    new_user_id = added_user.id
    session.execute("INSERT INTO ratings SELECT null as id,u.id as user_id, i.id as item_id, null as rating, null as text_rating, NOW() as user_add_time FROM items as i CROSS JOIN users as u WHERE u.id = {user}".format(user = new_user_id))
    session.commit()

def show_item_details(id):
    item = Rating.query.filter_by(item_id=id).all()
    return item

def add_rating(item_id, user_id, rating,text_rating):
    rating = Rating(item_id=item_id, user_id=user_id, rating=rating,text_rating=text_rating)
    session.add(rating)
    session.commit()

def is_rating(user_id, item_id):
    rating = Rating.query.filter_by(user_id=user_id, item_id=item_id).first()
    return rating

def update_rating(user_id, item_id, new_rating,new_text_rating):
    old_rating = Rating.query.filter_by(user_id=user_id, item_id=item_id).first()
    old_rating.rating = new_rating
    old_rating.text_rating=new_text_rating
    session.commit()


def show_current_algo(id):
    algo = Current_algo.query.filter_by(id=id).all()
    return algo


def update_current_algo(id, algorithm):
    old_algo = Current_algo.query.filter_by(id=id).first()
    old_algo.id = id
    old_algo.algorithm=algorithm
    session.commit()
    # return old_algo





def add_new_item(user_id, item_id, rating,text_rating):
    new_rating = Rating(user_id=user_id, item_id=item_id, rating=rating,text_rating=text_rating)
    session.add(new_rating)
    session.commit()

def delete_recommendations1():
    session.execute("DELETE FROM recommendations1")
    session.commit()


def delete_recommendations2():
    session.execute("DELETE FROM recommendations2")
    session.commit()

def delete_numeric_predictions1():
    session.execute("DELETE FROM transposed_prediction1")
    session.commit()

def delete_numeric_predictions2():
    session.execute("DELETE FROM transposed_prediction2")
    session.commit()

# def calculate_recommendations_rec_1():
    # compute_recommendations1()
    # session.commit()

# def calculate_recommendations_rec_2():
    # compute_recommendations2()
    # session.commit()

def show_recommendations1(id):
    rec = Recommendations1.query.filter_by(id=id).first()
    pred_1=Item.query.filter_by(id=Recommendations1.pred_1).first()
    pred_2=Item.query.filter_by(id=Recommendations1.pred_2).first()
    pred_3=Item.query.filter_by(id=Recommendations1.pred_3).first()
    pred_4=Item.query.filter_by(id=Recommendations1.pred_4).first()
    pred_5=Item.query.filter_by(id=Recommendations1.pred_5).first()
    pred_6=Item.query.filter_by(id=Recommendations1.pred_6).first()
    pred_7=Item.query.filter_by(id=Recommendations1.pred_7).first()
    pred_8=Item.query.filter_by(id=Recommendations1.pred_8).first()
    pred_9=Item.query.filter_by(id=Recommendations1.pred_9).first()
    pred_10=Item.query.filter_by(id=Recommendations1.pred_10).first()
    return rec, pred_1, pred_2, pred_3, pred_4, pred_5, pred_6,pred_7, pred_8, pred_9,pred_10

def show_recommendations2(id):
    rec2 = Recommendations2.query.filter_by(id=id).first()
    pred_11=Item.query.filter_by(id=Recommendations2.pred_1).first()
    pred_12=Item.query.filter_by(id=Recommendations2.pred_2).first()
    pred_13=Item.query.filter_by(id=Recommendations2.pred_3).first()
    pred_14=Item.query.filter_by(id=Recommendations2.pred_4).first()
    pred_15=Item.query.filter_by(id=Recommendations2.pred_5).first()
    pred_16=Item.query.filter_by(id=Recommendations2.pred_6).first()
    pred_17=Item.query.filter_by(id=Recommendations2.pred_7).first()
    pred_18=Item.query.filter_by(id=Recommendations2.pred_8).first()
    pred_19=Item.query.filter_by(id=Recommendations2.pred_9).first()
    pred_20=Item.query.filter_by(id=Recommendations2.pred_10).first()
    return rec2, pred_11, pred_12, pred_13, pred_14, pred_15, pred_16,pred_17, pred_18, pred_19,pred_20


def show_transposed_prediction1(id):
    tp_1 = Transposed_prediction1.query.filter_by(id=id).first()
    return tp_1




def add_rec_rating(user_id,user_rating_1,user_rating_2,user_rating_3,user_rating_4,user_rating_5,user_rating_6,user_rating_7,user_rating_8,user_rating_9,user_rating_10):
    rec_rating = Recrating(user_id=user_id,user_rating_1=user_rating_1,user_rating_2=user_rating_2,user_rating_3=user_rating_3,user_rating_4=user_rating_4,user_rating_5=user_rating_5,user_rating_6=user_rating_6,user_rating_7=user_rating_7,user_rating_8=user_rating_8,user_rating_9=user_rating_9,user_rating_10=user_rating_10)
    session.add(rec_rating)
    session.commit()




def add_user_rating(user_id,novel_rating_1,novel_rating_2,novel_rating_3,novel_rating_4,novel_rating_5,novel_rating_6,novel_rating_7,novel_rating_8,novel_rating_9,novel_rating_10,
    unexp_find_rating_1,unexp_find_rating_2,unexp_find_rating_3,unexp_find_rating_4,unexp_find_rating_5,unexp_find_rating_6,unexp_find_rating_7,unexp_find_rating_8,unexp_find_rating_9,unexp_find_rating_10,
    unexp_recom_rating_1,unexp_recom_rating_2,unexp_recom_rating_3,unexp_recom_rating_4,unexp_recom_rating_5,unexp_recom_rating_6,unexp_recom_rating_7,unexp_recom_rating_8,unexp_recom_rating_9,unexp_recom_rating_10,
    diversity_rating_1,diversity_rating_2,diversity_rating_3,diversity_rating_4,diversity_rating_5,diversity_rating_6,diversity_rating_7,diversity_rating_8,diversity_rating_9,diversity_rating_10,
    unexp_implic_1,unexp_implic_2,unexp_implic_3,unexp_implic_4,unexp_implic_5,unexp_implic_6,unexp_implic_7,unexp_implic_8,unexp_implic_9,unexp_implic_10):
    user_rating = Userrating(user_id=user_id,novel_rating_1=novel_rating_1,novel_rating_2=novel_rating_2,novel_rating_3=novel_rating_3,novel_rating_4=novel_rating_4,novel_rating_5=novel_rating_5,novel_rating_6=novel_rating_6,novel_rating_7=novel_rating_7,novel_rating_8=novel_rating_8,novel_rating_9=novel_rating_9,novel_rating_10=novel_rating_10,
    unexp_find_rating_1=unexp_find_rating_1,unexp_find_rating_2=unexp_find_rating_2,unexp_find_rating_3=unexp_find_rating_3,unexp_find_rating_4=unexp_find_rating_4,unexp_find_rating_5=unexp_find_rating_5,unexp_find_rating_6=unexp_find_rating_6,unexp_find_rating_7=unexp_find_rating_7,unexp_find_rating_8=unexp_find_rating_9,unexp_find_rating_9=unexp_find_rating_9,unexp_find_rating_10=unexp_find_rating_10,
    unexp_recom_rating_1=unexp_recom_rating_1,unexp_recom_rating_2=unexp_recom_rating_2,unexp_recom_rating_3=unexp_recom_rating_3,unexp_recom_rating_4=unexp_recom_rating_4,unexp_recom_rating_5=unexp_recom_rating_5,unexp_recom_rating_6=unexp_recom_rating_6,unexp_recom_rating_7=unexp_recom_rating_7,unexp_recom_rating_8=unexp_recom_rating_8,unexp_recom_rating_9=unexp_recom_rating_9,unexp_recom_rating_10=unexp_recom_rating_10,
    diversity_rating_1=diversity_rating_1,diversity_rating_2=diversity_rating_2,diversity_rating_3=diversity_rating_3,diversity_rating_4=diversity_rating_4,diversity_rating_5=diversity_rating_5,diversity_rating_6=diversity_rating_6,diversity_rating_7=diversity_rating_7,diversity_rating_8=diversity_rating_8,diversity_rating_9=diversity_rating_9,diversity_rating_10=diversity_rating_10,
    unexp_implic_1=unexp_implic_1, unexp_implic_2=unexp_implic_2,unexp_implic_3=unexp_implic_3,unexp_implic_4=unexp_implic_4,unexp_implic_5=unexp_implic_5,unexp_implic_6=unexp_implic_6,unexp_implic_7=unexp_implic_7,unexp_implic_8=unexp_implic_8,unexp_implic_9=unexp_implic_9,unexp_implic_10=unexp_implic_10)
    session.add(user_rating)
    session.commit()


def add_feedback(user_id,novelty,unexpectedness,satisfaction,recommendation, overall_unexp_implicit):
    new_feedback = Feedback(user_id=user_id,novelty=novelty, unexpectedness=unexpectedness, satisfaction=satisfaction, recommendation=recommendation, overall_unexp_implicit=overall_unexp_implicit)
    session.add(new_feedback)
    session.commit()


def add_within_feedback(user_id,within_unexp_find, within_unexp_implicit, within_novel, within_diversity, within_satisfaction, any_feedback):
    new_within_feedback = Within_feedback(user_id=user_id,within_unexp_find=within_unexp_find, within_unexp_implicit=within_unexp_implicit, within_novel=within_novel,
    within_diversity=within_diversity, within_satisfaction=within_satisfaction,any_feedback=any_feedback)
    session.add(new_within_feedback)
    session.commit()



def add_cart(user_id, item_id):
    cart = ShoppingCart(user_id=user_id, item_id=item_id)
    session.add(cart)
    session.commit()


def delete_cart(user_id, item_id):
    del_cart = ShoppingCart(user_id=user_id, item_id=item_id)
    session.expunge(del_cart)
    session.commit()


# def view_cart(user_id, item_id):
#     viewer = ShoppingCart.query.filter_by(user_id=user_id, item_id=item_id).first()
#     return viewer

def view_shoppingcart(id):
    cart = ShoppingCart.query.filter_by(id=id).first()
    # cart = ShoppingCart.query.filter_by(id=id).first()
    return cart



# only to create Database
def create_tables():
    Base.metadata.create_all(engine)

def main():
    create_tables()

if __name__ == "__main__":
    main()
