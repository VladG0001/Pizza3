from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

78
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orderman.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)


class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)


class ReviewForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    pizzas = Pizza.query.all()
    return render_template('menu.html', pizzas=pizzas)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    form = ReviewForm()
    if form.validate_on_submit():
        new_review = Review(name=form.name.data, content=form.content.data)
        db.session.add(new_review)
        db.session.commit()
        flash('Review added successfully!')
        return redirect(url_for('reviews'))
    reviews = Review.query.all()
    return render_template('reviews.html', form=form, reviews=reviews)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

def init_db():
    db.create_all()
    if Pizza.query.count() == 0:
        pizzas = [
            Pizza(name='Pepperoni', ingredients='Піца з пепероні та сиром', price=8.99),
            Pizza(name='Margherita', ingredients='Класична піца з томатами та моцарелою', price=7.99),
            Pizza(name='Hawaiian', ingredients='Піца Гавайська з ананасами та шинкою', price=9.99)
        ]
        db.session.bulk_save_objects(pizzas)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
