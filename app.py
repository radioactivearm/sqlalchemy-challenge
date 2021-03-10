## Andy McRae's Flask Server

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database setting
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect
Base = automap_base()

# tables
Base.prepare(engine, reflect=True)

# reference tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#------------------------------------------------------

# This is now Flask

app = Flask(__name__)


#----------------------------------------------
# routes

# home route
@app.route("/")
def home():
    """Lists all routes"""
    return (
        f"These are the Available Routes.<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"<br/>"
        f"start and end are dates"
    )


# precipitation query
@app.route("/api/v1.0/precipitation")
def get_prcp():
    session = Session(engine)

    """Return Dates and Their Accompanying Precipitations"""
    a_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) > a_year_ago).all()

    # making empty dictionary to populate with data
    result_dict = {}

    # populating with data
    for result in results:
        result_dict[result[0]] = result[1]

    session.close()

    return jsonify(result_dict)
    

# stations query
@app.route("/api/v1.0/stations")
def get_station():
    session = Session(engine)

    """Returns list of unique Stations"""
    # querying stations
    stations = session.query(Station.station).distinct().all()

    # getting into list form
    station_list = [station[0] for station in stations]

    session.close()

    return jsonify(station_list)



if __name__ == '__main__':
    app.run(debug=True)