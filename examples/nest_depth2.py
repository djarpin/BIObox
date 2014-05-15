# Biogeme model file bio_test_nest2.py
from biogeme import *
from headers import *
from nested import *
from cnl import *
from distributions import *
from loglikelihood import *
from statistics import *
import collections

# Specify coefficients
PRICE = Beta('PRICE', 0, -100, 100, 0)
ASC_0 = Beta('ASC_0', 0, -100, 100, 1)
ASC_1 = Beta('ASC_1', 0, -100, 100, 0)
ASC_2 = Beta('ASC_2', 0, -100, 100, 0)
ASC_3 = Beta('ASC_3', 0, -100, 100, 0)
ASC_4 = Beta('ASC_4', 0, -100, 100, 0)
ASC_5 = Beta('ASC_5', 0, -100, 100, 0)
ASC_6 = Beta('ASC_6', 0, -100, 100, 0)
ASC_7 = Beta('ASC_7', 0, -100, 100, 0)
ASC_8 = Beta('ASC_8', 0, -100, 100, 0)
ASC_9 = Beta('ASC_9', 0, -100, 100, 0)
ASC_10 = Beta('ASC_10', 0, -100, 100, 0)
ASC_11 = Beta('ASC_11', 0, -100, 100, 0)
ASC_12 = Beta('ASC_12', 0, -100, 100, 0)
ASC_13 = Beta('ASC_13', 0, -100, 100, 0)
ASC_14 = Beta('ASC_14', 0, -100, 100, 0)
ASC_15 = Beta('ASC_15', 0, -100, 100, 0)
ASC_16 = Beta('ASC_16', 0, -100, 100, 0)
ASC_17 = Beta('ASC_17', 0, -100, 100, 0)
ASC_18 = Beta('ASC_18', 0, -100, 100, 0)
ASC_19 = Beta('ASC_19', 0, -100, 100, 0)
ASC_20 = Beta('ASC_20', 0, -100, 100, 0)

SCALE311 = Beta('SCALE311', 1, 0.01, 100, 0)
SCALE312 = Beta('SCALE312', 1, 0.01, 100, 0)
SCALE321 = Beta('SCALE321', 1, 0.01, 100, 0)
SCALE322 = Beta('SCALE322', 1, 0.01, 100, 0)
SCALE210 = Beta('SCALE210', 1, 0.01, 100, 0)
SCALE220 = Beta('SCALE220', 1, 0.01, 100, 0)
SCALE100 = Beta('SCALE100', 1, 0.01, 100, 1)

# Specify utility functions
V0 = ASC_0 + PRICE * pct_price_change_0
V1 = ASC_1 + PRICE * pct_price_change_1
V2 = ASC_2 + PRICE * pct_price_change_2
V3 = ASC_3 + PRICE * pct_price_change_3
V4 = ASC_4 + PRICE * pct_price_change_4
V5 = ASC_5 + PRICE * pct_price_change_5
V6 = ASC_6 + PRICE * pct_price_change_6
V7 = ASC_7 + PRICE * pct_price_change_7
V8 = ASC_8 + PRICE * pct_price_change_8
V9 = ASC_9 + PRICE * pct_price_change_9
V10 = ASC_10 + PRICE * pct_price_change_10
V11 = ASC_11 + PRICE * pct_price_change_11
V12 = ASC_12 + PRICE * pct_price_change_12
V13 = ASC_13 + PRICE * pct_price_change_13
V14 = ASC_14 + PRICE * pct_price_change_14
V15 = ASC_15 + PRICE * pct_price_change_15
V16 = ASC_16 + PRICE * pct_price_change_16
V17 = ASC_17 + PRICE * pct_price_change_17
V18 = ASC_18 + PRICE * pct_price_change_18
V19 = ASC_19 + PRICE * pct_price_change_19
V20 = ASC_20 + PRICE * pct_price_change_20

# Specify utility lookup
V = {0: V0,
     1: V1,
     2: V2,
     3: V3,
     4: V4,
     5: V5,
     6: V6,
     7: V7,
     8: V8,
     9: V9,
     10: V10,
     11: V11,
     12: V12,
     13: V13,
     14: V14,
     15: V15,
     16: V16,
     17: V17,
     18: V18,
     19: V19,
     20: V20}

# Specify availability lookup
AV = {0: available_0,
      1: available_1,
      2: available_2,
      3: available_3,
      4: available_4,
      5: available_5,
      6: available_6,
      7: available_7,
      8: available_8,
      9: available_9,
      10: available_10,
      11: available_11,
      12: available_12,
      13: available_13,
      14: available_14,
      15: available_15,
      16: available_16,
      17: available_17,
      18: available_18,
      19: available_19,
      20: available_20}

# Define multi-level nests
TREE = collections.OrderedDict([
    (0, 100),
    (1, 311), 
    (3, 311), 
    (5, 311), 
    (7, 311), 
    (9, 311), 
    (11, 312), 
    (13, 312), 
    (15, 312), 
    (17, 312), 
    (19, 312), 
    (2, 321),
    (4, 321),
    (6, 321),
    (8, 321),
    (10, 321),
    (12, 322),
    (14, 322),
    (16, 322),
    (18, 322),
    (20, 322),
    (311, 210),
    (312, 210),
    (321, 220),
    (322, 220),
    (210, 100),
    (220, 100)])

# Associate nest nodes with scale coefficients
SCALE = {311: SCALE311,
         312: SCALE312,
         321: SCALE321,
         322: SCALE322,
         210: SCALE210,
         220: SCALE220,
         100: SCALE100}

# Multilevel nest likelihood creation
def getMevForMultiLevelNested(V,av,tree,param,rootcode=0):
    availability = av.copy()
    y = {}
    for i,v in V.items() :
        y[i] = exp(v)
    Gi = {}
    def ifavail(i,val):
        return Elem({0:0.0,1:val},availability[i]!=0)
    param[rootcode] = 1.0
    tree[rootcode] = rootcode
    for parent in param.keys():
        availability[parent] = 0
        y[parent] = 0.0
    #calculate y on up
    for child, parent in tree.items():
        if child in param:
            y[child] = y[child] ** (1.0/param[child])
        y[parent] += ifavail(child, y[child] ** param[parent])
        availability[parent] = Elem({0:availability[child],1:1},availability[parent]!=0)
    # calculate Gi
    for i in V.keys() :
        n = tree[i]
        Gi[i] = y[i]**(param[n]-1.0)
        nn = tree[n]
        while nn!=n:
            Gi[i] *= y[n]**(param[nn] - param[n])
            n = nn
            nn = tree[n]
        Gi[i] = Elem({0: (0), 1: Gi[i]}, availability[i]!=0)
    return Gi

GI = getMevForMultiLevelNested(V, AV, TREE, SCALE, rootcode=100)

# Maximize likelihood
rowIterator('obsIter')
PROB_V = mev(V, GI, AV, chosen)
BIOGEME_OBJECT.ESTIMATE = Sum(log(PROB_V), 'obsIter')

# Set optimization parameters
BIOGEME_OBJECT.PARAMETERS['stopFileName'] = 'nest_depth2.py.stop'
BIOGEME_OBJECT.PARAMETERS['optimizationAlgorithm'] = 'BIO'
