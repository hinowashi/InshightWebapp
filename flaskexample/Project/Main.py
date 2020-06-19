#!/usr/bin/env python
# coding: utf-8

# # Insight Project --Birding Big Year--
# 
# In this project I intend to determine a way to see all the birds one can see on a single state, for a given time window.  For all those birdirers that want to get to the top 100 of their state on ebrid, this will be the perfect tool. The user will input the state, home address (or lat,lon), time window and birds that already have been seen*. This last one (*) is an optional thing.


import numpy as np
import pickle
import googlemaps
import pandas as pd
import psycopg2

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

import matplotlib.pyplot as plt

from flaskexample.Project import SetCover
from flaskexample.Project import DBScaner
from flaskexample.Project import Definition
from flaskexample.Project import Itinerary

def save_fig(name):
    fig.savefig(name,dpi=80,bbox_inches='tight', pad_inches=0.02, format = 'png')


def give_lat_lgn(userHomeBase):
#    gmaps = googlemaps.Client(key=Definition.GOOGLEKEY)
#    geocode_result = gmaps.geocode('{}'.format(userHomeBase))
#    pickle.dump(geocode_result, open("./geocode_result.p", "wb" ))
    geocode_result = pickle.load(open("./geocode_result.p", "rb" ))
    state_long = geocode_result[0]['address_components'][2]['long_name']
    state_short = geocode_result[0]['address_components'][2]['short_name']
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
#    print(state_long,lat, lng)
#    print('YESSS')
    
    return lat, lng

def produce_table():
    '''
    The bird data has been trasnform to a Postgres SQL database.  This section of the code reads form this database to do the calculations.

    '''

    dbname = Definition.DBNAME
    username = Definition.USERNAME
    pswd = Definition.PSWD

    # connect:
    con = None
    con = psycopg2.connect(database = dbname, user = username, host='localhost', password=pswd)

    # query:
    sql_query = """SELECT * FROM test WHERE year = 2018;"""
    dfTrain = pd.read_sql_query(sql_query,con)
#    print(dfTrain['common_name'].value_counts())
    
    return dfTrain


def clustering_and_prob(dfTrain):
    '''
    BDSCAN is a density clustering that will tell where is popular for people to go birding (based on the desnity of hotsopts).  I will define a cluster as having atleast 3 point and with a maximum distance of 0.05degrees or about 5km.  With that I will optain where does each hotspot ('LOCALITY') belongs to. If '-1' they are not part of any cluster.
    '''


    dfcluster, labels, n_clusters_ = DBScaner.cluster_selection(dfTrain, eps=0.03, min_samples=2)
    dfCounts = DBScaner.cluster_center(dfcluster, dfTrain)

    dfProb = dfTrain.merge(dfcluster.filter(['locality','db_cluster']),
                                left_on='locality', right_on='locality', how = 'left').filter(['common_name','all_species_reported','year_week', 'db_cluster'])

    nTime = 54
    nLoc = n_clusters_
    setMat = np.empty((nTime,nLoc), dtype=object)


    for week in range(0,nTime):
        dfProbA = dfProb[dfProb['year_week']== week]
        dfProb1 = dfProbA.groupby(['common_name','db_cluster']).sum().filter(['all_species_reported']).reset_index()
        dfProb1.rename(columns = {'all_species_reported':'pos_obs'}, inplace=True)
        dfProb2 = dfProbA.groupby(['db_cluster']).sum().filter(['all_species_reported']).reset_index()
        dfProb2.rename(columns = {'all_species_reported':'tot_obs'}, inplace=True)
        dfProb3 = dfProb1.merge(dfProb2, left_on='db_cluster', right_on='db_cluster', how = 'left')
        dfProb3['pos_prob'] = dfProb3['pos_obs']/dfProb3['tot_obs']
        for loc in range(0,nLoc):
            dfWeek = dfProb3[dfProb3['db_cluster'] == loc]
            dfWeek['tf'] = list(map(lambda x: 0 if x < 0.03 else 1, dfWeek['pos_prob']))
            setMat[week,loc] = set(dfWeek[dfWeek['tf'] == 1]['common_name'].values)
        
    return setMat, nTime, n_clusters_, dfCounts

def output_generator(dfCounts, userlat, userlgn, setMat, nTime, n_clusters_):
#    print(userlat, userlgn)

    '''
    Choose between this and the other seccion.  For test, use the other one, it does not use google dist function.
    '''
#    gmaps = googlemaps.Client(key='{}'.format(Definition.GOOGLEKEY))
#    coorHotspot = np.empty((n_clusters_+1, 2))
#    coorHotspot[:,0], coorHotspot[:,1] = dfCounts['longitude'],dfCounts['latitude']
#
#    distMat = np.empty((nTime,n_clusters_))
#    countBreak = divmod(n_clusters_,100)
#
#    for i in range(0,countBreak[0]):
#        distanceMatGmaps = gmaps.distance_matrix(origins = (userlat, userlgn),
#                                              destinations=list(coorHotspot[100*i:100*(i+1)]),
#                                              mode = 'driving', units = 'metric')
#        for j in range(100*i,100*(i+1)):
#            jj = j - 100*i
#            try:
#                distMat[:,j] = distanceMatGmaps['rows'][0]['elements'][jj]['duration']['value']/3600
#            except KeyError:
#                distMat[:,j] = 100
#
#    distanceMatGmaps = gmaps.distance_matrix(origins = (userlat, userlgn),
#                                              destinations=list(coorHotspot[countBreak[0]*100:]),
#                                              mode = 'driving', units = 'metric')
#
#    for j in range(countBreak[0]*100,countBreak[0]*100+countBreak[1]):
#        jj = j - countBreak[0]*100
#        try:
#            distMat[:,j] = distanceMatGmaps['rows'][0]['elements'][jj]['duration']['value']/3600
#        except KeyError:
#            distMat[:,j] = 100
#
#    pickle.dump(distMat, open("./distMat.p", "wb" ))
#

    #==========================================================================
    #==========================================================================
    #==========================================================================

    distMat = np.random.rand(nTime*n_clusters_).reshape((nTime,n_clusters_))
#    distMat = pickle.load(open("./distMat.p", "rb" ))
    ToMakeUniverse = list(setMat.flatten())
#    print(ToMakeUniverse)
    Universe = set(e for s in ToMakeUniverse for e in s)
#
    setList, locList = SetCover.set_cover_weighted_greedy(Universe, ToMakeUniverse,list(distMat.flatten()))
    outLoc = Itinerary.location_list_maker(dfCounts,locList, nTime, n_clusters_)
    mapMarkerList = Itinerary.google_map_marker_list(dfCounts, outLoc)
#    userOut = Itinerary.dic_user_ouput_maker(dfCounts,locList,nTime, n_clusters_)
    
    dataTable = Itinerary.table_creator(dfCounts, locList, setList, nTime, n_clusters_)
    
    return mapMarkerList, dataTable

#    return 1, 2, 3






