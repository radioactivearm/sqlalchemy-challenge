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


# tobs query
@app.route("/api/v1.0/tobs")
def get_tobs():
    session = Session(engine)

    "Returns list of Temperatures over last year from most active station"
    # list of stations in desceding order
    stations_desc = session.query(Measurement.station, func.count(Measurement.tobs)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.tobs).desc()).all()

    # most active station
    station_one = stations_desc[0][0]

    # measure a year ago
    a_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # temps and dates over last year from most active station
    temp_list = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == station_one).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) > a_year_ago).all()

    # temps in list with out tuples
    new_temp_list = [x[1] for x in temp_list]

    # ending session
    session.close()

    return jsonify(new_temp_list)


# start date
@app.route("/api/v1.0/<start>")
def begin(start):
    session = Session(engine)

    """Given a start date, returns min, max and average temps"""

    # calculating min temp in range using query
    # the [0][0] at the end is to pull it out of list and tuple
    tmin = session.query(func.min(Measurement.tobs)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= func.strftime('%Y-%m-%d', start)).all()[0][0]

    # calculating avg temp in range using query
    # the [0][0] at the end is to pull it out of list and tuple
    tavg = session.query(func.avg(Measurement.tobs)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= func.strftime('%Y-%m-%d', start)).all()[0][0]

    # calculating max temp in range using query
    # the [0][0] at the end is to pull it out of list and tuple
    tmax = session.query(func.max(Measurement.tobs)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= func.strftime('%Y-%m-%d', start)).all()[0][0]

    # making list that will be jsonified
    t_list = [tmin, tavg, tmax]

    # closing session
    session.close()

    return jsonify(t_list)


# start and end
@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    session = Session(engine)

    """Given a start and an end date, returns min, max and average temps"""

    # calculating min temp in range using query
    # the [0][0] at the end is to pull it out of list and tuple
    tmin = session.query(func.min(Measurement.tobs)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= func.strftime('%Y-%m-%d', start)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) <= func.strftime('%Y-%m-%d', end)).all()[0][0]

    # calculating avg temp in range using query
    # the [0][0] at the end is to pull it out of list and tuple
    tavg = session.query(func.avg(Measurement.tobs)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= func.strftime('%Y-%m-%d', start)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) <= func.strftime('%Y-%m-%d', end)).all()[0][0]

    # calculating max temp in range using query
    # the [0][0] at the end is to pull it out of list and tuple
    tmax = session.query(func.max(Measurement.tobs)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= func.strftime('%Y-%m-%d', start)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) <= func.strftime('%Y-%m-%d', end)).all()[0][0]

    # making a list to return jsonifyed
    t_list = [tmin, tavg, tmax]

    # closing session
    session.close()

    return jsonify(t_list)



if __name__ == '__main__':
    app.run(debug=True)