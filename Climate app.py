#Import flask
from flask import Flask, jsonify

#Import other dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
###################################
#Database Setup
###################################

#Set up engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect the database
Base = automap_base()
Base.prepare(engine, reflect=True)

#Save the tables
measure = Base.classes.measurement
station = Base.classes.station

###################################
#Flask set up
###################################

#Create an app
app = Flask(__name__)

###################################
#Flask Routes
###################################

@app.route("/")
def home():
    return(f"Hello Welcome to my Climate App<br/>"
           f"Available routes are listed below<br/>"
           f"/api/v1.0/precipitation<br/>"
           f"/api/v1.0/stations<br/>"
           f"/api/v1.0/tobs<br/>"
           f"/api/v1.0/<start> and /api/v1.0/<start>/<end><br/>")

@app.route("/api/v1.0/precipitation")
def prcp():
    #Create a session
    session = Session(engine)

    #Query data for date and measure
    results = session.query(measure.date, measure.prcp).all()

    session.close()

    #Create a dictionary from the data we just pulled

    prcp_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    #Create a session
    session = Session(engine)

    #Query data for date and measure
    results = session.query(station.station, station.name).all()

    session.close()

    stations = {}

    for stat, name in results:
        stations[stat] = name

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    #Find the last day in the data set
    last_day = session.query(measure.date).order_by(measure.date.desc()).first()

    # Get the data for one year ago
    last_year_day = (dt.datetime.strptime(last_day[0], '%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    results= session.query(measure.date, measure.tobs).filter(measure.date >= last_year_day).order_by(measure.date).all()

    session.close()

    #Create empty list
    tobs_list = []

    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobs_list.append(tobs_dict)

    return jsonify((tobs_list))


if __name__ == "__main__":
    app.run(debug=True)