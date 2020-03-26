import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine('postgresql://postgres:deepika5@localhost:5432/mydb')
db=scoped_session(sessionmaker(bind=engine))


def main():

    ##list all flights.
    flights = db.execute("SELECT id,origin,destination,duration From flights").fetchall()
    for flight in flights:
        print(f"Flight Id:{flight.id}: {flight.origin} to {flight.destination}, {flight.duration} minutes.")


if __name__ == '__main__':
   main()

####prompt user to choose a flight#######
flight_id=int(input("\nFlight ID: "))
flight= db.execute("SELECT origin,destination,duration From flights where id=:id",
          {'id':flight_id}).fetchone()

###make sure flight is valid##
if flight is None:
    print("Error: No such flight.")
    #return

###list passengers
passengers = db.execute("select name from passengers where flight_id = :flight_id  ",
            {"flight_id":flight_id}).fetchall()

print("\npassengers:")
for passenger in passengers:
    print(passenger.name)
if len(passengers)==0:
    print("No passengers.")
