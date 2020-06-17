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
def output():
      address = request.args.get('Address')

      lat, lng = Main.give_lat_lgn(address)
      dfAll = Main.produce_table()

      setMat, nTime, n_clusters_, dfCounts = Main.clustering_and_prob(dfAll)
      outLoc, mapMarkerList, userOut = Main.output_generator(dfCounts, lat, lng, setMat, nTime, n_clusters_)
      
      return render_template("output.html", sumofnums = userOut, lat = lat, lon = lng, loclist = json.dumps(mapMarkerList))
      
      
      
@app.route('/outputTesting')
def outputTesting():
      address = request.args.get('Address')

      lat, lng = Main.give_lat_lgn(address)
#      dfAll = Main.produce_table()
#
#      setMat, nTime, n_clusters_, dfCounts = Main.clustering_and_prob(dfAll)
#      outLoc, mapMarkerList, userOut = Main.output_generator(dfCounts, lat, lng, setMat, nTime, n_clusters_)

      userOut = 'aaa'
      mapMarkerList = [
        ['Bondi Beach', 43.890542, -89.274856, 4],
        ['Coogee Beach', 43.923036, -89.259052, 5],
        ['Cronulla Beach', 43.923036, -89.259052, 3],
        ['Manly Beach', 43.80010128657071, -89.28747820854187, 2],
        ['Maroubra Beach', 43.950198, -89.259302, 1]
      ]
      
      arrayWeeks = [4,5,3,2,1]
      arrayLocName = ['Bondi Beach', 'Coogee Beach','Cronulla Beach','Manly Beach','Maroubra Beach']
      arrayBirds = [['a','c'],['a','d','c'],['c','d'],['q','w'],['e'],['f','t']]
      arrayLat = [43.890542,43.923036,43.923036,43.800101,43.950198]
      arrayLng = [-89.274856,-89.259052,-89.259052,-89.2874782,-89.259302]
      
      
      test = pd.DataFrame({'Week': np.array(arrayWeeks),
                        'Place': np.array(arrayLocName),
                        'Birds': np.array(arrayBirds),
                        'Lat': np.array(arrayLat),
                        'Lgn': np.array(arrayLng),
                          })
      
      return render_template("outputTesting.html", sumofnums = userOut, lat = lat, lon = lng, loclist = json.dumps(mapMarkerList), tableInfo = test)
    



