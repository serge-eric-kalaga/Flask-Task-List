from os import rename
from urllib import request
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect
from datetime import datetime


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Task(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       title = db.Column(db.String(255), nullable=False)
       date = db.Column(db.DateTime, default=datetime.now)
       
       def __repr__(self) -> str:
           return self.title


@app.route("/", methods = ["GET", "POST"])
def index():
   if request.method == "POST" :
      title = request.form['title'] 
      task = Task(title=title)
      db.session.add(task)
      db.session.commit()
      return redirect("/")
          
   tasks = Task.query.order_by(Task.date)
   return render_template("index.html", tasks=tasks)


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