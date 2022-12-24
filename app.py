from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
import os

base_dir = os.path.dirname(os.path.realpath(__file__))

db = SQLAlchemy()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir, 'todo.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

class Todo(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean())
    
    

@app.route('/')
def home():
    todo_list = Todo.query.all()
    return render_template('base.html', todo_list=todo_list)

@app.route('/add', methods = ['GET', 'POST'])
def add():
    title = request.form.get('title')
    new_todo =Todo(title=title, complete= False)

    db.session.add(new_todo)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/update/<int:id>')
def update(id) :
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete   

    db.session.commit()

    return redirect(url_for('home'))

@app.route('/delete')
def delete(id):
    todo = Todo.query.filter_by(id=id).first()

    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for('home'))

if __name__=="__main__":
    app.run(debug=True)    