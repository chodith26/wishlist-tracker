from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wishlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class WishlistItem(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(100), nullable=False)
    price    = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    added_on = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'WishlistItem({self.name}, {self.price})'


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    items = db.session.execute(db.select(WishlistItem)).scalars().all()
    return render_template('index.html', items=items, count=len(items))

@app.route('/add', methods=['POST'])
def add():
    name     = request.form.get('name', '').strip()
    price    = request.form.get('price', '').strip()
    category = request.form.get('category', '').strip()

    if not name or not price or not category:
        return redirect(url_for('home'))

    added_on = datetime.now().strftime('%d %b %Y')
    new_item = WishlistItem(name=name, price=price,
                            category=category, added_on=added_on)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    item = db.session.get(WishlistItem, id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/api/wishlist')
def api_wishlist():
    items = db.session.execute(db.select(WishlistItem)).scalars().all()
    return jsonify([{
        'id':       item.id,
        'name':     item.name,
        'price':    item.price,
        'category': item.category,
        'added_on': item.added_on
    } for item in items])


if __name__ == '__main__':
    app.run(debug=True)