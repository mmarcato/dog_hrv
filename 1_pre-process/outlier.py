from math import sqrt
from scipy.special import erfinv
import pandas as pd
import numpy as np
import statistics


def alpha_a (n, p):
	return(sqrt(2) * erfinv( 2 * pow(p/100, 1/n) - 1 ))

def alpha_b (n, p):
	return(sqrt(2) * erfinv( p/50 - 1 ))

def k(n, p):
	a = alpha_a(n,p)
	b = alpha_b(n,p)

	#print(a,b)

	k_numerator = 2*(n-1)
	k_denominator = 2*(n-1) - b**2

	k_sqrt_num = n * a**2 + 2*(n-1) - b**2
	k_sqrt_den = 2 * n * (n-1)

	k_multiplier = a + b * sqrt(k_sqrt_num / k_sqrt_den)

	k = k_numerator/k_denominator * k_multiplier

	return (k)

def avec(rr_raw, p = 0.74, n = 41):
	'''
	Takes an array of datapoints to evaluate whether xd is an outlier
	where xd is the middle point [ ... , xd, ... ]

	Parameters:
	rr_raw - list of rr data

	Return:
	rr_avec

	'''
	# window size is 20
	w_size = int((n - 1)/2)
	# rr size
	rr_size = len(rr_raw)
	
	# Counting the number of outliers
	count_outliers = 0
	# empty list
	rr_avec = []

	# Adding first 20 numbers to array
	rr_avec = rr_raw[:w_size]
	for mid in range(w_size, (rr_size - w_size)):
		# Mid and i are the same, both the middle number
		start = mid - w_size
		end = mid + w_size
		''' for every iteration x is gonna be the 20 values before mid
		and 20 numbers after
		'''
		x = rr_raw[start : mid] + rr_raw[mid : end]

		xg = rr_raw[mid]
		if abs(xg - statistics.mean(x)) > k(n, p) * statistics.stdev(x):
			# if true add None to the list, same as returning np.nan
			rr_avec.append(None)
			count_outliers += 1

		else:
			#otherwise add xg to the list
			rr_avec.append(xg)

	# Adding last 20 numbers to array
	rr_avec.extend(rr_raw[rr_size - w_size:])

	print('Number of Outliers detected in sample', count_outliers)
	print('Percentage of Outliers detected in sample', (count_outliers/rr_size))

	return (rr_avec)
