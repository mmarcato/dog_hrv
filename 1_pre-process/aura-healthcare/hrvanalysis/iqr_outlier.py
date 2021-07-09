def Outlier(nn_intervals):
    outliers = []
    #sort nn_intervals so outliers are easier to see
    sort = sorted(nn_intervals)

    #getting lower and upper quartiles
    Q1, Q3 = np.percentile(sort, [25, 75])
    IQR = Q3 - Q1
    lower = Q1 - ((IQR) * 1.5)
    upper = Q3 + ((IQR) * 1.5)

    i = 0
    while i < len(nn_intervals):
        if nn_intervals[i] < lower or nn_intervals[i] > upper:
            #adding to outliers list if it is outside of the IQR
            outliers.append(nn_intervals[i])
            #replce with N/A
            nn_intervals[i] = None
        i += 1

    return nn_intervals
