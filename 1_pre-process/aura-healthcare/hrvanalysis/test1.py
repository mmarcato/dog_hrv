from imports import *

def main():
    path_polar = '../../1_Polar/2019-6-13_RR_Edrick.csv'
    path_bio = '../../1_bioharness/2019_06_13-13_28_56_BB_RR.csv'

    df_polar = import_polar(path_polar)
    df_bio = import_bio(path_bio)

    #timing the program
    start = time()
    polar_avec(df_polar)
    #bio_avec(df_bio)
    #polar_bio(df_polar, df_bio)
    #polar_bio_avec(polar_avec(df_polar), bio_avec(df_bio))
    end = time()

    print('{} seconds'.format(end - start))

def polar_bio(polar, bio):
        plt.plot(polar.index, polar['rr'])
        plt.plot(bio.index, bio['RtoR'])
        plt.legend(["Polar", "Bioharness"])
        plt.title("Raw Polar Vs Bioharness")
        plt.show()

# not working yet
def polar_bio_avec(polar, bio):
        plt.plot(polar['removed out'])
        plt.plot(bio['removed out'])
        plt.legend(["Polar", "Bioharness"])
        plt.title("Polar Vs Bioharness without Outliers")
        plt.show()


def polar_avec(df):
    rlist = list(df['rr'])
    outlier_removed = avec(rlist)
    df['removed out'] = outlier_removed
    df.to_csv("polar_test.csv", index=True)
    plt.plot(df.index, df['rr'])
    plt.plot(df.index, df['removed out'])
    plt.legend(["Raw Polar", "Outliers Removed"])
    plt.title("Polar Graph")
    plt.show()

def bio_avec(df):
    rlist = list(df['RtoR'])
    outlier_removed = avec(rlist)
    df["removed out"] = outlier_removed
    #df.to_csv("test.csv", index=True)
    plt.plot(df.index, df['RtoR'])
    plt.plot(df.index, df['removed out'])
    plt.legend(["Raw Bioharness", "Outliers Removed"])
    plt.title("Bioharness Graph")
    plt.show()

# Function to import polar data
def import_polar(path):
    parser = lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S +0000')
    df = pd.read_csv(path, index_col ='date', date_parser = parser, dayfirst = True)
    return df

# Function to import bioharness data
def import_bio(path):
    parser = lambda x: datetime.strptime(x,'%d/%m/%Y %H:%M:%S.%f')
    df = pd.read_csv(path, index_col ='Timestamp' , usecols = ['Timestamp', 'RtoR'], date_parser = parser, dayfirst = True)
    df.drop_duplicates(['RtoR'], keep = 'first', inplace = True)
    df['RtoR'] = round(df['RtoR'].abs()*1000)
    return df

if __name__ == '__main__':
    main()
