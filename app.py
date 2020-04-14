# All my imports 

from flask import Flask
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


############################################
## Data_Base Set-up                        ##
############################################

engine= create_engine("sqlite:///hawaii.sqlite")

# reflect an exicting database into a new mode;

Base= automap_base()

Measurement = Base.classes.measurement
Station = Base.classes.station



############################################
## Flask Set-up                       ##
############################################

app = Flask(__name__)

############################################
## Flask Routes                      ##
############################################

@app.route("/")
def home():
    print(" Welcome to the Home Page. <br> All routes listed below")
    return(
       f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start> "
        f"/api/v1.0/<start>/<end>")

    


