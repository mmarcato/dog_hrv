# Dog HRV - Heart Rate Variability
This repository constains scripts to process ECG(electrocardiogram) and RR(R to R invervals)/IBI(InterBeat Interval) data. 

## Folders

0. data-raw: raw .csv files from start to finish of the behaviour test. Folder structure: Subject/DC_Device/filename.csv
1. pre-process: scripts to process files (clean rr). 
    - bioharness
    - polar
    - combine both?
2. data-processed: processed .csv files from start to finish. Folder structure: Subject/DC_Device/filename-processed.csv
3. hrv-metrics: 
    - imports rr processed files and timestamps files
    - calculates hrv metrics considering the timestamp files 
    - outputs a final dataframe 
4. data-hrv: final dataframe (row = dogs, columns = dc_subtest_hrv-metric)
5. hrv-analysis: 
    - imports/combines hrv-data and dog demographics datasets 
    - hypothesis test if there are differences between groups considering sex, breed, source, **training outcome** 

