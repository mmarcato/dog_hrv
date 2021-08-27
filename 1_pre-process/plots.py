from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd

# Function to plot polar graph
def raw_avec(df, device):
    plt.scatter(df.index, df['rr_raw'], label = 'Raw data')
    plt.scatter(df.index, df['rr_avec'], label = 'AVEC data')
    plt.legend()
    plt.title("{} Graph".format(device))
    plt.show()

# Raw bioharness and polar
def polar_bio(polar, bio, column):
    plt.scatter(polar.index, polar[column], label = 'Polar')
    plt.scatter(bio.index, bio[column], label = 'Bioharness')
    plt.legend()
    plt.title("{} - Polar vs Bioharness".format(column))
    plt.show()

def all_plot(df, device):
    plt.scatter(df.index, df['rr_raw'], label = 'Raw IBI data')
    plt.scatter(df.index, df['Inter'], label = 'Interpolated IBI data')
    #plt.scatter(df.index, df['rr_avec'], label = 'AVEC data')
    plt.xlabel('Time')
    plt.ylabel('IBI values (ms)')
    plt.legend()
    plt.title("IBI values of the {} Device".format(device))
    plt.show()

def hrv_plot(bio, polar):
    i = 16 #########################
    while i < len(bio.columns):

        pd.crosstab(bio[bio.columns[i]], polar[polar.columns[i]]).plot(kind='bar')
        #plt.bar(bio['episodes'], bio[bio.columns[i]], label =  'Bioharness data')
        #plt.bar(polar['episodes'], polar[polar.columns[i]], label =  'Polar data')
        plt.legend()
        plt.title("{} - Bio Vs Polar".format(bio.columns[i]))
        plt.xticks(rotation=90)
        plt.show()
        i += 1
