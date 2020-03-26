import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

app=Flask(__name__)


engine = create_engine('postgresql://postgres:deepika5@localhost:5432/mydb')
db= scoped_session(sessionmaker(bind=engine))

@app.route('/')
def admin():
    origin=request.form.get("origin")
    destination=request.form.get("destination")
    duration=request.form.get("minutes")
    if request.method == 'POST':
        db.execute("insert into flights (origin,destination,duration) values (:origin, :destination, :duration)",
             {"origin":origin,"destination":destination,"duration":duration})
        db.commit()
    return render_template("admin.html", origin=origin,destination=destination,duration=duration)

@app.route('/update',methods=['GET', 'POST'])
def update():
    flights=db.execute("select * from flights").fetchall()
    return render_template("update.html",flights=flights)
