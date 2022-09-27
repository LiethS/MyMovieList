from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import lxml
from bs4 import BeautifulSoup

class Movie:
    def __init__(self, title, year, image, link):
        self.title = title
        self.year = year
        self.image = image
        self.link = "https://www.imdb.com"+link

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id



def scrape(title):
    title = title.replace(" ", "%20")
    URL = "https://www.imdb.com/find?q=" + title + "&s=tt&ttype=ft&ref_=fn_ft"

    html_content = requests.get(URL).text

    try:
        data = html_content.split("table")
        data = data[1].split("<td class=\"primary_photo\">")
        data.pop(0)

        movies = ()

        db.create_all()

        for movie in data:
            movies.append(Movie(movie.split(">")[6][:-3], movie.split(">")[7][1:-4], movie.split("\"")[3], movie.split("\"")[1]))
        return movies
    except:
        return ()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        results = ()
        title_search = request.form['content']
        results = scrape(title_search)
        return redirect('/query'+"%20")
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        results = (Movie("black", "adfasdfadsf", "asdfadsf", "adsfadsfadsfad"), Movie("red", "dafsdff", "asd", "adsfadsfadsfad"))
        for movie in results:
            print(movie.title + " " + movie.year)
        return render_template('index.html', tasks=tasks, results=results)

# @app.route('/query')
# def query():

# @app.route('/add/<Movie:movie>')
# def add(movie):
#     new_task = Todo(content=movie)
#     try:
#         db.session.add(new_task)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'There was an issue adding your task'

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)
    
if __name__ == "__main__":
    app.run(debug=True)
