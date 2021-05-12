from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=True)
    intro = db.Column(db.String(300), nullable=True)
    text = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):  # когда выбираем объект, будет выдаваться айди + сам объект
        return '<Article %r>' % self.id


@app.route('/') # Главная
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("news_home.html")


@app.route('/posts') # Страница всех статей
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()  # обращаемся к БД, сортируя по дате
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>') # страница новой статьи
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/create-article', methods=['POST', 'GET']) # создание новой записи
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)  # создаём объект

        try:
            db.session.add(article)  # добавляем в БД
            db.session.commit()  # сохраняем в БД
            return redirect('/posts')
        except:
            return "Произошла ошибка :("
    else:
        return render_template("create-article.html")


@app.route('/posts/<int:id>/delete') # страница удаления записи
def post_delete(id):
    article = Article.query.get_or_404(id) # ищем нужную запись в БД

    try:
        db.session.delete(article) # удаляем запись
        db.session.commit()  # сохраняем в БД
        return redirect('/posts')
    except:
        return "При удалении возникла ошибка"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET']) # редактирование записи
def update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.description = request.form['text']

        try:
            db.session.commit()  # сохраняем в БД
            return redirect('/posts')
        except:
            return "Произошла ошибка :("
    else:
        return render_template("update.html", article=article)

if __name__ == "__main__":
    app.run(debug=True)
