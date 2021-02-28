#hello world!

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys()

# Save reference to the table
station = Base.classes.station
measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    data_precip = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >=query_date).all()
    
    session.close()

    # Convert list of tuples into normal list
    # all_names = list(np.ravel(results))  USE THIS IF LIST, IF NOT USE DICT 
    precip = []
    for date, prcp in data_precip:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        precip.append(prcp_dict)

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    #session link
    session = Session(engine)
    #query all stations
    stations = session.query(station.name).all

    session.close()

    return jsonify(stations)

@app.route('/api/v1.0/tobs')
def tobs():
    #session link
    session = Session(engine)
    #query dates and temp observations (tobs)
    for 'USC00519281' in measurement.station:
        print(measurement.date, measurement.tobs)

    session.close()
    #return jsonify tobs
    return jsonify(tobs)

@app.route('/api/v1.0/<start>')
def stat_temp():
    #Return a JSON list of the minimum temperature, 
    # the average temperature, 
    # and the max temperature for a given start or start-end range.
    session = Session(engine)

    temps = measurement.temps.describe()
    
    session.close()
    return jsonify(temps)

    # When given the start only, calculate TMIN, TAVG, and TMAX 
    # for all dates greater than and equal to the start date.

    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX 
    # for dates between the start and end date inclusive.



if __name__ == '__main__':
    app.run(debug=True)
