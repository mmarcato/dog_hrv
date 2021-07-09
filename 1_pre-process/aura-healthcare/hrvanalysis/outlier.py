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

def avec(sample):
	'''
	Takes an array of datapoints to evaluate whether xd is an outlier
	where xd is the middle point [ ... , xd, ... ]

	Parameters:
	rr_sample - array of size n where xd is the middle point

	Return:
	np.nan  - if xd is an outlier
	xd      - if xd is not an outlier

	'''

	#empty list
	new_list = []
	#window size is 20
	w_size = 20
	# Counting the number of outliers
	count_outliers = 0
	# Adding first 20 numbers to array
	new_list = sample[:w_size]
	# p is the confidence level
	p = 0.75
	# n is the length of the sample
	n = len(sample)
	for mid in range(w_size, n - w_size):
		# Mid and i are the same, both the middle number
		start = mid - w_size
		end = mid + w_size
		''' for every iteration x is gonna be the 20 values before mid
		and 20 numbers after
		'''
		x = sample[start : mid] + sample[mid : end]

		xg = sample[mid]
		if abs(xg - statistics.mean(x)) > k(n, p) * statistics.stdev(x):
			# if true add None to the list, same as returning np.nan
			new_list.append(None)
			count_outliers += 1

		else:
			#otherwise add xg to the list
			new_list.append(xg)

	# Adding last 20 numbers to array
	for i in sample[n-w_size:]:
		new_list.append(i)

	return new_list
