
"""
based on the Example flask-based web application.
See the README.md file for instructions how to set up and run the app in development mode.

Rins Note: 装了flask bson dotenv 就可以用python test.py 跑了。网站地址是 http://127.0.0.1:5000
那些comment掉的东西我都还没测过
.env 的配置是：
FLASK_ENV=development
FLASK_PORT=5000
"""

import os
import datetime
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, dotenv_values

load_dotenv()  # load environment variables from .env file


def create_app():
    """
    Create and configure the Flask application.
    returns: app: the Flask application object
    """

    app = Flask(__name__)
    # load flask config from env variables
    config = dotenv_values()
    app.config.from_mapping(config)

    # cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
    # db = cxn[os.getenv("MONGO_DBNAME")]

    # try:
    #     cxn.admin.command("ping")
    #     print(" *", "Connected to MongoDB!")
    # except Exception as e:
    #     print(" * MongoDB connection error:", e)

<<<<<<< HEAD
    @app.route("/",methods = ["POST","GET"])
    def home():
        message_from_req= request.form.get('message')
        if(message_from_req==None):
            message_from_req = request.args.get('message', '')
            
        return render_template("rinbase.html",message=message_from_req)
=======
    @app.route("/")
    def home():

        return render_template("rinbase.html")
>>>>>>> 4afb7ef11f5d072f7b170488e1f4d879cf7d76b4
    
    @app.route("/login",methods=["POST","GET"])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get("email")
            usertype= request.form.get("isAdmin")#如果是admin，值=="on"; 如果不是admin, 值==None
            #login process

            #if login successfully as a guest
            if (usertype==None):
                return redirect(url_for("aptlist"))
            elif (usertype=="on"):
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("message",message="login failed"))
            
            
        return render_template("login.html")
    
    @app.route("/register",methods=["POST","GET"])
    def register():
        return render_template("register.html")


    
    @app.route("/profile")
    def profile():
        return render_template("profile.html", 
                               userInfo={
                                   "username":"Rin",
                                   "usertype":0,
                                   "avatar":"",
                                   "email":"yq2290@nyu.edu"
                               },
                               houseInfo=[{
                                "building": "Jackson Park",
                                "apt_num": "#512",
                                "price": 1350.50,
                                "bedroom": "2",
                                "bathroom": "2",
                                "area": "1200",
                                "available_date": "2025-06-01",
                                "city":"Long Island City, NY 11101"
                               },
                               {
                                "building": "Tower 28",
                                "apt_num": "#5312",
                                "price": 1000.,
                                "bedroom": "1",
                                "bathroom": "2",
                                "area": "1400",
                                "available_date": "2025-06-01",
                                "city":"Long Island City, NY 11101"
                               },
                               {
                                "building": "Jackson f",
                                "apt_num": "#512",
                                "price": 1350.50,
                                "bedroom": "Studio",
                                "bathroom": "Studio",
                                "area": "12020",
                                "available_date": "2025-03-01",
                                "city":"Jercey City, NJ 11101"
                               },
                               {
                                "building": "Tower 28",
                                "apt_num": "#5312",
                                "price": 1000.,
                                "bedroom": "1",
                                "bathroom": "2",
                                "area": "1400",
                                "available_date": "2025-06-01",
                                "city":"Long Island City, NY 11101"
                               },
                               {
                                "building": "Tower 28",
                                "apt_num": "#5312",
                                "price": 1000.,
                                "bedroom": "1",
                                "bathroom": "2",
                                "area": "1400",
                                "available_date": "2025-06-01",
                                "city":"Long Island City, NY 11101"
                               },])
       

    @app.route("/admin_dashboard")
    def admin_dashboard():
        return render_template("admin-dashboard.html")

    @app.route("/userlist", methods=["GET"])
    def userlist():
        query = request.args.get('q', '')  # Retrieve the 'q' parameter, default to empty string if not provided
        print(f"userlist requests for q: {query}") 
        return render_template("userlist.html", target = query,
                               usersInfo=[{
                                   "username":"Rin",
                                   "usertype":0,
                                   "avatar":"",
                                   "email":"yq2290@nyu.edu"
                               },{
                                   "username":"Cindy",
                                   "usertype":1,
                                   "avatar":"",
                                   "email":"12341241@nyu.edu"
                               },{
                                   "username":"Hang",
                                   "usertype":0,
                                   "avatar":"",
                                   "email":"safsfd@nyu.edu"
                               },{
                                   "username":"Hang",
                                   "usertype":0,
                                   "avatar":"",
                                   "email":"safsfd@nyu.edu"
                               },{
                                   "username":"Hang",
                                   "usertype":0,
                                   "avatar":"",
                                   "email":"safsfd@nyu.edu"
                               }],)
    
    @app.route("/search_user")
    def search_user():
        return render_template("search-user.html")
<<<<<<< HEAD
    
    @app.route("/detail/<apt_id>", methods=["GET"])
    def detail(apt_id):
        return render_template("detail.html",user = {"username": "JohnDoe"},
                                apt = {"id": "101dafsdfasdfeafdr2eqr",
                                "street_address": "123 Main St",
                                "city_address": "New York, NY 10001",
                                "apt_num": "16K",
                                "price":1350,
                                "bedroom":1,
                                "bathroom":1,
                                "area":1,
                                "date":"05/16/2025",
                                "postperson":"Rin",
                                "about_info": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In at sem cursus, fringilla lectus eu, ultrices dolor. Nam consequat metus libero, viverra tincidunt tortor efficitur porta. In id volutpat arcu. Proin gravida massa ut tincidunt egestas. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam vitae mollis mi. Integer lacus augue, tristique non tristique finibus, venenatis vitae eros. In hac habitasse platea dictumst. Ut laoreet, felis eu mattis tempus, lacus felis placerat justo, nec vehicula risus orci non orci. Quisque sodales eros a accumsan tristique. Ut efficitur nunc nec neque euismod, quis posuere ex molestie. Duis gravida vulputate posuere. Duis lacinia, magna ac elementum feugiat, lectus tellus pulvinar orci, eu viverra nulla velit ac felis. Etiam egestas quam ac orci gravida lacinia. Suspendisse sagittis nisi mauris, sed hendrerit velit imperdiet ac. Maecenas nec eleifend dolor.",
                                "policies": {
                                    "pet_allowed": 1,
                                    "guarantor_accepted": 1,
                                    "smoke_free": 1
                                },
                                "amenities": {
                                    "doorman": 1,
                                    "bikeroom": 1,
                                    "elevator": 1,
                                    "laundry": 1,
                                    "gym": 1,
                                    "package_room": 0,
                                    "parking": 1,
                                    "library": 1
                                },
                                "features": {
                                    "centralair": 1,
                                    "dishwasher": 1,
                                    "view": 1,
                                    "hardwoodfloor": 1,
                                    "fridge": 1,
                                    "privateoutdoor": 1,
                                    "oven": 1,
                                    "washerdryer": 1
                                },
                                "building":{
                                    "name":"Luxury High-Rise Apartment",
                                    "num_unit": 123213,
                                    "address":"building address",
                                    "about_info":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. In at sem cursus, fringilla lectus eu, ultrices dolor. Nam consequat metus libero, viverra tincidunt tortor efficitur porta. In id volutpat arcu. "
                                }})
=======
>>>>>>> 4afb7ef11f5d072f7b170488e1f4d879cf7d76b4

    @app.route("/aptlist",methods=["GET"])
    def aptlist():
        query = request.args.get('q', '')  # Retrieve the 'q' parameter, default to empty string if not provided
        print(f"userlist requests for q: {query}") 
        return render_template("aptlist.html",target = query,
                               houseInfo=[{
                                "building": "Jackson Park",
                                "apt_num": "#512",
                                "price": 1350.50,
                                "bedroom": "2",
                                "bathroom": "2",
                                "area": "1200",
                                "available_date": "2025-06-01",
                                "city":"Long Island City, NY 11101"
                               },
                               {
                                "building": "Tower 28",
                                "apt_num": "#5312",
                                "price": 1000.,
                                "bedroom": "1",
                                "bathroom": "2",
                                "area": "1400",
                                "available_date": "2025-06-01",
                                "city":"Long Island City, NY 11101"
                               },
                               {
                                "building": "Jackson f",
                                "apt_num": "#512",
                                "price": 1350.50,
                                "bedroom": "Studio",
                                "bathroom": "Studio",
                                "area": "12020",
                                "available_date": "2025-03-01",
                                "city":"Jercey City, NJ 11101"
                               },
                               {
                                "building": "Tower 28",
                                "apt_num": "#5312",
                                "price": 1000.,
                                "bedroom": "1",
                                "bathroom": "2",
                                "area": "1400",
                                "available_date": "2025-06-01",
                                "city":"Long Island City, NY 11101"
                               },
                               {
                                "building": "Tower 28",
                                "apt_num": "#5312",
                                "price": 1000.,
                                "bedroom": "1",
                                "bathroom": "2",
                                "area": "1400",
                                "available_date": "2025-06-01",
                                "city":"Long Island City, NY 11101"
                               },
                               {
                                "building": "Tower 28",
                                "apt_num": "#5312",
                                "price": 1000.,
                                "bedroom": "1",
                                "bathroom": "2",
                                "area": "1400",
                                "available_date": "2025-06-01",
                                "city":"Long Island City, NY 11101"
                               },])
    
    @app.route("/delete/<user_id>", methods=['POST'])
    def delete_user_q(user_id):
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get("email")
            # process the submitted data here
            print(f"Received username: {username}")
            print(f"Received email: {email}")


        print("req post for delete user from Userlist")
<<<<<<< HEAD
        return render_template("delete-user.html", q_message = "Are you sure that you want to detele this user?",
=======
        return render_template("delete-user.html", q_message = "Are you sure that you want to detele this user",
>>>>>>> 4afb7ef11f5d072f7b170488e1f4d879cf7d76b4
                               username=username,
                               email=email)
    

    @app.route("/delete/<user_id>", methods=['GET'])
    def delete_user(user_id):
        print("req get for delete user from Userlist")
        return render_template("delete-user.html", username=user_id)
    
<<<<<<< HEAD
    @app.route("/delete/apt/<apt_id>", methods=['POST'])
    def delete_apt_q(apt_id):
        if request.method == 'POST':
            apt_id = request.form.get('apt_id')
            # process the submitted data here
            print(f"Received apt_id: {apt_id}")


        print("req post for delete apt from Aptlist")
        return render_template("delete-apt.html", q_message = "Are you sure that you want to detele this apartment?",
                               apt={
                                "building": "Jackson Park",
                                "apt_num": "#512",
                                "price": 1350.50,
                                "bedroom": "2",
                                "bathroom": "2",
                                "area": "1200",
                                "available_date": "2025-06-01",
                                "city":"Long Island City, NY 11101"
                               })
    

=======
>>>>>>> 4afb7ef11f5d072f7b170488e1f4d879cf7d76b4
    @app.route("/message", methods=['POST','GET'])
    def message():
        message_from_req= request.form.get('message')
        if(message_from_req==None):
            message_from_req = request.args.get('message', '')
        
        print("message",message_from_req)
        redirectAddress=url_for("home")

        if message_from_req == "User Deleted":
            username = request.form.get('username')
            email = request.form.get("email")
            redirectAddress=url_for("userlist")

            # do something in backend to deleted the user
            # can retrieve user id if needed
            # if success, proceed with message user deleted
            # else, change the message and show the user that the deletion failed
<<<<<<< HEAD
# 
        if message_from_req == "Apartment Deleted":
            # id = request.form.get('id')
            redirectAddress=url_for("aptlist")

            # do something in backend to deleted the user
            # can retrieve user id if needed
            # if success, proceed with message user deleted
            # else, change the message and show the user that the deletion failed
=======
>>>>>>> 4afb7ef11f5d072f7b170488e1f4d879cf7d76b4

        if message_from_req == "Registration Sucessful":
            username = request.form.get('username')
            email = request.form.get("email")
            password = request.form.get("password")
            usertype= request.form.get("isAdmin")#如果是admin，值=="on"; 如果不是admin, 值==None

            print("POST method from register page")
            print(f"Received username: {username}")
            print(f"Received email: {email}")
            print(f"Received password: {password}")
            print(f"Received usertype: {usertype}") #
            
            redirectAddress=url_for("login")
            # process the submitted data here
        
        
        
        return render_template("message.html", redirectWebsite=redirectAddress,
                               message=message_from_req)
    










    # @app.route("/create", methods=["POST"])
    # def create_post():
    #     """
    #     Route for POST requests to the create page.
    #     Accepts the form submission data for a new document and saves the document to the database.
    #     Returns:
    #         redirect (Response): A redirect response to the home page.
    #     """
    #     name = request.form["fname"]
    #     message = request.form["fmessage"]

    #     doc = {
    #         "name": name,
    #         "message": message,
    #         "created_at": datetime.datetime.utcnow(),
    #     }
    #     db.messages.insert_one(doc)

    #     return redirect(url_for("home"))

    # @app.route("/edit/<post_id>")
    # def edit(post_id):
    #     """
    #     Route for GET requests to the edit page.
    #     Displays a form users can fill out to edit an existing record.
    #     Args:
    #         post_id (str): The ID of the post to edit.
    #     Returns:
    #         rendered template (str): The rendered HTML template.
    #     """
    #     doc = db.messages.find_one({"_id": ObjectId(post_id)})
    #     return render_template("edit.html", doc=doc)

    # @app.route("/edit/<post_id>", methods=["POST"])
    # def edit_post(post_id):
    #     """
    #     Route for POST requests to the edit page.
    #     Accepts the form submission data for the specified document and updates the document in the database.
    #     Args:
    #         post_id (str): The ID of the post to edit.
    #     Returns:
    #         redirect (Response): A redirect response to the home page.
    #     """
    #     name = request.form["fname"]
    #     message = request.form["fmessage"]

    #     doc = {
    #         "name": name,
    #         "message": message,
    #         "created_at": datetime.datetime.utcnow(),
    #     }

    #     db.messages.update_one({"_id": ObjectId(post_id)}, {"$set": doc})

    #     return redirect(url_for("home"))

    # @app.route("/delete/<post_id>")
    # def delete(post_id):
    #     """
    #     Route for GET requests to the delete page.
    #     Deletes the specified record from the database, and then redirects the browser to the home page.
    #     Args:
    #         post_id (str): The ID of the post to delete.
    #     Returns:
    #         redirect (Response): A redirect response to the home page.
    #     """
    #     db.messages.delete_one({"_id": ObjectId(post_id)})
    #     return redirect(url_for("home"))

    # @app.route("/delete-by-content/<post_name>/<post_message>", methods=["POST"])
    # def delete_by_content(post_name, post_message):
    #     """
    #     Route for POST requests to delete all post by their author's name and post message.
    #     Deletes the specified record from the database, and then redirects the browser to the home page.
    #     Args:
    #         post_name (str): The name of the author of the post.
    #         post_message (str): The contents of the message of the post.
    #     Returns:
    #         redirect (Response): A redirect response to the home page.
    #     """
    #     db.messages.delete_many({"name": post_name, "message": post_message})
    #     return redirect(url_for("home"))

    # @app.errorhandler(Exception)
    # def handle_error(e):
    #     """
    #     Output any errors - good for debugging.
    #     Args:
    #         e (Exception): The exception object.
    #     Returns:
    #         rendered template (str): The rendered HTML template.
    #     """
    #     return render_template("error.html", error=e)

    return app


app = create_app()

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "6000")
    FLASK_ENV = os.getenv("FLASK_ENV")
    print(f"FLASK_ENV: {FLASK_ENV}, FLASK_PORT: {FLASK_PORT}")
    app.run(port=FLASK_PORT)