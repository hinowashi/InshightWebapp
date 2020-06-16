import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN

def cluster_selection(df, eps=0.05, min_samples=3):
    '''
    Calculates for a given geographical region identify in the dataframe, the location of where bird watchers tend to go more often. This does not qualifies the goodness of the locations just that are locations used by birders. A bird watching cluster is defined by having at least 3 birding locations all up to 5km apart (eps =0.05) 
    
    Arg:
        df: The data frame of the geographical region, from it both latitude and longitude will be use to determine the clusters
        eps: Max separation between points in the BDSCAN clustering algorithm. eps = 0.01~1km
        min_sample: A cluster need to have atleast 3 birding spots.  
        
    Out:
        dfcluster: Data frame with the latitude,logitude, location name and cluster ID for all the points in the region.
        labels: List of label asigment (cluster number) for each of the different points. '-1' means they are not part of a cluster.
        n_clusters_: Total number of different clusters (it includes the '-1' points).
    
    
    '''
    dfcluster = df.filter(['locality','latitude', 'longitude'])
    dfcluster.drop_duplicates(subset='latitude', keep = 'first', inplace = True)
    locationList = np.array((dfcluster['latitude'],dfcluster['longitude'])).T
    
    dbmod = DBSCAN(eps=eps, min_samples=min_samples, metric='euclidean').fit(locationList)
    
    labels = dbmod.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    
    dfcluster['db_cluster'] = labels
    
    return dfcluster, labels, n_clusters_

def hotspot_finder(df):
    '''
    Finds the number of different bird species seen at each of the different locations (time averaged).  This generates a ranking that will be used to find the center of the BDSCAN cluster.
    
    Arg:
        df:  The dataframe with all the information
        
    Out:
        dfLocations: a dataframe with the number of different bird species seen a each of the different hotspots.
    '''
    
    dfLocations = pd.pivot_table(df, values='all_species_reported', index=['locality'],columns=['common_name'], aggfunc=np.min)
    dfLocations['tot_bird_species'] = dfLocations.sum(axis=1)
    dfLocations = dfLocations.reset_index()
    dfLocations = dfLocations.filter(['locality','tot_bird_species']).sort_values(by='tot_bird_species', ascending=False)
    return dfLocations

def cluster_center(dfcluster, df):
    '''
    Finds the best birding location in each of the clusters, to use as a cluster center and to give navigation address. This will send you to the most likely area in witch you will see the most number of birds.
    
    Arg:
        df: The dataframe with all the information
        dfcluster: Data frame with the latitude,logitude, location name and cluster ID for all the points in the region.
        
    Out:
        dfProb: Selects the location with the highest number of bird sightings for each of the clusters.
    '''
    dfProb = dfcluster.merge(hotspot_finder(df), left_on='locality', right_on='locality', how = 'left')
    dfProb = dfProb.groupby(['db_cluster']).max().reset_index().filter(['db_cluster',
                                                                        'locality',
                                                                        'tot_bird_species'])
    dfProb = dfProb.merge(dfcluster, left_on='locality', right_on='locality', how = 'left')
    dfProb.drop(['db_cluster_x'], axis=1, inplace=True)
    dfProb.rename(columns={'db_cluster_y': 'db_cluster'}, inplace=True)
    return dfProb

# def color_data(df,labels):
#     unique_labels = set(labels)
#     print(unique_labels)
#     colors = np.array([plt.cm.viridis_r(each) for each in np.linspace(0, 1, len(unique_labels))])
# #     dfColors = df.filter(['LATITUDE', 'LONGITUDE'])
#     dfaa = pd.DataFrame(data = {'COLOR': colors, 'BD CLUSTER': np.array(list(unique_labels))})      
#     return dfaa
