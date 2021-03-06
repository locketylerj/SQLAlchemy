import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"For average, max, and min temperatures after a certain start date enter the start date below in YYYY-M_DD format<br>"
        f"/api/v1.0/<start><br/>"
        f"For average, max, and min temperatures between a start and end date enter the dates below in YYYY-M_DD format with a slash between start and end dates<br>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    timeframe=dt.date(2017,8,23) - dt.timedelta(days=365)
    
    prcptimeframe = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date>=timeframe).all()

    
    precip = []
    for tobs in prcptimeframe:
        precip_dict = {}
        precip_dict["date"] = tobs[1]
        precip_dict["tobs"]=tobs[0]
        precip.append(precip_dict)

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()

    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    start_date=dt.date(2016,8,23) - dt.timedelta(days=365)
    end_date = dt.date(2016,8,23)
    
    results = session.query(Measurement.tobs).filter(Measurement.date>=start_date).filter(Measurement.date<=end_date) .all()
    tobs_results = list(np.ravel(results))

    return jsonify(tobs_results)

@app.route("/api/v1.0/<start>")
def start(start):
    start = dt.datetime.strptime(start, "%Y-%m-%d")
    start_stats = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date>=start).all()
    start_stats_list = list(np.ravel(start_stats))
    return jsonify(start_stats_list)

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    start = dt.datetime.strptime(start, "%Y-%m-%d")
    end = dt.datetime.strptime(end, "%Y-%m-%d")
    start_end_stats = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    start_end_list = list(np.ravel(start_end_stats))
    return jsonify(start_end_list)

if __name__ == '__main__':
    app.run(debug=True)