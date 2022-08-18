from os import rename
import re
from urllib import request
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, session
from datetime import datetime
from flask import url_for


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "23_mars_2000"
db = SQLAlchemy(app)

if __name__ == "__main__":
   db.create_all()
   app.run(debug=True)


class User(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String(255), nullable=False)
      password = db.Column(db.String(255), nullable=False)
      task = db.relationship("Task", backref="user", lazy=True)


class Task(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       title = db.Column(db.String(255), nullable=False)
       description = db.Column(db.Text, nullable=True, default="No description")
       date = db.Column(db.DateTime, default=datetime.now)
       user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
       
       def __repr__(self) -> str:
           return self.title
        



@app.route("/login", methods = ["GET", "POST"])
def login():
   if "username" and "password" in session :
      return redirect("/")
   if request.method == "POST":
      username = request.form['username'] 
      password = request.form['password']
      
      if username == "" or password == "" :
            return redirect("/login")
      
      # voir si user existe , password=password
      if  User.query.filter_by(username=username, password=password).count() > 0:
         session['username'] = username
         session['password'] = password
         user_logged_id = User.query.filter_by(username=username).first().id
         session['user_logged_id'] = user_logged_id
         # print("------------" + session['username'])
         return redirect("/")
      else : 
         session['username'] = username
         session['password'] = password
         db.session.add(User(username=username, password=password))
         db.session.commit()
         user_logged_id = User.query.filter_by(username=username).first().id
         session['user_logged_id'] = user_logged_id
         return redirect("/")
         
   return render_template("login.html", username = session.get('username'))


@app.route("/logout")
def logout():
   session.clear()
   return redirect("/login")



@app.route("/", methods = ["GET", "POST"])
def index():
   
   if "username" and "password"  in session :
       
      if request.method == "POST" :
         title = request.form['title'] 
         description = request.form['description'] 
         user = User.query.filter_by(username=session.get("username")).first()
         # print(user_logged_id)
         task = Task(title=title, description=description, user=user)
         db.session.add(task)
         db.session.commit()
         return redirect("/")
            
      # Filtrer les task en fonction de l'utilisateur connecte  
      user_logged_id = session.get("user_logged_id")
      print(session["user_logged_id"])
      tasks = Task.query.filter_by(user_id=user_logged_id).order_by(Task.date)
      tasks_len = Task.query.filter_by(user_id=user_logged_id).count()
      return render_template("index.html", tasks=tasks, tasks_len=tasks_len)
   
   return redirect("/login")
   


@app.route("/delete/<int:id>/")
def delete(id):
   if "username" and "password"  in session :
      task = Task.query.get_or_404(id)
      db.session.delete(task)
      db.session.commit()
      return redirect("/")
   return redirect("/login")


@app.route("/update/<int:id>/", methods=["POST", "GET"])
def update(id):
   if "username" and "password"  in session :
      task = Task.query.get_or_404(id)
      if request.method == "POST":
         task.title = request.form["title"]
         task.description = request.form["description"]
         db.session.commit()
      else:
         return render_template("update.html", task=task)
      return redirect("/")
   return redirect("/login")


@app.route("/<int:id>/", methods=["GET",])
def detail(id):
   if "username" and "password"  in session :
      task = Task.query.get_or_404(id)
      return render_template("detail.html", task=task)
   return redirect("/login")


@app.route("/contact")
def contact():
   if "username" and "password"  in session :
      return render_template("contact.html")
   return redirect("/login")

@app.route("/about")
def about():
   if "username" and "password"  in session :
      return render_template("about.html")
   return redirect("/login")








db.create_all()

# db.session.add(User(username="serge", password="1234"))
# db.session.add(User(username="eric", password="1234"))
# db.session.add(Task(title="task 1", user_id=1))
# db.session.add(Task(title="task 2", user_id=1))

# db.session.commit()
