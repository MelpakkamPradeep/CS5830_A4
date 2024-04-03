# CS5830_A4

## Description
This repository contains the solution for Assignment 4 of CS5830. The given task is to obtain data from the NCEI database and compare the monthly average of daily measurements and the given monthly measurements, for certain fields. Given that not all files contain data for all fields, we first fix the columns we deal with as `DailyAverageDryBulbTemperature, DailyMaximumDryBulbTemperature, 'DailyMinimumDryBulbTemperature` and `MonthlyMaximumTemperature, MonthlyMeanTemperature, MonthlyMinimumTemperature`. We then keep pinging the database, selecting one random file for downloading, until the required number of files, with all 6 columns filled are found. <br/><br/>
These files are stored in a `data` directory. The files are processed using scripts `process.py` and `prepare.py`. The output is then sent to `evaluate.py`, which returns a `csv` file with the stations as rows, `MaximumTemperature`, `MinimumTemperature`, `MeanTemperature` as columns and the $R^{2}$ score as values. <br/><br/>
We use `git` to track `params`, `source` (contains the scripts) and the `dvc` accessory files. `data` and the output files are tracked by `dvc`.

## Installation
1. Clone the Git Repository: `git clone https://github.com/MelpakkamPradeep/CS5830_A4.git`
2. Navigate to the downloaded repository.
3. Install the dependencies: `conda create --name <env name> --file requirements.txt`

## Usage
1. Navigate to the downloaded repository.
2. Execute experiments using `dvc exp run -n <expt name>` or `dvc repro`
3. The final results can be found in `results/computed_r2_scores.csv`

## Notes
1. `dvc.yaml` contains the DAG of scripts for `dvc` to execute. All outputs are tracked by `dvc`.
2. `params` contains `params.yaml`. It has 2 parameters: `year` to specify the year from which the NCEI files are retrieved, and `n_locs` which gives the required number of files.
3. Until the number of `csv` files in `data/` is `n_locs`, `download.py` keeps executing.
4. `results/` shall contain 3 `csv` files: `computed_monthly_averages.csv` (output of `prepare.py`), `actual_monthly_averages.csv` (output of `process.py`) and `computed_r2_scores.csv` (output of `evaluate.py`)
5. `source/` contains the scripts for the pipeline. The functionality is as follows:
   - `evaluate.py` : 
