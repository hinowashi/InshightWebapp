import flask
from flask import render_template, request, session, g, redirect, url_for, abort, render_template, flash
from flaskexample import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
import json

import pandas as pd
import numpy as np

from flaskexample.Project import Main

app.config.from_object(__name__)

@app.route('/')
@app.route('/index')
@app.route('/input')
def input():
   return render_template("input.html")
      
      
@app.route('/output')
def outputTesting():
      address = request.args.get('Address')

      lat, lng = Main.give_lat_lgn(address)
      dfAll = Main.produce_table()

      setMat, nTime, n_clusters_, dfCounts = Main.clustering_and_prob(dfAll)
      mapMarkerList, dataTable = Main.output_generator(dfCounts, lat, lng, setMat, nTime, n_clusters_)
      
      return render_template("output.html", lat = lat, lon = lng, loclist = json.dumps(mapMarkerList), tableInfo = dataTable)
    



