

from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy





app = Flask(__name__)
app.config['SECRET_KEY'] = 'Python'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///card.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///film.sqlite'
app.config['SQLALCHEMY_BINDS'] = {'first':'sqlite:///quotes.sqlite'}
db = SQLAlchemy(app)


class Cardinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    ccn = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Float, nullable=False)
db.create_all()

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    birthday = db.Column(db.FLOAT(12), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    nickname = db.Column(db.String(40), nullable=False)
    portrayed = db.Column(db.String(40), nullable=False)
    status = db.Column(db.String(40), nullable=False)

    def __str__(self):
        return f'{self.id}) დაბადების თარიღია:{self.birthday}; სახელია: {self.name}; მეტსახელია: {self.nickname}; ნამდვილი სახელია : {self.portrayed}; სტატუსია:{self.status}'

class Quotes(db.Model):
    __bind_key__ = 'first'
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(70), nullable=False)
    author = db.Column(db.String(30), nullable=False)

    def __str__(self):
        return f'{self.id})ციტატა:{self.quote}; ავტორი:{self.author}'

@app.route('/')
def home():
    all_film =  Film.query.all()
    return render_template('index.html', all_film=all_film)


@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/SaveWalt')
def SaveWalt():
    return render_template('savewalt.html')

@app.route('/quotes')
def quotes():
    all_quotes = Quotes.query.all()
    return render_template('quotes.html', all_quotes=all_quotes)



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('user'))

    return render_template('login.html')

@app.route('/carousel')
def carousel():
    return render_template('carousel.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return 'you are logged out'


@app.route('/cardinfo', methods=['GET', 'POST'])
def cardinfo():
    if request.method=='POST':
        fn = request.form['first_name']
        ln = request.form['last_name']
        ccn = request.form.get("ccn", False)
        a = request.form['amount']
        if fn=='' or ln=='' or a=='' or ccn=='':
            flash('გთხოვთ შეავსოთ ყველა ველი', 'error')
        elif not a.isnumeric():
            flash('გთხოვთ, ბარათის ნომერი და თანხა შეიყვანოთ რიცხვებით', 'error')
        else:
            c1 = Cardinfo(first_name=fn, last_name=ln, ccn=float(ccn), amount=float(a))
            db.session.add(c1)
            db.session.commit()
            flash('თანხა გადარიცხულია', 'info')

    return render_template('cardinfo.html')


if __name__ == "__main__":
    app.run(debug=True,use_reloader=True)

b1 = cardinfo(last_name='leqsebi krebuli', first_name='ilia', amount=15)
db.session.add(b1)
db.session.commit()

