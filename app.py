# All my imports 
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


############################################
## Data_Base Set-up                        ##
############################################

engine= create_engine("sqlite:///hawaii.sqlite")

# reflect an exicting database into a new mode;
Base = automap_base()

# Reflect the tables 
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create the link to the Database from python 
session=Session(engine)


############################################
## Flask Set-up                       ##
############################################

app = Flask(__name__)

############################################
## Flask Routes                      ##
############################################

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation <br>"
        f"/api/v1.0/stations <br>"
        f"/api/v1.0/tobs <br>"
        f"/api/v1.0/start_date <br>"
        f"/api/v1.0/start_date/end_date <br>"
        )



@app.route("/api/v1.0/precipitation")
def precipitation():



    session = Session(engine)

    # Query all measurment data
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    measurment_results = []
    for date, prcp, in results:
        measurment_dict = {}
        measurment_dict["date"] = date
        measurment_dict["prcp"] = prcp
        measurment_results.append(measurment_dict)

    return jsonify( measurment_results)

@app.route('/api/v1.0/stations')
def station():

    session = Session(engine)

    # Query all measurment data
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation)

    session.close()
    # Create a dictionary from the row data and append to a list of all_passengers
    station_results = []
    for station, name,latitude,longitude,elevation in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        station_results.append(station_dict)

    return jsonify(station_results)



@app.route('/api/v1.0/tobs')
def tobs():

    year_ago= dt.date(2017, 8, 23) - dt.timedelta(days=365)

    tobs= session.query(Measurement.tobs, Measurement.date).filter(Measurement.date >= year_ago).all()
    
    #Close query
    session.close()

    # Convert list of tuples into normal list
    temp_list= list(np.ravel(tobs))

    
	

    return jsonify(temp_list)

@app.route('/api/v1.0/<start>')
def beginning_dates(start):
    #Set-up for user entry
    start_date =dt.datetime.strptime(start, '%Y-%m-%d')
    # Query Min, Avg, Max tempeture and filter by date
    Date= session.query(func.min (Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs).filter(Measurement.date >= start_date)).all()
    #Close query
    session.close()
    return jsonify(Date)

@app.route('/api/v1.0/<start>/<end>')
def hawaii(start,end):

     #Set-up for user entry
    begin_date =dt.datetime.strptime(start, '%Y-%m-%d')
     #Set-up for user entry
    end_date =dt.datetime.strptime(end, '%Y-%m-%d')

    # Query Min, Avg, Max tempeture and filter by date
    summary_date= session.query((func.min (Measurement.tobs), func.avg(Measurement.tobs), func.min (Measurement.tobs).filter( Measurement.date >= begin_date, Measurement.date<=end_date))).all()

    #Close query
    session.close()

    return jsonify(summary_date)






    
if __name__ == '__main__':
    app.run(debug=True)

