import sys
from hrvanalysis.extract_features import (get_time_domain_features, get_geometrical_features,
                                          _create_interpolated_timestamp_list, get_sampen,
                                          get_csi_cvi_features, get_poincare_plot_features,
                                          get_frequency_domain_features, _get_freq_psd_from_nn_intervals,
                                          get_poincare_plot_features)
from hrvanalysis.plot import (plot_timeseries, plot_distrib, plot_poincare, plot_psd)
from hrvanalysis.preprocessing import (remove_outliers, interpolate_nan_values,
                                       remove_ectopic_beats, get_nn_intervals)


def aura(nn_intervals):
    # HRV Analysis
    print(get_time_domain_features(nn_intervals))
    print(get_geometrical_features(nn_intervals))
    print(_create_interpolated_timestamp_list(nn_intervals))
    print(get_sampen(nn_intervals))
    print(get_csi_cvi_features(nn_intervals))
    print(get_poincare_plot_features(nn_intervals))
    print(get_frequency_domain_features(nn_intervals))
    print(_get_freq_psd_from_nn_intervals(nn_intervals))
    print(get_poincare_plot_features(nn_intervals))

    #Plot functions
    plot_timeseries(nn_intervals)
    plot_distrib(nn_intervals)
    plot_poincare(nn_intervals)
    plot_psd(nn_intervals)

    # Preprocessing
    interpolate_nan_values(nn_intervals)
    remove_ectopic_beats(nn_intervals)
    get_nn_intervals(nn_intervals)
