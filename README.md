# Dog HRV - Heart Rate Variability
This repository constains scripts to process ECG(electrocardiogram) and RR(R to R invervals)/IBI(InterBeat Interval) data. 

## Folders

0. data-raw: raw .csv files from start to finish of the behaviour test. Folder structure: Subject/DC_Device/filename.csv. e.g. Douglas/1_Bioharness/'2019_05_20-13_36_29_BB_RR.csv'
1. pre-process: scripts to process files -> import raw files / clean rr data with algorithm (avec). 
    - bioharness
    - polar
2. data-processed: processed .csv files from start to finish. Folder structure: Subject/DC_Device/filename-processed.csv
3. hrv-metrics: 
    - imports rr processed files and timestamps files
    - calculates hrv metrics considering the timestamp files 
    - outputs a final dataframe 
4. data-hrv: final dataframe (row = dogs, columns = dc_subtest_hrv-metric)
5. hrv-analysis: 
    - imports/combines hrv-data and dog demographics datasets 
    - hypothesis test if there are differences between groups considering sex, breed, source, **training outcome** 

