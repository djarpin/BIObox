#!/usr/local/bin/python

from CreateBiogemeCode import *

alternatives = list(range(21))

# Simple MNL Model
b = BiogemeCode(alternatives)
b.add_utility('V# = ASC_# + PRICE * pct_price_change_#')
b.add_comment('Need to fix a single ASC at 0')
b.write_file('mnl.py')

# Alternative specific price elasticity
b1 = BiogemeCode(alternatives)
b1.add_utility('V# = ASC_# + PRICE_# * pct_price_change_#')
b1.add_comment('Need to fix a single ASC at 0')
b1.write_file('mnl_altprice.py')

# 3 Latent class model
b2 = BiogemeCode(alternatives)
b2.add_utility('A_V# = A_ASC_# + A_PRICE * pct_price_change_#')
b2.add_utility('B_V# = B_ASC_# + B_PRICE * pct_price_change_#')
b2.add_utility('C_V# = C_ASC_# + C_PRICE * pct_price_change_#')
b2.add_latent_class('CLASS_# = INTERCEPT_# + MALE_# * male')
b2.add_comment('Need to fix a single ASC at 0')
b2.write_file('lc.py')

# 3 nest logit
b3 = BiogemeCode(alternatives)
b3.add_utility('V# = ASC_# + PRICE * pct_price_change_#')
b3.add_nest([0])
b3.add_nest([1, 3, 5, 7, 9, 11, 13, 15, 17, 19])
b3.add_nest([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
b3.add_comment('Need to fix a single ASC at 0')
b3.add_comment('Need to change SCALE start and lower bound')
b3.write_file('nest.py')

# Scale varying model (HEV approximation)
# Also shows method for changing coefficient parameters
b4 = BiogemeCode(alternatives)
b4.add_utility('V# = (ASC_# + PRICE * pct_price_change_#) * SCALE_#')
b4.add_comment('Need to fix a single ASC at 0')
b4.add_comment('Need to fix a single SCALE at 1')
b4.coefficients['SCALE_#']['start'] = 1
b4.coefficients['SCALE_#']['lower_bound'] = 0.01
b4.write_file('hev.py')

# Change initialization parameters for all coefficients
b5 = BiogemeCode(alternatives)
b5.initial = {'start': 0, 'lower_bound': -10, 'upper_bound': 10, 'estimate': 0}
b5.add_utility('V# = ASC_# + PRICE * pct_price_change_#')
b5.add_comment('Need to fix a single ASC at 0')
b5.write_file('bound.py')
