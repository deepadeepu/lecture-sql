import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

app=Flask(__name__)

engine = create_engine('postgresql://postgres:deepika5@localhost:5432/mydb')
db= scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    flights=db.execute("select * from flights").fetchall()
    return render_template("index.html", flights=flights)

@app.route("/book", methods=["POST"])
def book():
    """Book a flight.""" ##get more information
    name=request.form.get("name")
    try:
       flight_id=int(request.form.get("flight_id"))
    except ValueError:
       return render_template("error.html", message="Invalid flight number")

##make sure the flight exist
    if db.execute("select * from flights where id =:id", {"id": flight_id}).rowcount == 0:
         return render_template("error.html", message="No such flight with that id")
    db.execute("insert into passengers (name,flight_id) values (:name, :flight_id)",
             {"name":name,"flight_id":flight_id})
    db.commit()
    return render_template("success.html")

@app.route("/flights")
def flights():
    """Lists all flights"""
    flights=db.execute("select * from flights").fetchall()
    return render_template("flights.html", flights=flights)

@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    """Lists details about a single flight"""

##make sure the flight exist
    flight=db.execute("select * from flights where id =:id", {"id": flight_id}).fetchone()
    if flight is None:
        return render_template("error.html", message="No such flight")

    passengers = db.execute("select name from passengers where flight_id= :flight_id",
                       {"flight_id":flight_id}).fetchall()
    return render_template("flight.html",flight=flight,passengers=passengers)
