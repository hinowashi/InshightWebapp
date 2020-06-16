import pandas as pd
import numpy as np


def google_map_marker_list(df, locations):
    '''
    Makes a python list that is use to generate the markers on the live google map.

    Arg:
        df: The dataframe form DBScaner.cluster_center.  It has the location name, lat, lgn and cluster number.
        locations:  The list of unique locations obtain from the set cover.
        
    Out:
        mapMakerList: python list with the form: [[location, latitude, longitue]....[..]]
    '''
    mapMarkerList = []
    for i in locations:
        lat = df.loc[df['locality'] == i].iloc[0]['latitude']
        lng = df.loc[df['locality'] == i].iloc[0]['longitude']
        mapMarkerList.append([i,lat,lng])
        
    return mapMarkerList

def location_list_maker(df, rawLocList, nTime, nLoc):
    '''
    Uses the raw output form the SetCover.set_cover_weighted_greedy or SetCover.set_cover_greedy methods to obtain the list of unique places that will be visited. The locations are transformed back to a (time,location) configuration and then just o a location format.
    
    Arg:
        rawLocList: Raw locations form the set_cover method.
        nTime: The number of time intervals (tipicaly 54)
        nLoc: The number of unique total hotspots.
        
    Out:
        outLoc: List of unique locations.
    
    '''
    locMat = np.linspace(1,nTime*nLoc,nTime*nLoc).reshape(nTime,nLoc)
    outLoc = set()
    for element in sorted(rawLocList):
        week,loc = np.where(locMat == element)
        outLoc |= set([df.loc[df['db_cluster'] == loc[0]].iloc[0]['locality']])
    outLoc = list(outLoc)
    return outLoc

def dic_user_ouput_maker(df, rawLocList, nTime, nLoc):
    '''
    Creates the dictionary that will be use to give the user the output it required.  The keys will be the different weeks and the entries the different location as labels.  The locations most likely will not make sence the the user and that is why the will have coordinates.
    
    Arg:
        rawLocList: Raw locations form the set_cover method.
        nTime: The number of time intervals (tipicaly 54)
        nLoc: The number of unique total hotspots.
        
    Out:
        userOut: dic with keys with the form of: 'week 1' and the values is a list of the different locations to visit.
    '''

    locMat = np.linspace(1,nTime*nLoc,nTime*nLoc).reshape(nTime,nLoc)

    userOut = {}
    for element in sorted(rawLocList):
        week,loc = np.where(locMat == element)
        placeNew = df.loc[df['db_cluster'] == loc[0]].iloc[0]['locality']
        key = 'week {}'.format(str(week[0]))
        if key in userOut.keys():
            placeOld = userOut[key]
            placeOld.extend([placeNew])
            userOut[key] = placeOld
        else:
            userOut[key] = [placeNew]
            
    return userOut
