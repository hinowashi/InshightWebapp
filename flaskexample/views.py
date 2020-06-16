import flask
from flask import render_template, request, session, g, redirect, url_for, abort, render_template, flash
from flaskexample import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
import json

from flaskexample.Project import Main

app.config.from_object(__name__)

@app.route('/')
@app.route('/index')
@app.route('/input')
def input():
   return render_template("input.html")

@app.route('/output', methods=['GET', 'POST'])
def output():
   address = request.args.get('Address')

   lat, lng = Main.give_lat_lgn(address)
   dfAll = Main.produce_table()

   setMat, nTime, n_clusters_, dfCounts = Main.clustering_and_prob(dfAll)
   outLoc, mapMarkerList, userOut = Main.output_generator(dfCounts, lat, lng, setMat, nTime, n_clusters_)

#   userOut = 'aaa'
   
   return render_template("output.html", sumofnums = userOut, lat = lat, lon = lng)
   
   
@app.route('/outputTesting')
def outputTesting():
      address = request.args.get('Address')

      lat, lng = Main.give_lat_lgn(address)
      dfAll = Main.produce_table()
   
      setMat, nTime, n_clusters_, dfCounts = Main.clustering_and_prob(dfAll)
      outLoc, mapMarkerList, userOut = Main.output_generator(dfCounts, lat, lng, setMat, nTime, n_clusters_)

      userOut = 'aaa'
#      mapMarkerList = [
#        ['Bondi Beach', 43.890542, -89.274856, 4],
#        ['Coogee Beach', 43.923036, -89.259052, 5],
#        ['Cronulla Beach', 43.028249, -89.157507, 3],
#        ['Manly Beach', 43.80010128657071, -89.28747820854187, 2],
#        ['Maroubra Beach', 43.950198, -89.259302, 1]
#      ]
      
      return render_template("outputTesting.html", sumofnums = userOut, lat = lat, lon = lng, loclist = json.dumps(mapMarkerList))
    



