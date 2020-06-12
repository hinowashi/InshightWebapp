import flask
from flask import render_template, request, session, g, redirect, url_for, abort, render_template, flash
from flaskexample import app
from flaskexample.miniWorkingCode import set_cover_mine, analysis
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2

app.config.from_object(__name__)

@app.route('/')
@app.route('/index')
@app.route('/input')
def addition_input():
   return render_template("input.html")

@app.route('/output')
def addition_output():
   lat = float(request.args.get('Lat'))
   lng = float(request.args.get('Lng'))
   distList = analysis(lat, lng)
#   print(distList)
   return render_template("output.html", sumofnums = distList, lat = lat, lon = lng)

@app.route('/mapbox_js',methods=['GET','POST'])
def mapbox_js():
    lat = float(request.args.get('Lat'))
    lng = float(request.args.get('Lng'))
    return render_template(
        "mapbox_js.html",
        ACCESS_KEY=app.config['MAPBOX_ACCESS_KEY'],
        lat = lat, lon = lng
    )
    
