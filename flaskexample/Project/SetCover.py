import numpy as np

def universe_maker(setsList):
    '''
    This alorithm determines the universe of elements contain on the list of sets 'setList'.  To do that it uses a double loop that adds the elements to 'universe' set.  Since 'universe' is a set only unique elements are store.
    
    Arg:
        setsList: is a list of all the sets
        
    Out:
        universe:  is a set of all the elements

    '''
    universe = set(e for s in setsList for e in s)
    
    return universe


def set_cover_greedy(universe, setsList):
   '''
   This alorithm for the set cover problem uses the greedy alorithm.  The rule that follows is choosing the set that contains the largest number of uncovered elements.
   This alorithm is a ln n –approximation.
   
   Arg:
        universe:  is a set of all the elements
        setsList: is a list of all the sets

   Out:
        cover: is the list of sets that covers the hole universe.
        listCover: is the list that indicates what set (number) was use to forn the cover.
   '''
    
   if universe_maker(setsList) != universe:
        raise ValueError('There is a discrepancy between the universe input and the universe constructed from the list of sets.')
   
   covered = set()
   cover = []
   listCover = []
   while covered != universe:
        subSet = max(setsList, key=lambda s: len(s - covered))
        cover.append(subSet)
        listCover.append(setsList.index(subSet))
        covered |= subSet

   return cover, listCover
   
   
def set_cover_weighted_greedy(universe, setsList, weightList, normalize = True):
    '''
    This alorithm for the set cover problem uses the greedy alorithm.  The rule that follows is choosing the set that is most efficent at adding new elements.  The efficency is deffiend as the new elements to be added weighted by their cost.
    This alorithm is a ln n –approximation.
   
    Arg:
        universe:  is a set of all the elements
        setsList: is a list of all the sets

   Out:
        cover: is the list of sets that covers the hole universe.
        listCover: is the list that indicates what set (number) was use to forn the cover.
   '''
    
    if universe_maker(setsList) != universe:
        raise ValueError('There is a discrepancy between the universe input and the universe constructed from the list of sets.')
        
    if len(setsList) != len(weightList):
        raise ValueError('The two list have different lenghts')
   
    covered = set()
    cover = []
    listCover = []
    
    #The weights are normalized, limits numerical errors.
    if normalize == True:
        weightList = weightList/np.mean(weightList)
        
    while covered != universe:
        #setWeightStep is the list of cost given what is alrady present in covered. When a set does not gives value (no new items) it assings a 0.
        setWeightStep = list(map(lambda x, y: len(x -covered)/y if len(x -covered) != 0 else 0, setsList, weightList))
        #It will give the first element on the setWeightStep that is the most efficent. It is likely that more than one index will have the min same value.  In such cases a secondary cost function could be use to separate them. s
        index = setWeightStep.index(max(setWeightStep))
        cover.append(setsList[index])
        listCover.append(index)
        covered |= setsList[index]

    return cover, listCover
