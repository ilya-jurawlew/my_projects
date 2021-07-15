from flask import Flask, render_template, request, redirect

from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy

from cloudipsp import Api, Checkout


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


categories = [
        'Световые панели',
        'Средства защиты для бизнеса',
        'Грифельные доски',
        'Световые короба',
        'Объёмные буквы',
        'Штендеры',
        'Рекламные островки',
        'Рекламно-информационные стойки',
    ]


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    parameter_1 = db.Column(db.String(50), nullable=False)
    parameter_2 = db.Column(db.String(50), nullable=False)
    parameter_3 = db.Column(db.String(50), nullable=False)
    parameter_4 = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return {self.title}


@app.route('/')
def home():
    return render_template('home.html', categories=categories)


@app.route('/category/<string:category>')
def category(category):
    items = Item.query.order_by(Item.price).all()
    return render_template('category.html', items=items, categories=categories)


@app.route('/product/<int:id>')
def product(id):
    item = Item.query.get(id)
    return render_template('product.html', item=item)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/product/<int:id>/pay')
def pay(id):
    item = Item.query.get(id)

    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(item.price) + '00.00'
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        description = request.form['description']
        category = request.form['category']
        parameter_1 = request.form['parameter_1']
        parameter_2 = request.form['parameter_2']
        parameter_3 = request.form['parameter_3']
        parameter_4 = request.form['parameter_4']

        item = Item(title=title, price=price, description=description, category=category, parameter_1=parameter_1,
                    parameter_2=parameter_2, parameter_3=parameter_3, parameter_4=parameter_4)

        try:
            db.session.add(item)  # добавляем в БД
            db.session.commit()  # сохраняем в БД
            return redirect('/')
        except:
            return "Произошла ошибка :("
    else:
        return render_template('create.html', categories=categories)


@app.route('/product/<int:id>/del')
def post_delete(id):
    item = Item.query.get_or_404(id)
    try:
        db.session.delete(item)
        db.session.commit()
        return redirect('/')
    except:
        return "При удалении возникла ошибка"


if __name__ == "__main__":
    app.run(debug=True)
