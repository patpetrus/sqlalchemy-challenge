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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
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
def stat():
    #session link
    session = Session(engine)
    #query all stations
    # result = session.query(station.station).all
    # output = list(np.ravel(result))

    station_nm = session.query(station.station,station.name).all()
    return jsonify(station_nm)
    session.close()

    # return jsonify(output)

@app.route('/api/v1.0/tobs')
def tobs():
    #session link
    session = Session(engine)
    #query dates and temp observations (tobs)
    output = session.query(measurement.station, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
filter(measurement.station == 'USC00519281').all()

    session.close()
    #return jsonify tobs
    return jsonify(output)

@app.route('/api/v1.0/<start>')
def stat_temp(start):
    #Return a JSON list of the minimum temperature, 
    # the average temperature, 
    # and the max temperature for a given start or start-end range.
    session = Session(engine)

    temps = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
filter(measurement.date >= start).all()

    
    session.close()
    return jsonify(temps)

@app.route('/api/v1.0/<start>/<end>')
def stat_start_end(start, end):
    session = Session(engine)

    temps_start = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
filter(measurement.date >= start).filter(measurement.date <= end).all()

    session.close()
    return jsonify(temps_start)


    # When given the start only, calculate TMIN, TAVG, and TMAX 
    # for all dates greater than and equal to the start date.

    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX 
    # for dates between the start and end date inclusive.



if __name__ == '__main__':
    app.run(debug=True)
