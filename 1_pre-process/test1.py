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

    #timing the program
    #start = time()
    df_polar = polar_avec(df_polar, projectdir, "Edrick", "1", '2019-6-13_RR_Edrick.csv')
    #end = time()
    #print('{} seconds'.format(end - start))

    df_bio = bio_avec(df_bio, projectdir, "Edrick", "1", '2019-6-13_RR_Edrick.csv')

    plots.raw_avec(df_polar, 'Polar')
    plots.raw_avec(df_bio, 'Bioharness')

    plots.polar_bio(df_polar, df_bio, 'rr_raw')
    plots.polar_bio(df_polar, df_bio, 'rr_avec')


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

if __name__ == '__main__':
    main()
