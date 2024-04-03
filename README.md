# CS5830_A4

## Description
This repository contains the solution for Assignment 4 of CS5830. The given task is to obtain data from the NCEI database and compare the monthly average of daily measurements and the given monthly measurements, for certain fields. Given that not all files contain data for all fields, we first fix the columns we deal with as `DailyAverageDryBulbTemperature, DailyMaximumDryBulbTemperature, 'DailyMinimumDryBulbTemperature` and `MonthlyMaximumTemperature, MonthlyMeanTemperature, MonthlyMinimumTemperature`. We then keep pinging the database, selecting one random file for downloading, until the required number of files, with all 6 columns filled are found. <br/><br/>
These files are stored in a `data` directory. The files are processed using scripts `process.py` and `prepare.py`. The output is then sent to `evaluate.py`, which returns a `csv` file with the stations as rows, `MaximumTemperature`, `MinimumTemperature`, `MeanTemperature` as columns and the $R^{2}$ score as values. <br/><br/>
We use `git` to track `params`, `source` (contains the scripts) and the `dvc` accessory files. `data` and the output files are tracked by `dvc`.

## Installation
