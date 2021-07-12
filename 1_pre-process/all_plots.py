# Function to plot polar graph
def Polar_plot(nn_intervals):
    plt.plot(nn_intervals)
    plt.plot(Outlier(nn_intervals))
    plt.legend(["Raw Polar", "Outliers Removed"])
    plt.title("Polar Graph")
    plt.show()

# Function to plot bioharness graph
def Bioharness_plot(bb_intervals):
    plt.plot(bb_intervals)
    plt.plot(Outlier(bb_intervals))
    plt.legend(["Raw Bioharness", "Outliers Removed"])
    plt.title("Bioharness Graph")
    plt.show()

# Function to plt bioharness and polar graph
def Biopolar_plot(nn_intervals, bb_intervals):
    plt.plot(bb_intervals)
    plt.plot(nn_intervals)
    plt.legend(["Raw Bioharness", "Raw Polar"])
    plt.title("Bioharness Vs Polar")
    plt.show()
