from imports import *

currentdir = os.path.dirname(os.path.realpath(__file__))
projectdir = os.path.dirname(currentdir)
sys.path.append(os.path.dirname(projectdir))


def main():


    path_polar = os.path.join(projectdir, '0_data-raw\\Edrick\\1_Polar\\2019-6-13_RR_Edrick.csv')
    path_bio =  os.path.join(projectdir, '0_data-raw\\Edrick\\1_Bioharness\\2019_06_13-13_38_51_BB_RR.csv')

    df_polar = import_polar(path_polar)
    df_bio = import_bio(path_bio)

    # defining start and finish times as a datetime object
    # start time for Edrick DC1
    start_time = dt.strptime('13/06/2019 13:38:51', '%d/%m/%Y %H:%M:%S')
    # finish time for Edrick DC1
    finish_time = dt.strptime('13/06/2019 13:52:15', '%d/%m/%Y %H:%M:%S')

    df_bio = df_bio.between_time(start_time.time(), finish_time.time())
    df_polar = df_polar.between_time(start_time.time(), finish_time.time())


    #timing the program
    #start = time()
    #polar_avec(df_polar, projectdir, "Edrick", "1", '2019-6-13_RR_Edrick.csv')
    #bio_avec(df_bio)
    #polar_bio(df_polar, df_bio)
    df_polar_avec = polar_avec(df_polar, projectdir, "Edrick", "1", '2019-6-13_RR_Edrick.csv')
    df_bio_avec = bio_avec(df_bio, projectdir, "Edrick", "1", '2019-6-13_RR_Edrick.csv')
    polar_bio_avec(df_polar_avec, df_bio_avec)
    #end = time()
    #print(df_polar.columns)

    #print('{} seconds'.format(end - start))

# Raw bioharness and polar
def polar_bio(polar, bio):
        plt.plot(polar.index, polar[' rr'])
        plt.plot(bio.index, bio['RtoR'])
        plt.legend(["Polar", "Bioharness"])
        plt.title("Raw Polar Vs Bioharness")
        plt.show()

# bioharness and polar after avec
def polar_bio_avec(polar, bio):
        plt.plot(polar.index, polar['removed out'])
        plt.plot(bio.index, bio['removed out'])
        plt.legend(["Polar", "Bioharness"])
        plt.title("Polar Vs Bioharness without Outliers")
        plt.show()

# polar raw and avec
def polar_avec(df, dir, subject, dc, filename):
    df['removed out'] = avec(list(df[' rr']))

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
    plt.plot(df.index, df[' rr'])
    plt.plot(df.index, df['removed out'])
    plt.legend(["Raw Polar", "Outliers Removed"])
    plt.title("Polar Graph")
    plt.show()

    return df

# bioharness raw and avec
def bio_avec(df, dir, subject, dc, filename):
    df["removed out"] = avec(list(df['RtoR']))
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
    plt.plot(df.index, df['RtoR'])
    plt.plot(df.index, df['removed out'])
    plt.legend(["Raw Bioharness", "Outliers Removed"])
    plt.title("Bioharness Graph")
    plt.show()

    return df

# Function to import polar data
def import_polar(path):
    parser = lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S +0000')
    df = pd.read_csv(path, index_col ='date', date_parser = parser, dayfirst = True)
    return df

# Function to import bioharness data
def import_bio(path):
    parser = lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S.%f')
    df = pd.read_csv(path, index_col ='Timestamp' , usecols = ['Timestamp', 'RtoR'], date_parser = parser, dayfirst = True)
    df.drop_duplicates(['RtoR'], keep = 'first', inplace = True)
    df['RtoR'] = round(df['RtoR'].abs()*1000)
    return df

if __name__ == '__main__':
    main()
