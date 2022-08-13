from os import rename
from urllib import request
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, session
from datetime import datetime


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "23_mars_2000"
db = SQLAlchemy(app)


class User(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String(255), nullable=False, primary_key=True)
      password = db.Column(db.String(255), nullable=False)
      
      task = db.relationship("Task", backref="user")


class Task(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       title = db.Column(db.String(255), nullable=False)
       date = db.Column(db.DateTime, default=datetime.now)
       
       user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
       
       def __repr__(self) -> str:
           return self.title
        



@app.route("/login", methods = ["GET", "POST"])
def login():
   if request.method == "POST":
      username = request.form['username'] 
      password = request.form['password']
      
      # voir si user existe
      if db.session.query(User.id).filter_by(username=username, password=password) is not None:
         session['username'] = username
         session['password'] = password
         # print("------------" + session['username'])
         return redirect("/")
      else : 
         session['username'] = username
         session['password'] = password
         db.session.create(User(username=username, password=password))
         db.session.commit()
         return redirect("/")
         
   return render_template("login.html")


@app.route("/", methods = ["GET", "POST"])
def index():
   
   if "user" and "password"  in session :
       
      if request.method == "POST" :
         title = request.form['title'] 
         task = Task(title=title)
         db.session.add(task)
         db.session.commit()
         return redirect("/")
            
            
      user_logged_username = session["username"]
      user_logged_id = User.query.filter_by(username=user_logged_username)[0].id
      tasks = Task.query.filter(user_id=user_logged_id).order_by(Task.date)
      return render_template("index.html", tasks=tasks)
   
   return redirect("/login")
   


@app.route("/delete/<int:id>/")
def delete(id):
   task = Task.query.get_or_404(id)
   db.session.delete(task)
   db.session.commit()
   return redirect("/")


@app.route("/update/<int:id>/", methods=["POST", "GET"])
def update(id):
   task = Task.query.get_or_404(id)
   if request.method == "POST":
      task.title = request.form["title"]
      db.session.commit()
   else:
      return render_template("update.html", task=task)
   return redirect("/")


@app.route("/<int:id>/", methods=["GET",])
def detail(id):
   task = Task.query.get_or_404(id)
   return render_template("detail.html", task=task)


@app.route("/contact")
def contact():
   return render_template("contact.html")

@app.route("/about")
def about():
   return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)