from merge import app, db, Default, Record, Samples
from flask.ext.script import Manager, prompt_bool
import csv
import datetime
manager = Manager(app)

@manager.command
def init():
    db.create_all()
    db.session.add(Samples(name="Lake Beasley"))
    db.session.add(Default(lake=1, kmn=0.025, kmp=0.001, ktga=0.008, ktgb=0.008, tm=30, im=300, kpr=0.125, kpd=0.02, kda=0.069, kdb=0.069, fday=0.52, pmx=2, cj=0.014, cii=-1))
    db.session.commit()
    print 'Initialized the database'

@manager.command
def drop():
    if prompt_bool(
        "Are you sure you want to lose all your data"):
        db.drop_all()
        print 'Dropped the database'

@manager.command
def haul():
    f = open("import.csv", "rt")
    try:
        reader = csv.reader(f)
        for row in reader:
            date = row[0].split("/")
            date = datetime.date(int(date[2]), int(date[0]), int(date[1]))
            po=float(row[1])
            nh=float(row[2])
            no=float(row[3])
            fn=float(row[4])
            temp=float(row[5])
            ft=float(row[6])
            solar=float(row[7])
            depth=float(row[8])
            sediment=float(row[9])
            kess=float(row[10])
            death=float(row[11])
            alpha=float(row[12])
            fi=float(row[13])
            growth=float(row[14])
            concentration=float(row[15])
            db.session.add(Record(lake=1, date=date, po=po, nh=nh, no=no, fn=fn, temp=temp, ft=ft, solar=solar, depth=depth, sediment=sediment, kess=kess, death=death, alpha=alpha, fi=fi, growth=growth, concentration=concentration))
            print row
    finally:
        db.session.commit()
        f.close()

@manager.command
def start():
    app.run()

if __name__ == '__main__':
    manager.run()
