from matplotlib import pyplot as plt

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