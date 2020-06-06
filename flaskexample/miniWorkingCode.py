import numpy as np
import pickle

def set_cover_mine(elements, subsets, initset):
   '''
   There is a greedy algorithm for polynomial time approximation of set covering that chooses sets according to one rule: at each stage, choose the set that contains the largest number of uncovered elements.
   '''
   covered = initset.copy()
   cover = []
   listCover = []
   # Greedily add the subsets with the most uncovered points
   while covered != elements:
       subset = max(subsets, key=lambda s: len(s - covered))
       cover.append(subset)
       listCover.append(subsets.index(subset))
       covered |= subset
   return cover, listCover
   
def analysis(userInputLat,userInputLon):
    userInput = [userInputLat,userInputLon]
    kmeansLoaded = pickle.load(open("./flaskexample/static/kmeansModel.p", "rb" ))
    setMatLoaded = pickle.load(open("./flaskexample/static/2dSetLocations.p", "rb" ))
    initialLocSet = setMatLoaded[0,kmeansLoaded.predict([userInput])[0]]
    ToMakeUniverse = list(setMatLoaded.flatten())
    Universe = set(e for s in ToMakeUniverse for e in s)
    setList, locList = set_cover_mine(Universe, ToMakeUniverse, initialLocSet)
    locList = np.sort(locList)
    nTime, nLoc = setMatLoaded.shape
    locMat = np.linspace(1,nTime*nLoc,nTime*nLoc).reshape(nTime,nLoc)
    outList = ['On week 0, you need to be at location {}'.format(kmeansLoaded.predict([userInput])[0])]
    for element in locList:
        a,b = np.where(locMat == element)
        outList.append('On week {}, you need to be at location {}'.format(a[0],b[0]))
    return outList
