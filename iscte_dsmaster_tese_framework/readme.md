
# Plumbline Sensor Data Quality Framework

This repository implements a **Data Quality Framework (DQF)** specifically designed to evaluate and monitor the quality of time series data from *plumbline sensors* used in **structural health monitoring (SHM)** of dams.

The framework is modular, extensible, and instrument-agnostic, but the current implementation focuses on a real-world use case involving *manual* and *automatic* readings from plumbline instruments.

## Architecture Overview

The framework is divided into several modules, each responsible for a layer of the data quality pipeline:

- **Input Layer**: Ingests `.txt` files from sensors.
- - automatic reading mode [RAD] - e.g. - RADFIOPRUMOBASECOORD49352.txt
- - manual reading mode [RMD] - e.g. - RMDFIOPRUMOBASECOORD49355.txt
- **Profiling Layer**: Generates profiling reports (HTML + plots) per sensor/year.
- **DQ Checks Layer**: Applies Timeliness and Completeness checks.
- **Threshold Validation Layer**: Evaluates DQ metrics against predefined thresholds.
- **Visualization Layer**: Generates plots for DQ metrics and displacement data.
- **Orchestration Layer**: Handles execution modes and controls workflow per file/year.

## Directory Structure

```
configs/
├── framework.py                 # Global configuration
├── manual.json                  # Instrument-specific thresholds & parameters

data/
├── in/
│   └── dq_framework/
│       └── plumbline/           # Input sensor files (.txt)
├── out/
    └── dq_framework/
        └── plumbline/
            ├── displacements_visuals/
            ├── dqchecks/
            ├── dqchecks_visuals/
            ├── log/
            ├── profiling/
            ├── profiling_visuals/
            ├── profiling_visuals/
            ├── threshold_validator/
            ├── threshold_validator_visuals/
```

## Features

- **Time Series Aware**: Designed to handle `ANO`, `MES`, `DIA`, `HORA`, `MINUTO`-based data.
- **Modular Checks**: `Timeliness` and `Completeness` checks by read mode (automatic [RAD] or manual [RMD] files)
- **Threshold Validator**: Flags metrics as `OK`, `WARNING`, `ALERT`, or `NO THRESHOLD`.
- **Visual Reports**: Generates violin plots, bar charts, and profiling summaries.
- **Flexible Execution for Read Mode**: Supports `manual`, `automatic`, or `all` read modes. 
- **Flexible Execution for List of sensors**: Supports `49352`, `49352 49353`, or `all` sensors.
- **Flexible Execution for List of Years**: Supports `2023`, `2023 2024`, or `all` years.
- 
## DQ Dimensions Implemented

| Dimension     | Checks Implemented                              | Metric Type      |
|---------------|-------------------------------------------------|------------------|
| Completeness  | Expected vs actual count, missing data rate     | abs (Absolute/Decimal Values), prctg (Percentage values)       |
| Timeliness    | Record interval, max gaps, data density         | abs (Absolute/Decimal Values), prctg (Percentage values)       |


##  Execution Modes
You can replicate the work done in my project by running th following command:
```bash
python .\src\dq_framework\dq_framework_exec.py --instrument plumbline --mode all --id_list 49352  --year_list 2024
```

Other available examples:
```bash
python .\src\dq_framework\dq_framework_exec.py --instrument plumbline --mode all --id_list all  --year_list all
```
```bash
python .\src\dq_framework\dq_framework_exec.py --instrument plumbline --mode automatic --id_list 49352 49353  --year_list 2024
```
```bash
python .\src\dq_framework\dq_framework_exec.py --instrument plumbline --mode manual --id_list 49352  --year_list 2024 2025
```


## Main Scripts' Modules

| Script | Purpose |
|--------|---------|
| `data_profiler.py` | Implements Data Profiling outputs |
| `dq_checks.py` | Implements timeliness & completeness checks |
| `dq_checks_visuals.py` | DQ metric plotting |
| `dq_threshold_validator.py` | Threshold classification engine |
| `dq_threshold_validator_visuals.py` | Threshold + table plots |
| `displacements_visuals.py` | Monthly & moving average plots |
| `dq_utils.py` | Logger, directory manager, file I/O |
| `plumbline_exec.py` | Main execution entrypoint for plumbline data |
| `dq_framework_exec.py` | Main framework execution |

## Logger Standardization

All steps are logged with a consistent format using modules like:
- `generate_log_starting_message`
- `generate_log_success_message`
- `generate_log_error_message`
- log file filename: dq_framework_execution.log


## Outputs
All outputs are located in `out/plumbline/YYYYMMDD_HHMISS/<module>` directory.
### Profiling
#### First Profiling component is the output of ydataProfling lib
- .html report
- .csv file
#### Second Profiling component is the year-month distribution
- generates .png file

### Example DQCheck Output

Sample output from a DQ Check CSV:
```
plumbline_id;year;read_mode;dq_dimension;metric;value
49352;2024;automatic;Completeness;days_with_multiple_records_abs;0.0
49352;2024;automatic;Completeness;days_with_multiple_records_prctg;0.0
49352;2024;automatic;Completeness;hours_with_multiple_records_abs;191.0
```
There are the correspondent visuals (.png)

### Example Threshold Validator Output

Sample output from a DQ Check CSV:
```
plumbline_id;year;read_mode;dq_dimension;metric;status;value;threshold;threshold_diff;threshold_deviation_pct
49352;2024;automatic;Completeness;hours_with_multiple_records_abs;ALERT;191.0;0.0;191.0;100.0
49352;2024;automatic;Completeness;hours_with_multiple_records_prctg;ALERT;0.03;0.0;0.03;3.0
49352;2024;automatic;Completeness;redundant_records_hours_abs;ALERT;252.0;0.0;252.0;100.0
```
There are the correspondent visuals (.png)


## Adding a new sensor
1 - Add the needed varaibles in `framework.py` configuration file
2 - Add the correspondent folders and scripts in `/src` folder, along with the 
sensor main script
3 - Add the correspondent DQChecks
4 - Add the correspondent Threshold Validator logic

Make sure that for 3) and $ you add the respective metrics and thresholds in `config/manual.json` file.

---

Data Science MSc - Master Thesis Project | ISCTE | Author: Diogo Fernandes 2025
