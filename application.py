


# importing the model file and required packages for the platform. Primarily includes flask and sqlalchemy modules

from flask import Flask, render_template, redirect, request, flash, session, url_for
import model
from sqlalchemy.orm import joinedload
from sqlalchemy import text
# from planout.experiment import SimpleExperiment
# from planout.ops.random import *
from random import randint, choice
import random



# import install_surprise

# importing the recommenders. Each module is linked to a .py file with the same name


# These recommenders do not need the surprise library installed....................................
import recommender1_random
import recommender2_topitems

# import surprise
# These recommenders need the surprise library installed.............................................
# import recommender3_svd
# import recommender4_knn
# import recommender5_nmf
# import recommender6_slopeone
# import recommender7_baseline
# import recommender8_normal


application = Flask(__name__)
app = application
app.secret_key = '23987ETFSDDF345560DFSASF45DFDF567'

@app.route("/")
def index():
    # return 'hello'
    return render_template("index.html")



# Decorator for the login, signup and instructions pages. Each decorator may point to either an update action (e.g filling in signup/login forms) or an
# HTML page found in the templates folder.


@app.route("/install")
def install_surprise():
    import install_surprise
    # model.add_pageview(user_id=None, item_id=None, page="Module Install", activity_type="Installed Surprise Module")

    return render_template("surprise_install.html")


@app.route("/login")
def show_login():
    model.add_pageview(user_id=None, item_id=None, page="login", activity_type="enter login page",rating=None) #pageview
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = model.get_user_from_email(email)

    if user == None:
        flash ("This user is not registered yet")
        model.add_pageview(user_id=None, item_id=None, page="login", activity_type="non-registered id / incorrect details",rating=None) #pageview
        return redirect('signup')
    else:
        session['user'] = user.id
        model.add_pageview(user_id=user.id, item_id=None, page="login", activity_type="successful login",rating=None) #pageview
        # return redirect(url_for('show_user_details', id=user.id))
        # model.add_pageview(user_id=user.id, item_id=None, page="login", activity_type="to Instructions page",rating=None) #pageview
        return redirect(url_for('instructions', id=user.id))



@app.route("/instructions")
def instructions():
    model.add_pageview(user_id=session["user"], item_id=None, page="feedback", activity_type="start viewing instructions", rating=None) #pageview
    return render_template("instructions.html")



@app.route("/signup")
def show_signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def make_new_account():
    email = request.form.get("email")
    password = request.form.get("password")
    turk_id = request.form.get("turk_id")
    age = request.form.get("age")
    gender = request.form.get("gender")
    occupation = request.form.get("occupation")
    state = request.form.get("state")
    country = request.form.get("country")
    model.create_user(email, password,turk_id, age, gender,occupation, state, country)
    model.add_pageview(user_id=None, item_id=None, page="signup", activity_type="successful signup",rating=None) #pageview
    flash ("You're registered! Now please log in")
    return redirect('/login')


@app.route("/user_list/", defaults={"page":1})
@app.route("/user_list/<int:page>")
def user_list(page):
    perpage = 50
    pages = (model.session.query(model.User).count()) / perpage
    back_one = page - 1
    forward_one = page + 1
    user_list = model.session.query(model.User).limit(perpage).offset((page*perpage) -perpage).all()
    return render_template("user_list.html", users=user_list, pages=pages, back=back_one, forward=forward_one)


# Decorator for the user-items pages. Various attributes are queried for each item and show on the respective pages.
# view_item shows a more detailed item view

@app.route("/view_user/<int:id>")
def show_user_details(id):
    user_id = session["user"]
    model.add_pageview(user_id=user_id, item_id=None, page="Movie List", activity_type="enter Movie List",rating=None) #pageview
    user = model.session.query(model.User).filter_by(id=id).join(model.Rating).join(model.Item).first()
    ratings = model.session.query(model.Rating).options(joinedload(model.Rating.item)).filter_by(user_id=id).all()
    return render_template("view_user.html", user=user, ratings=ratings)

@app.route("/algo")
def view_algo():
    algo1_id = model.show_current_algo(1)
    model.add_pageview(user_id=None, item_id=None, page="current_recommender", activity_type= 'current recommender 1 is ' + str(algo1_id[0].algorithm)[13:].upper(), rating=None) #pageview
    algo2_id = model.show_current_algo(2)
    model.add_pageview(user_id=None, item_id=None, page="current_recommender", activity_type= 'current recommender 2 is ' + str(algo2_id[0].algorithm)[13:].upper(), rating=None) #pageview
    # algo1 = algo1_id[0]
    # algo_11 = model.update_current_algo(2)


    # model.add_pageview(user_id=session["user"], item_id=item.id, page="item", activity_type="start item view",rating=None) #pageview
    return render_template("algo.html", algo1_id=algo1_id, algo2_id=algo2_id) #prediction_items=prediction_items,


@app.route("/update_algo", methods=["POST"])
def update_algo():
    algorithm_1 = request.form.get("algorithm_1")
    algorithm_2 = request.form.get("algorithm_2")

    model.update_current_algo(id=1, algorithm=algorithm_1)
    model.update_current_algo(id=2, algorithm=algorithm_2)
    model.add_pageview(user_id=None, item_id=None, page="update_recommender", activity_type= 'updated recommenders', rating=None) #pageview

    # model.add_pageview(user_id=session["user"], item_id=item_id, page="item", activity_type="end item view",rating=None) #pageview
    flash ("You've changed algorithms")
    return redirect(url_for('view_algo'))











@app.route("/view_item/<int:id>")
def view_item_details(id):
    item_ratings = model.show_item_details(id)
    item = item_ratings[0].item
    model.add_pageview(user_id=session["user"], item_id=item.id, page="item", activity_type="start item view",rating=None) #pageview
    return render_template("view_item.html", item=item) #prediction_items=prediction_items,


# Update_rating updates the rating for each item

@app.route("/update_rating", methods=["POST"])
def update_rating():
    new_rating = request.form.get("rating")
    item_id = request.form.get("item")
    new_text_rating = request.form.get("text_rating")
    user_id = session['user']
    model.update_rating(user_id, item_id, new_rating,new_text_rating)
    model.add_pageview(user_id=session["user"], item_id=item_id, page="item", activity_type="rate item",rating=new_rating) #pageview
    model.add_pageview(user_id=session["user"], item_id=item_id, page="item", activity_type="end item view",rating=None) #pageview
    flash ("You've changed your rating for an item")
    return redirect(url_for('show_user_details', id=user_id))

# Decorator for cart activity. Not used in current application version.

@app.route("/add_cart", methods=["POST"])
def cart_update():
    user_id = session['user']
    item_id = request.form.get("item")
    model.add_cart(user_id, item_id)
    model.add_pageview(user_id=session["user"], item_id=item_id, page="cart", activity_type="add to cart",rating=None) #pageview
    flash ("You've added to your shopping cart!")
    return redirect(url_for('show_user_details', id=user_id))


# This decorator is used to run the recommenders when the user clicks on the calculate and show recommmendations button

# It starts by capturing the click itself, and then deletes previous recommendations corresponding to that user (they are stil stored in the ....... tablee)



@app.route("/recommend_compute/<int:id>")
def recsys_compute(id):
    user_id = session['user']
    model.add_pageview(user_id=session["user"], item_id=None, page="recommender_algorithm", activity_type="initialize recommender", rating=None) #pageview
    model.delete_recommendations1()
    model.delete_recommendations2()
    model.delete_numeric_predictions1()
    model.delete_numeric_predictions2()

# A/B Testng and algorithm randomization. Since we have to randomize which algorithm recommendentations to show first, a list of lists is used
# for random selection. The results are then appended to two separate tables depending on the algorithm.

# HERE algorithm 1 is recommender3_svd
# HERE algorithm 2 is recommender4_knn

    select_list = [[1,2], [2,1]]
    selector = random.choice(select_list)

    if selector[0] == 1:
        # Run algorithm 1 first
        algo1_id = model.show_current_algo(1)
        recommender1 = __import__(algo1_id[0].algorithm)

        recommender1.compute_recommendations(user_id=user_id, prediction_table='recommendations1', numeric_prediction_table='transposed_prediction1')
        model.add_algo(user_id=user_id, algorithm=str(algo1_id[0].algorithm)[13:].upper())
        model.add_pageview(user_id=session["user"], item_id=None, page="recommender_algorithm", activity_type= 'used recommender ' + str(algo1_id[0].algorithm)[13:].upper(), rating=None) #pageview


        # Run algorithm 2

        algo2_id = model.show_current_algo(2)
        recommender2 = __import__(algo2_id[0].algorithm)

        recommender2.compute_recommendations(user_id=user_id, prediction_table='recommendations2', numeric_prediction_table='transposed_prediction2')
        model.add_algo(user_id=user_id, algorithm=str(algo2_id[0].algorithm)[13:].upper())
        model.add_pageview(user_id=session["user"], item_id=None, page="recommender_algorithm", activity_type= 'used recommender ' + str(algo2_id[0].algorithm)[13:].upper(), rating=None) #pageview
    else:
        algo2_id = model.show_current_algo(2)
        recommender2 = __import__(algo2_id[0].algorithm)

        recommender2.compute_recommendations(user_id=user_id, prediction_table='recommendations1', numeric_prediction_table='transposed_prediction1')
        model.add_algo(user_id=user_id, algorithm=str(algo2_id[0].algorithm)[13:].upper())
        model.add_pageview(user_id=session["user"], item_id=None, page="recommender_algorithm", activity_type= 'used recommender ' + str(algo2_id[0].algorithm)[13:].upper(), rating=None) #pageview

        # Run algorithm 1
        algo1_id = model.show_current_algo(1)
        recommender1 = __import__(algo1_id[0].algorithm)

        recommender1.compute_recommendations(user_id=user_id, prediction_table='recommendations2', numeric_prediction_table='transposed_prediction2')
        model.add_algo(user_id=user_id, algorithm=str(algo1_id[0].algorithm)[13:].upper())
        model.add_pageview(user_id=session["user"], item_id=None, page="recommender_algorithm", activity_type= 'used recommender ' + str(algo1_id[0].algorithm)[13:].upper(), rating=None) #pageview


    model.add_pageview(user_id=session["user"], item_id=None, page="recommender_algorithm", activity_type="finish recommender computation", rating=None) #pageview
    flash ("You've computed Recommendations! Please dont re-run until new recommendations are required!!")
    # return render_template("recommendations.html", id=id)
    return redirect(url_for('view_recommendations', id=id))


# Showing recommendations. Top 10 are taken by prediction value.

@app.route("/view_recommendations/<int:id>")
def view_recommendations(id):
    rec,pred_1, pred_2, pred_3, pred_4, pred_5, pred_6,pred_7, pred_8, pred_9,pred_10 = model.show_recommendations1(id)
    tp_1=model.show_transposed_prediction1(id)
    model.add_pageview(user_id=session["user"], item_id=None, page="recommendations", activity_type="start viewing recommendations", rating=None) #pageview
    return render_template("recommendations.html", id=id, rec=rec, pred_1=pred_1, pred_2=pred_2,pred_3=pred_3, pred_4=pred_4,pred_5=pred_5, pred_6=pred_6, pred_7=pred_7, pred_8=pred_8, pred_9=pred_9, pred_10=pred_10, tp_1=tp_1)


# @app.route("/view_recommendations/<int:id>")
# def view_recommendations(id):
#     model1_rec,model1_pred_1, model1_pred_2, model1_pred_3, model1_pred_4, model1_pred_5, model1_pred_6,model1_pred_7, model1_pred_8, model1_pred_9,model1_pred_10 = model.show_recommendations1(id)
#     model2_rec,model2_pred_1, model2_pred_2, model2_pred_3, model2_pred_4, model2_pred_5, model2_pred_6,model2_pred_7, model2_pred_8, model2_pred_9,model2_pred_10 = model.show_recommendations2(id)
#     model.add_pageview(user_id=session["user"], item_id=None, page="recommendations", activity_type="start viewing recommendations", rating=None) #pageview
#     return render_template("recommendations.html", id=id, model1_rec=model1_rec,model1_pred_1=model1_pred_1, model1_pred_2=model1_pred_2, model1_pred_3=model1_pred_3, model1_pred_4=model1_pred_4, model1_pred_5=model1_pred_5, model1_pred_6=model1_pred_6,model1_pred_7=model1_pred_7, model1_pred_8=model1_pred_8, model1_pred_9=model1_pred_9,model1_pred_10=model1_pred_10,
#     model2_rec=model2_rec,model2_pred_1=model2_pred_1, model2_pred_2=model2_pred_2, model2_pred_3=model2_pred_3, model2_pred_4=model2_pred_4, model2_pred_5=model2_pred_5, model2_pred_6=model2_pred_6, model2_pred_7=model2_pred_7, model2_pred_8=model2_pred_8, model2_pred_9=model2_pred_9,model2_pred_10=model2_pred_10)

@app.route("/view_recommended_item/<int:id>")
def view_recommended_item_details(id):
    item_ratings = model.show_item_details(id)
    item = item_ratings[0].item
    model.add_pageview(user_id=session["user"], item_id=item.id, page="item", activity_type="recommended item view",rating=None) #pageview
    return render_template("view_recommended_item.html", item=item) #prediction_items=prediction_items,


# Decorators for user feedback for recommendations. Include per-recommendation, overall and per-algorithm feedback

@app.route("/rate_recommendations", methods=["POST"])
def add_rec_rating():
    user_id = session['user']
    user_rating_1 = request.form.get("user_rating_1")
    novel_rating_1 = request.form.get("novel_rating_1")
    unexp_find_rating_1 = request.form.get("unexp_find_rating_1")
    unexp_recom_rating_1 = request.form.get("unexp_recom_rating_1")
    diversity_rating_1 = request.form.get("diversity_rating_1")
    diversity_rating_1 = request.form.get("diversity_rating_1")

    user_rating_2 = request.form.get("user_rating_2")
    novel_rating_2 = request.form.get("novel_rating_2")
    unexp_find_rating_2 = request.form.get("unexp_find_rating_2")
    unexp_recom_rating_2 = request.form.get("unexp_recom_rating_2")
    diversity_rating_2 = request.form.get("diversity_rating_2")

    user_rating_3 = request.form.get("user_rating_3")
    novel_rating_3 = request.form.get("novel_rating_3")
    unexp_find_rating_3 = request.form.get("unexp_find_rating_3")
    unexp_recom_rating_3 = request.form.get("unexp_recom_rating_3")
    diversity_rating_3 = request.form.get("diversity_rating_3")

    user_rating_4 = request.form.get("user_rating_4")
    novel_rating_4 = request.form.get("novel_rating_4")
    unexp_find_rating_4= request.form.get("unexp_find_rating_4")
    unexp_recom_rating_4 = request.form.get("unexp_recom_rating_4")
    diversity_rating_4 = request.form.get("diversity_rating_4")

    user_rating_5 = request.form.get("user_rating_5")
    novel_rating_5 = request.form.get("novel_rating_5")
    unexp_find_rating_5= request.form.get("unexp_find_rating_5")
    unexp_recom_rating_5 = request.form.get("unexp_recom_rating_5")
    diversity_rating_5 = request.form.get("diversity_rating_5")

    user_rating_6 = request.form.get("user_rating_6")
    novel_rating_6 = request.form.get("novel_rating_6")
    unexp_find_rating_6= request.form.get("unexp_find_rating_6")
    unexp_recom_rating_6 = request.form.get("unexp_recom_rating_6")
    diversity_rating_6 = request.form.get("diversity_rating_6")

    user_rating_7 = request.form.get("user_rating_7")
    novel_rating_7 = request.form.get("novel_rating_7")
    unexp_find_rating_7= request.form.get("unexp_find_rating_7")
    unexp_recom_rating_7 = request.form.get("unexp_recom_rating_7")
    diversity_rating_7 = request.form.get("diversity_rating_7")

    user_rating_8 = request.form.get("user_rating_8")
    novel_rating_8 = request.form.get("novel_rating_8")
    unexp_find_rating_8= request.form.get("unexp_find_rating_8")
    unexp_recom_rating_8 = request.form.get("unexp_recom_rating_8")
    diversity_rating_8 = request.form.get("diversity_rating_8")

    user_rating_9 = request.form.get("user_rating_9")
    novel_rating_9 = request.form.get("novel_rating_9")
    unexp_find_rating_9= request.form.get("unexp_find_rating_9")
    unexp_recom_rating_9 = request.form.get("unexp_recom_rating_9")
    diversity_rating_9 = request.form.get("diversity_rating_9")

    user_rating_10 = request.form.get("user_rating_10")
    novel_rating_10 = request.form.get("novel_rating_10")
    unexp_find_rating_10= request.form.get("unexp_find_rating_10")
    unexp_recom_rating_10 = request.form.get("unexp_recom_rating_10")
    diversity_rating_10 = request.form.get("diversity_rating_10")

    unexp_implic_1 = request.form.get("unexp_implic_1")
    unexp_implic_2 = request.form.get("unexp_implic_2")
    unexp_implic_3 = request.form.get("unexp_implic_3")
    unexp_implic_4 = request.form.get("unexp_implic_4")
    unexp_implic_5 = request.form.get("unexp_implic_5")
    unexp_implic_6 = request.form.get("unexp_implic_6")
    unexp_implic_7 = request.form.get("unexp_implic_7")
    unexp_implic_8 = request.form.get("unexp_implic_8")
    unexp_implic_9 = request.form.get("unexp_implic_9")
    unexp_implic_10 = request.form.get("unexp_implic_10")


    model.add_rec_rating(user_id,user_rating_1,user_rating_2,user_rating_3,user_rating_4,user_rating_5,user_rating_6,user_rating_7,user_rating_8,user_rating_9,user_rating_10)
    model.add_user_rating(user_id,novel_rating_1,novel_rating_2,novel_rating_3,novel_rating_4,novel_rating_5,novel_rating_6,novel_rating_7,novel_rating_8,novel_rating_9,novel_rating_10,
        unexp_find_rating_1,unexp_find_rating_2,unexp_find_rating_3,unexp_find_rating_4,unexp_find_rating_5,unexp_find_rating_6,unexp_find_rating_7,unexp_find_rating_8,unexp_find_rating_9,unexp_find_rating_10,
        unexp_recom_rating_1,unexp_recom_rating_2,unexp_recom_rating_3,unexp_recom_rating_4,unexp_recom_rating_5,unexp_recom_rating_6,unexp_recom_rating_7,unexp_recom_rating_8,unexp_recom_rating_9,unexp_recom_rating_10,
        diversity_rating_1,diversity_rating_2,diversity_rating_3,diversity_rating_4,diversity_rating_5,diversity_rating_6,diversity_rating_7,diversity_rating_8,diversity_rating_9,diversity_rating_10,
        unexp_implic_1,unexp_implic_2,unexp_implic_3,unexp_implic_4,unexp_implic_5,unexp_implic_6,unexp_implic_7,unexp_implic_8,unexp_implic_9,unexp_implic_10)

    model.add_pageview(user_id=session["user"], item_id=None, page="recommendations", activity_type="rate recommendations and finish view", rating=None) #pageview
    flash ("You've rated your recommendations!Thank you for the feedback!")
    return redirect(url_for('to_overall_feedback', id=user_id))


# Overall feedback page

@app.route("/overall_feedback")
def to_overall_feedback():
    model.add_pageview(user_id=session["user"], item_id=None, page="feedback", activity_type="start viewing overall feedback", rating=None) #pageview
    return render_template("feedback.html")


@app.route("/overall_feedback", methods=["POST"])
def overall_feedback():
    user_id = session['user']
    novelty = request.form.get("novelty")
    unexpectedness = request.form.get("unexpectedness")
    satisfaction = request.form.get("satisfaction")
    recommendation = request.form.get("recommendation")
    overall_unexp_implicit = request.form.get("overall_unexp_implicit")

    model.add_feedback(user_id,novelty,unexpectedness,satisfaction,recommendation, overall_unexp_implicit)
    model.add_pageview(user_id=session["user"], item_id=None, page="feedback", activity_type="finish viewing and giving overall feedback", rating=None) #pageview
    flash ("Thank you for the overall feedback!")
    return redirect(url_for('view_combined_recommendations', id=user_id))

# Page for comparison of algorithm 1 vs algorithm 2

@app.route("/view_combined_recommendations/<int:id>")
def view_combined_recommendations(id):
    rec,pred_1, pred_2, pred_3, pred_4, pred_5, pred_6,pred_7, pred_8, pred_9,pred_10 = model.show_recommendations1(id)
    rec2,pred_11, pred_12, pred_13, pred_14, pred_15, pred_16,pred_17, pred_18, pred_19,pred_20 = model.show_recommendations2(id)
    model.add_pageview(user_id=session["user"], item_id=None, page="recommendations", activity_type="start viewing combined recommendations", rating=None) #pageview
    return render_template("combined_recommendations.html", id=id, rec=rec, pred_1=pred_1, pred_2=pred_2,pred_3=pred_3, pred_4=pred_4,pred_5=pred_5, pred_6=pred_6, pred_7=pred_7, pred_8=pred_8, pred_9=pred_9, pred_10=pred_10,
    rec2=rec2,pred_11=pred_11, pred_12=pred_12, pred_13=pred_13, pred_14=pred_14, pred_15=pred_15, pred_16=pred_16,pred_17=pred_17, pred_18=pred_18, pred_19=pred_19,pred_20=pred_20)

@app.route("/within_feedback", methods=["POST"])
def within_feedback():
    user_id = session['user']
    within_unexp_find = request.form.get("within_unexp_find")
    within_unexp_implicit = request.form.get("within_unexp_implicit")
    within_novel = request.form.get("within_novel")
    within_diversity = request.form.get("within_diversity")
    within_satisfaction = request.form.get("within_satisfaction")
    any_feedback = request.form.get("any_feedback")
    model.add_within_feedback(user_id,within_unexp_find, within_unexp_implicit, within_novel, within_diversity, within_satisfaction, any_feedback)
    model.add_pageview(user_id=session["user"], item_id=None, page="within feedback", activity_type="finish the with-effects feedback", rating=None) #pageview
    flash ("Thank you for the feedback, and using the website!")
    return redirect(url_for('show_user_details', id=user_id))


# Cart view actions. Not used in current version
@app.route("/view_cart/<int:id>")
def show_cart_details(id):
    user = model.session.query(model.User).filter_by(id=id).join(model.ShoppingCart).join(model.Item).first()
    shopitem = model.session.query(model.ShoppingCart).options(joinedload(model.ShoppingCart.item)).filter_by(user_id=id).all()
    # ratings = model.session.query(model.Rating).options(joinedload(model.Rating.item)).filter_by(user_id=id).all()
    # return render_template("view_user.html", user=user, ratings=ratings)
    model.add_pageview(user_id=session["user"], item_id=None, page="cart", activity_type="view cart", rating=None) #pageview
    return render_template("shoppercart.html", user=user, shopitem=shopitem)



# page for logout

@app.route("/logout")
def process_logout():
    model.add_pageview(user_id=session["user"], item_id=None, page="logout", activity_type="user logout", rating=None) #pageview
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)


        # recommender3_svd.compute_recommendations(user_id=user_id, prediction_table='recommendations1', numeric_prediction_table='transposed_prediction1')
        # model.add_algo(user_id=user_id, algorithm="SVD")
        # model.add_pageview(user_id=session["user"], item_id=None, page="recommender_algorithm", activity_type="used SVD", rating=None) #pageview
        #
        # recommender4_knn.compute_recommendations(user_id=user_id, prediction_table='recommendations2', numeric_prediction_table='transposed_prediction2')
        # model.add_algo(user_id=user_id, algorithm="Item-based KNN")
        # model.add_pageview(user_id=session["user"], item_id=None, page="recommender_algorithm", activity_type="used Item-based KNN", rating=None) #pageview


        # recommender1_random.compute_recommendations(user_id=user_id, prediction_table='recommendations1')
        # model.add_algo(user_id=user_id, algorithm="Random Items")
        # model.add_pageview(user_id=session["user"], item_id=None, page="recommender_algorithm", activity_type="used Random Items", rating=None) #pageview
        # Run algorithm 2

        # recommender2_topitems.compute_recommendations(user_id=user_id, prediction_table='recommendations2')
        # model.add_algo(user_id=user_id, algorithm="Top Items")
        # model.add_pageview(user_id=session["user"], item_id=None, page="recommender_algorithm", activity_type="used Top Items", rating=None) #pageview
