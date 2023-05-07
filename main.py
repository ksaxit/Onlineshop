from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    text = db.Column(db.Text, default=None)

    def __repr__(self):
        return self.title

@app.route('/')
def index():
    shops = Shop.query.order_by(Shop.price).all()
    return render_template('index.html', data=shops)


@app.route('/bye/<int:id>')
def bye(id):
    shop = Shop.query.get(id)
    from cloudipsp import Api, Checkout
    api = Api(merchant_id=1396424, #id компании выдается при регистрации своей компании в фонди + секретный ключ
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": str(shop.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        text = request.form['text']
        shops = Shop(title=title, price=price, text=text)
        try:
            db.session.add(shops)
            db.session.commit()
            return redirect('/')
        except:
            return "Ой, ошибочка вышла"
    else:
        return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True)