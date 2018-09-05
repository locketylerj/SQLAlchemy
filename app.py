import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
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
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    timeframe=dt.date(2017,8,23) - dt.timedelta(days=365)
    
    prcptimeframe = session.query(Measurement.prcp, Measurement.date).filter(Measurement.date>=timeframe).all()

    
    precipitations = []
    for record  in prcptimeframe:
        precipitation_dict = {}
        precipiation_dict["tobs"] = measurement.tobs
        precipitation_dict["date"] = measurement.date
        
        precipitation.append(precipitation_dict)

    return jsonify(precipitations)





if __name__ == '__main__':
    app.run(debug=True)