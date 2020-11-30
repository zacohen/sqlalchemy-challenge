import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Stations= Base.classes.station
Measurements= Base.classes.measurement

session = Session(engine)

app = Flask(__name__)
#Home page.
#List all routes that are available.
@app.route("/")
def home():
    return(f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-09-23<br/>"
        f"/api/v1.0/2016-09-23/2016-11-23<br/>")




#Convert the query results to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation = session.query(Measurements.date, Measurements.prcp).filter(Measurements.date>="2016-08-23").all()
    preDic = list(np.ravel(precipitation))
    
    return jsonify(preDic)




#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Stations.station, Stations.name).all()
    stationDictionary = list(np.ravel(stations))
    return jsonify(stationDictionary)



#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    most_active_station= 'USC00519281'
    tobs = session.query(Measurements.date, Measurements.tobs).\
           filter(Measurements.date>="2016-08-23").\
           filter(Measurements.date<="2017-08-23").\
           filter(Measurements.station == most_active_station).all()
    tobsDictionary = list(np.ravel(tobs))
    return jsonify(tobs)


#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/2016-09-23")
def start():
    start_day = session.query(Measurements.date,func.min(Measurements.tobs),func.avg(Measurements.tobs),func.max(Measurements.tobs)).\
    filter(Measurements.date >= "2016-09-23").\
    group_by(Measurements.date).all()

    # Convert List of Tuples Into Normal List
    start_day_list = list(start_day)
        
    return jsonify(start_day_list)
    

@app.route("/api/v1.0/2016-09-23/2016-11-23")
def end():
    start_end_day = session.query(Measurements.date,func.min(Measurements.tobs),func.avg(Measurements.tobs),func.max(Measurements.tobs)).\
    filter(Measurements.date >= "2016-09-23").\
    filter(Measurements.date <= "2016-11-23").\
    group_by(Measurements.date).all()
    
    # Convert List of Tuples Into Normal List
    start_end_day_list = list(start_end_day)
        
    return jsonify(start_end_day_list)


if __name__ == "__main__":
    app.run(debug=True)