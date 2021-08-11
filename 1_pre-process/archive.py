#--- None of these functions are being used anymore ---#
def align(polar, bio):
    df_align = polar.join(bio, how='outer', rsuffix='_bio')
    df_align.to_csv('Experiment2.csv')
    p_list = df_align["rr_avec"]
    b_list = df_align['rr_avec_bio']

    combined = []
    i = 0
    while i < len(b_list):
        if np.isnan(b_list[i]) and not np.isnan(p_list[i]):
            combined.append(p_list[i])
        elif np.isnan(p_list[i]) and not np.isnan(b_list[i]):
            combined.append(b_list[i])
        #elif np.isnan(b_list[i]) and np.isnan(p_list[i]):

        i += 1
        return combined

def correlate(df_bio, df_polar):
    # estimate of the correlation between the polar and bioharness

    bio = list(df_bio['Inter'])
    polar = list(df_polar['Inter'])

    # sliding window of 30
    w_size = 15
    i = w_size
    j = w_size + 10
    corrlist = [] # list of all the correlation coefficients
    while i < len(bio) - w_size:
        x = bio[i - w_size : i + w_size]
        y = polar[j - w_size: j + w_size]
        #print(len(x), len(y))
        corcoef, p_value = pearsonr(x, y)
        corrlist.append(corcoef)
        i += 1
        j += 2


    correlation = sum(corrlist) / len(corrlist)
    print(correlation)

def iqr_outliers(nn_intervals):
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
