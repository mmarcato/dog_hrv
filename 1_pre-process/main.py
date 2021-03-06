from imports import *

currentdir = os.path.dirname(os.path.realpath(__file__))
projectdir = os.path.dirname(currentdir)
sys.path.append(os.path.dirname(projectdir))


def main():

    path_polar = os.path.join(projectdir, '0_data-raw\\Edrick\\1_Polar\\2019-6-13_RR_Edrick.csv')
    path_bio =  os.path.join(projectdir, '0_data-raw\\Edrick\\1_Bioharness\\2019_06_13-13_38_51_BB_RR.csv')

    df_polar = import_polar(path_polar)
    df_bio = import_bio(path_bio)

    # start time for Edrick DC1
    start_time = '13:38:51'
    # finish time for Edrick DC1
    finish_time = '13:52:15'

    # selecting data between start and finish times
    df_polar = df_polar.between_time(start_time, finish_time)
    df_bio = df_bio.between_time(start_time, finish_time)
    print(len(df_bio.index))

    #timing the program
    #start = time()
    # add column for with outlier detection using avec function
    df_polar = polar_avec(df_polar, projectdir, "Edrick", "1", '2019-6-13_RR_Edrick.csv')
    #end = time()
    #print('{} seconds'.format(end - start))

    df_bio = bio_avec(df_bio, projectdir, "Edrick", "1", '2019-6-13_RR_Edrick.csv')

    df_bio, df_polar = interpolate(df_bio, df_polar)
    '''
    #Raw Plots
    plots.raw_avec(df_polar, 'Polar')
    plots.raw_avec(df_bio, 'Bioharness')
    # Avec Plots
    plots.polar_bio(df_polar, df_bio, 'rr_raw')
    plots.polar_bio(df_polar, df_bio, 'rr_avec')
    # Interpolation Plot
    plots.polar_bio(df_polar, df_bio, 'Inter')
    '''
    # All plot
    #plots.all_plot(df_polar, 'Polar')
    plots.all_plot(df_bio, 'Bioharness')

    #Timesplit(df_polar, df_bio)
    #HRV(df_polar)

    # dataframe with Dog name and DC to import
    df_dogs = pd.DataFrame({
                'Dog' : ['Edrick'],
                'DC' : [1]
        })
    # path where all timestamp files are saved
    ts_path = os.path.join(projectdir, '0_data-raw')
    # dataframe containing all timestamps
    df_stats, df_episodes = timestamps(df_dogs, ts_path)

    df_bio_hrv = slide_hrv(df_episodes, finish_time, df_bio)
    df_polar_hrv = slide_hrv(df_episodes, finish_time, df_polar)

    #polar_hrv(df_polar_hrv, projectdir, "Edrick", "1", '2019-6-13_RR_Edrick.csv')
    #bio_hrv(df_bio_hrv, projectdir, "Edrick", "1", '2019-6-13_RR_Edrick.csv')

    #plots.hrv_plot(df_bio_hrv, df_polar_hrv)

    # read the nested dictionary ['Dog', 'DC'] containing, the timestamps where the episodes happen as a dataframe where columns ['Episode', 'Timestamp']

    # use the episode timestamps for 'Base-Walking' to calculate hrv metrics


# ------------------------------------------------------------------------- #
#                                Functions                                  #
# ------------------------------------------------------------------------- #

def slide_hrv(df_ep, finish_time, df):
    """
    Works its way through the episodes and calculates the hrv for that episode

    Parameters
        -------
        df_ep : Dictionary
            columns are subjects, dcs: unique combinations of dog name & dc number
        finish_time : str
            The time the testing was finished
        df : DataFrame
            The data frame of the chosen device you want to calculate hrv for

    Returns
        -------
        DataFrame of hrv calculations for each episode
    """
    df_hrv = pd.DataFrame()
    episodes = df_ep['Edrick'][1]['Episode']
    dates = df_ep['Edrick'][1].index

    ep_list = [] # list of episodes for df use
    start_list = [] # list of start times of each episode for df use
    times = [] # times is the start times of each episode
    for time in dates:
        # Turning the timestamp into datetime
        times.append(time.time())

    #df_hrv['start'] = times
    #print(df_hrv)

    # list of all the timestamps from the df
    df_times = list(df.index)

    dataframe_prep = []
    clock = 0 #used to iterate through the episodes
    while clock < len(episodes):
        intervals = []
        # The last episode is finish
        if clock == len(episodes) - 1:
            #print('Finish: {}'.format(finish_time))
            break
        i = 0
        while i < len(df_times):
            # if time in episode range add to intervals list
            if df_times[i].time() > times[clock] and df_times[i].time() < times[clock + 1]:
                intervals.append(list(df['Inter'])[i])
            i += 1
        '''
        # tests
        print('HRV Analysis for {}'.format(episodes[clock]))
        print('Start time:{}'.format(times[clock]))
        print('End time: {}'.format(times[clock + 1]))
        '''
        #checking if length of list is greater than 1 and is not an interval
        if len(intervals) > 1 and episodes[clock] != 'interval':
            dataframe_prep.append(HRV(intervals))
            ep_list.append(episodes[clock])
            start_list.append(times[clock])

        clock += 1

    # Adding to df_hrv
    df_hrv['episodes'] = ep_list # adding episodes to df_hrv
    df_hrv['start'] = start_list # adding start times to df_hrv

    fin_list = start_list # list of finish times of each episode for df use
    fin_list.pop(0) #remove start time
    fin_list.append(finish_time) # add overall finish time

    df_hrv['finish'] = fin_list # adding finish times to df_hrv

    j = 0
    while j < len(dataframe_prep[0]):
        name = list(dataframe_prep[j].keys())[j] # name of each episode
        name_list = [] # list of values of each episode
        i = 0
        while i < len(dataframe_prep):
            name_list.append(list(dataframe_prep[i].values())[0]) # adding values of each episode to list
            i += 1
        df_hrv[name] = name_list # creating new columns in df of each episode
        j += 1

    return df_hrv


def polar_hrv(df, dir, subject, dc, filename):
    # Creating folder structure
    subject_dir = os.path.join(dir, "5-hrv-analysis", subject)
    if not os.path.exists(subject_dir):
        os.mkdir(subject_dir)

    device_dir = os.path.join(dir, "5-hrv-analysis", subject, '{}_Polar'.format(dc))
    print(device_dir)
    if not os.path.exists(device_dir):
        os.mkdir(device_dir)

    path = os.path.join(projectdir, "5-hrv-analysis", subject, '{}_Polar'.format(dc), filename)
    df.to_csv(path, index=True)

def bio_hrv(df, dir, subject, dc, filename):
    # Creating folder structure
    subject_dir = os.path.join(dir, "5-hrv-analysis", subject)
    if not os.path.exists(subject_dir):
        os.mkdir(subject_dir)

    device_dir = os.path.join(dir, "5-hrv-analysis", subject, '{}_Bioharness'.format(dc))
    print(device_dir)
    if not os.path.exists(device_dir):
        os.mkdir(device_dir)

    path = os.path.join(projectdir, "5-hrv-analysis", subject, '{}_Bioharness'.format(dc), filename)
    df.to_csv(path, index=True)

# Calculate HRV Analysis
def HRV(intervals):
    return get_time_domain_features(intervals)
    #print(get_frequency_domain_features(intervals))
    '''print(get_geometrical_features(df["Inter"]))
    print(get_sampen(df["Inter"]))
    print(get_csi_cvi_features(df["Inter"]))
    print(get_poincare_plot_features(df["Inter"]))
    print(get_poincare_plot_features(df["Inter"]))
    '''

def interpolate(bio, polar):
    bio['Inter'] = interpolate_nan_values(list(bio['rr_avec'])) # new column of interpolated values
    polar['Inter'] = interpolate_nan_values(list(polar['rr_avec']))

    return bio, polar

def Timesplit(polar, bio):
    '''The Timesplit function just breaks the timestamps down into tuples
        so they are easier to pass to the  other functions.

        This function also prints the correlation between the bioharness
        and polar by taking values within every minute and creating an array
    '''
    times = []
    time_tuples = [] # time_tuples is the list of time tuples
    for date in polar.index:
        times.append(str(date).strip().split()[1]) #add all times to times list

    for time in times:
        (H, M, S) = time.split(':') #splitting the time into a tuple of hours minutes and seconds
        time_tuples.append((H, M, S)) # adding tuple times to list

    i = 0
    timestamp = []
    list = []
    start = int(time_tuples[0][1]) #start time
    end = int(time_tuples[-1][1]) # finish ime
    num = start
    count = 0 # number of polar values
    while i < len(time_tuples) and num < end:
        if int(time_tuples[i][1]) != num:
            list.append(get_index(time_tuples[i], bio, count, polar, i))
            num += 1
            count = 0 # number of polar values in any one minute
            start_time = time_tuples[i]
        if int(time_tuples[i][1]) == num:
            count += 1
        i += 1

        corrlist = [] # list of correlation coefficients
        for g in list:
            if isinstance(g, float): # if its a float add it to the corrlist
                corrlist.append(g)

def get_index(timer, bio, count, polar, polar_index):
    """
    The get_index function gets the index of the start of each minute of the polar device

    Parameters
        -------
        timer :
            list of polar time tuples
        bio : DataFrame
            bioharness df
        count : int

        polar : DataFrame
            polar df
        polar_index : int
            index of the start of each minute

    Returns
        -------
        correlation: float
            The correlation between the polar and Bioharness
    """
    times = []
    a = [] # list of (H, M, S) tuples
    for date in bio.index:
        times.append(str(date).strip().split()[1]) # adding bio times to list

    for time in times:
        (H, M, S) = time.split(':') # spliting bio times into HMS and adding to another list of tuples
        a.append((H, M, S))

    i = 0
    while i < len(a):
        if int(a[i][1]) == int(timer[1]): # if bio time and polar time are starting at the same minute
            return correlation(i, count, bio, polar, polar_index) # find correlation of values in that minute
            break
        i += 1

def correlation(index, count, bio, polar, polar_index):
    """
    The correlation function gets the correlation coefficient of the polar vs bio

    Parameters
        -------
        index :
            index of the start of each minute of the polar
        count : int
            number of values in polar list
        bio : DataFrame3
            bioharness df
        polar : DataFrame
            polar df
        polar_index : int
            index of the start of each minute

    Returns
        -------
        correlation: float
            The correlation between the polar and Bioharness
    """
    corrlist = []
    bio_inter = list(bio["Inter"])
    polar_inter = list(polar["Inter"])
    polar_list = polar_inter[polar_index: polar_index + count]

    bio_list = []
    n = 0
    while n < len(bio_inter):
        if index + count > len(bio): # if the polar list has more values than the bio, break
            break
        else:
            bio_list = bio_inter[index: index + count] # otherwise create a list of values that that is the same length as the polar list
        n += 1
    if len(polar_list) == len(bio_list): # making sure both lists are they same size
        corcoef, p_value = pearsonr(bio_list, polar_list) # get the correlation coefficient

        return corcoef # return it back to get_index function

# polar raw and avec
def polar_avec(df, dir, subject, dc, filename):
    df['rr_avec'] = avec(list(df['rr_raw']))

    # Creating folder structure
    subject_dir = os.path.join(dir, "2-data-processed", subject)
    if not os.path.exists(subject_dir):
        os.mkdir(subject_dir)

    device_dir = os.path.join(dir, "2-data-processed", subject, '{}_Polar'.format(dc))
    print(device_dir)
    if not os.path.exists(device_dir):
        os.mkdir(device_dir)

    path = os.path.join(projectdir, '2-data-processed', subject, '{}_Polar'.format(dc), filename)
    df.to_csv(path, index=True)
    return df

# bioharness raw and avec
def bio_avec(df, dir, subject, dc, filename):
    df['rr_avec'] = avec(list(df['rr_raw']))
    # Creating folder structure
    subject_dir = os.path.join(dir, "2-data-processed", subject)
    if not os.path.exists(subject_dir):
        os.mkdir(subject_dir)

    device_dir = os.path.join(dir, "2-data-processed", subject, '{}_Bioharness'.format(dc))
    print(device_dir)
    if not os.path.exists(device_dir):
        os.mkdir(device_dir)

    path = os.path.join(projectdir, '2-data-processed', subject, '{}_Bioharness'.format(dc), filename)
    df.to_csv(path, index=True)

    return df

# Function to import polar data
def import_polar(path):
    parser = lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S +0000')
    df = pd.read_csv(path, index_col ='date', date_parser = parser, dayfirst = True)
    df.rename(columns = {' rr': 'rr_raw'}, inplace = True)
    df.drop(' since start', axis = 1, inplace = True)
    return df

# Function to import bioharness data
def import_bio(path):
    parser = lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S.%f')
    df = pd.read_csv(path, index_col ='Timestamp' , usecols = ['Timestamp', 'RtoR'], date_parser = parser, dayfirst = True)
    df.drop_duplicates(['RtoR'], keep = 'first', inplace = True)
    df['RtoR'] = round(df['RtoR'].abs()*1000)
    df.rename(columns = {'RtoR': 'rr_raw'}, inplace = True)
    return df

def timestamps(df_data, base_dir):
    """
    Imports data from timestamps files, organise them in dictionaries and return

    Parameters
        -------
        df_data : DataFrame
            columns are subjects, dcs: unique combinations of dog name & dc number
        base_dir : str
            directory where timestamps are located

    Returns
        -------
        df_ep: DataFrame
            indexed by'Timestamps' containing 'Episode', 'Ep-VT' and 'Duration'
        df_stats: DataFrame
            containing 'Subject', 'DC', 'Date', 'Start time'
    """

    print('\nImporting Timestamp files - Episode and Position Data')
    stats = []
    df_ep, df_pos = {},{}

    for subj in df_data['Dog'].unique():
        df_ep[subj], df_pos[subj] = {},{}
        for dc in df_data.loc[df_data['Dog'] == subj, 'DC']:
            df_ep[subj][dc], df_pos[subj][dc] = None, None
            f_name = '%s\\%s\\%s_Timestamps.csv' % (base_dir, subj, dc)
            # if the timestamp file is found
            if os.path.exists(f_name):
                # Read the information about the behaviour test
                df_info = pd.read_csv(f_name, index_col = 0, nrows = 4, usecols = [0,1], dayfirst = False)
                date = df_info[subj]['Date']
                time = df_info[subj]['Start time']
                stats.append([subj, dc, date, time])

                dt = pd.to_datetime(date + time, format = '%d/%m/%Y%H:%M:%S' )

                # Read the EPISODE Virtual Time (VT)
                df_ep[subj][dc] = pd.read_csv(f_name, skiprows = 6, usecols = ['Episode', 'Ep-VT']).dropna()
                # Create new column for the episode Real Time (RT)
                df_ep[subj][dc].index = dt + pd.to_timedelta(df_ep[subj][dc]['Ep-VT'])
                # Create new column for the episode Duration
                ''' Add finish time column'''
                df_ep[subj][dc]['Duration'] = df_ep[subj][dc].index.to_series().diff().shift(-1)
                ''' ERROR CHECK'''
                df_ep[subj][dc]['Episode'] = df_ep[subj][dc]['Episode'].str.lower()

            else:
                print('Error loading', subj, dc)
    df_info = pd.DataFrame(stats, columns = ['Subject', 'DC', 'Date', 'Start time'])
    #logger.info('\t Imported Timestamps for \n{}'.format(df_info))


    return(df_info, df_ep)


if __name__ == '__main__':
    main()
