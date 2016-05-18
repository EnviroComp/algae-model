import os
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix
from sqlalchemy import asc, desc
import datetime
import calc
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'bio.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.wsgi_app = ProxyFix(app.wsgi_app)
db = SQLAlchemy(app)


class Samples(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    @staticmethod
    def find(num):
        return Samples.query.filter(Samples.id == num).first()

    @staticmethod
    def list():
        return Samples.query.order_by(asc(Samples.id)).all()


class Default(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lake = db.Column(db.Integer)
    kmn = db.Column(db.Float)
    kmp = db.Column(db.Float)
    ktga = db.Column(db.Float)
    ktgb = db.Column(db.Float)
    tm = db.Column(db.Float)
    im = db.Column(db.Float)
    kpr = db.Column(db.Float)
    kpd = db.Column(db.Float)
    kda = db.Column(db.Float)
    kdb = db.Column(db.Float)
    fday = db.Column(db.Float)
    pmx = db.Column(db.Float)
    cj = db.Column(db.Float)
    cii = db.Column(db.Float)

    @staticmethod
    def find(num):
        return Default.query.filter(Default.lake == num).first()

    @staticmethod
    def list():
        return Default.query.order_by(asc(Default.id)).all()


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lake = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    po = db.Column(db.Float)
    nh = db.Column(db.Float)
    no = db.Column(db.Float)
    fn = db.Column(db.Float)
    temp = db.Column(db.Float)
    ft = db.Column(db.Float)
    solar = db.Column(db.Float)
    depth = db.Column(db.Float)
    sediment = db.Column(db.Float)
    kess = db.Column(db.Float)
    death = db.Column(db.Float)
    alpha = db.Column(db.Float)
    fi = db.Column(db.Float)
    growth = db.Column(db.Float)
    concentration = db.Column(db.Float)

    @staticmethod
    def before(date):
        x = Record.query.filter(Record.date < date).order_by(
            desc(Record.date)).first()

    @staticmethod
    def after(date):
        x = Record.query.filter(Record.date > date).order_by(
            asc(Record.date)).first()

    @staticmethod
    def last(num):
        return Record.query.filter(Record.lake == num).order_by(desc(Record.date)).first()

    @staticmethod
    def find(num):
        return Record.query.filter(Record.lake == num).order_by(asc(Record.date)).all()


@app.context_processor
def inject_lakes():
    return dict(lakes=Samples.list())


@app.route('/')
def index():
    return render_template('index.html', sample=None)


@app.route('/<num>')
def lakes(num):
    temp = []
    sediment = []
    depth = []
    intensity = []
    limiting = []
    nutrient = []
    for e in Record.find(num):
        temp.append(e.temp)
        sediment.append(e.sediment)
        depth.append(e.depth)
        intensity.append(e.solar)
        limiting.append([e.fn, e.ft, e.fi])
        nutrient.append([e.po, e.nh, e.no])
    return render_template('index.html', sample=Samples.find(num), indexx=True, data=Record.find(num), nutrient = nutrient, limiting = limiting, intensity=intensity, depth=depth, temp=temp, sediment=sediment)


@app.route('/new/lake', methods=['GET', 'POST'])
def new_lake():
    if request.method == 'POST':
        for f in request.form:
            if request.form[f] == "":
                return redirect(url_for('lakes', num=num))
        a = Samples(name=request.form['name'])
        db.session.add(Default(lake=len(Samples.list()) + 1, kmn=0.025, kmp=0.001, ktga=0.008, ktgb=0.008,
                               tm=30, im=300, kpr=0.125, kpd=0.02, kda=0.069, kdb=0.069, fday=0.52, pmx=2, cj=0.014, cii=-1))
        db.session.add(a)
        db.session.commit()
        return render_template('new_lake.html', sample=None)
    return render_template('new_lake.html', sample=None)


@app.route('/<num>/input/', methods=['GET', 'POST'])
def input(num):
    if request.method == 'POST':
        for f in request.form:
            if request.form[f] == "":
                return redirect(url_for('lakes', num=num))
        default = Default.find(num)
        try:
            last = Record.last(num).concentration
        except:
            last = default.cii
        date = str(request.form['date']).split("-")
        date = datetime.date(int(date[2]), int(date[0]), int(date[1]))
        try:
            po = float(request.form['po'])
        except:
            po = Record.last(num).po
        try:
            nh = float(request.form['nh'])
        except:
            nh = Record.last(num).nh
        try:
            no = float(request.form['no'])
        except:
            no = Record.last(num).no
        try:
            temp = float(request.form['temp'])
        except:
            temp = Record.last(num).temp
        solar = float(request.form['solar'])
        try:
            depth = float(request.form['depth'])
        except:
            depth = Record.last(num).depth
        try:
            sediment = float(request.form['sediment'])
        except:
            sediment = Record.last(num).sediment
        fn = calc.calc_fn(nh, no, default.kmn, po, default.kmp)
        ft = calc.calc_ft(temp, default.tm, default.ktga, default.ktgb)
        kess = calc.calc_kess(last, sediment)
        death = calc.calc_death(default.kpr, default.kpd,
                                default.kda, default.kdb, temp)
        alpha = calc.calc_alpha(solar, default.im, kess, depth)
        fi = calc.calc_fi(alpha, default.fday, depth, kess)
        growth = calc.calc_growth(fn, fi, ft, default.pmx)
        concentration = calc.calc_concentration(
            default.cj, last, growth, death)

        a = Record(lake=num, date=date, po=po, nh=nh, no=no, fn=fn, temp=temp, ft=ft, solar=solar, depth=depth,
                   sediment=sediment, kess=kess, death=death, alpha=alpha, fi=fi, growth=growth, concentration=concentration)
        db.session.add(a)
        db.session.commit()
        return redirect(url_for('lakes', num=num))
    return render_template('input.html', sample=Samples.find(num))


@app.route('/<num>/config/', methods=['GET', 'POST'])
def config(num):
    if request.method == 'POST':
        for f in request.form:
            if request.form[f] == "":
                return redirect(url_for('config', num=num))
        default = Default.find(num)
        default.kmn = float(request.form['kmn'])
        default.kmp = float(request.form['kmp'])
        default.ktga = float(request.form['ktga'])
        default.ktgb = float(request.form['ktgb'])
        default.tm = float(request.form['tm'])
        default.im = float(request.form['im'])
        default.kpr = float(request.form['kpr'])
        default.kpd = float(request.form['kpd'])
        default.kda = float(request.form['kda'])
        default.kdb = float(request.form['kdb'])
        default.fday = float(request.form['fday'])
        default.pmx = float(request.form['pmx'])
        default.cj = float(request.form['cj'])  # boundary
        try:
            default.cii = float(request.form['cii'])  # initial
        except:
            default.cii = default.cii
        db.session.commit()
        return render_template('config.html', defaults=default, sample=Samples.find(num))
    return render_template('config.html', defaults=Default.find(num), sample=Samples.find(num))

if __name__ == '__main__':
    app.run()
