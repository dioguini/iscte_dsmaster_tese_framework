# Appendix Table of Contents

- [Appendix Table of Contents](#appendix-table-of-contents)
- [Appendix C - Configuration Files](#appendix-c---configuration-files)
  - [Framework Configurations File](#framework-configurations-file)
    - [Framework configuration file parameters](#framework-configuration-file-parameters)
    - [Framework full configuration file](#framework-full-configuration-file)
    - [Manual full configuration file](#manual-full-configuration-file)
    - [configuration of the manual.json configuration file](#configuration-of-the-manualjson-configuration-file)
  - [DQ Checks configuration](#dq-checks-configuration)
    - [Manual configurations for Completeness Data Quality Checks in automatic reading mode](#manual-configurations-for-completeness-data-quality-checks-in-automatic-reading-mode)
    - [Manual configurations for Completeness dimension DQ Checks](#manual-configurations-for-completeness-dimension-dq-checks)
    - [Manual configurations for Timeliness Data Quality Checks in automatic reading mode](#manual-configurations-for-timeliness-data-quality-checks-in-automatic-reading-mode)
    - [Manual configurations for Timeliness dimension DQ Checks](#manual-configurations-for-timeliness-dimension-dq-checks)
  - [Threshold Validator configurations](#threshold-validator-configurations)
    - [Manual configurations for Completeness Threshold Validator in automatic reading mode](#manual-configurations-for-completeness-threshold-validator-in-automatic-reading-mode)
    - [Manual configurations for Completeness Threshold Validator in manual reading mode](#manual-configurations-for-completeness-threshold-validator-in-manual-reading-mode)
    - [Manual configurations for Timeliness Threshold Validator in automatic reading mode](#manual-configurations-for-timeliness-threshold-validator-in-automatic-reading-mode)
    - [Manual configurations for Timeliness Threshold Validator in manual reading mode](#manual-configurations-for-timeliness-threshold-validator-in-manual-reading-mode)


# Appendix C - Configuration Files

## Framework Configurations File
### Framework configuration file parameters

| Variable Name                                      | Definition |
|:---------------------------------------------------| :--- |
| `ROOT_DIR`                                         | Root directory of the project |
| `SRC_DIR`                                          | Sources directory |
| `CONFIG_DIR`                                       | Directory where the configuration files must be placed |
| `ROOT_DATA_DIR`                                    | Root directory for data |
| `INPUT_DIR`                                        | Root directory for input data |
| `OUTPUT_DIR`                                       | Root directory for output data |
| `DQ_FRAMEWORK_INPUT_DIR`                           | Root input directory for the application layer |
| `DQ_FRAMEWORK_OUTPUT_DIR`                          | Root output directory for the application layer |
| `MANUAL_CONFIGS_FILENAME`                          | Name of the manual configuration file |
| `THRESHOLD_VALIDATOR_LABELS`                       | List of alert categories |
| `PLUMBLINE_INSTRUMENT_NAME`                        | Instrument name, defined in lowercase |
| `PLUMBLINE_INPUT_DATA_DIR`                         | Input directory for plumbline instrument data |
| `PLUMBLINE_MAIN_OUTPUT_DIR`                        | Root output directory for the plumbline instrument |
| `PLUMBLINE_TIMESTAMP_OUTPUT_DIR`                   | Output directory for plumbline instrument with execution timestamp |
| `PLUMBLINE_OUTPUT_PROFILING_DIR`                   | Output directory for profiling module of the plumbline instrument |
| `PLUMBLINE_OUTPUT_DQCHECK_DIR`                     | Output directory for DQ checks module of the plumbline instrument |
| `PLUMBLINE_OUTPUT_DQCHECK_VISUALS_DIR`             | Output directory for DQ check graphs for the plumbline instrument |
| `PLUMBLINE_OUTPUT_THRESHOLD_VALIDATOR_DIR`         | Output directory for threshold validator module for the plumbline instrument |
| `PLUMBLINE_OUTPUT_THRESHOLD_VALIDATOR_VISUALS_DIR` | Output directory for threshold validator graphs for the plumbline instrument |
| `PLUMBLINE_DISPLACEMENTS_OUTPUT_DIR`               | Output directory for displacements visuals |
| `PLUMBLINE_LOG_DIR`                                | Output directory for the log file of the plumbline instrument |
| `PLUMBLINE_RUN_MODES`                              | List of possible run modes |

### Framework full configuration file
```
"""
This script stores basic global variables values for the entire DQ framework.
It's not the main edit script.
All variables here should be declared in UPPER CASE.
"""
import os
import datetime

# Timestamp *unique per exec*
TIMESTAMP_FOLDER = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

THRESHOLD_VALIDATOR_LABELS = ["ALERT", "WARNING", "OK", "NO THRESHOLD"]

STATUS_COLOR_MAP = {
    "ALERT": "red",
    "WARNING": "orange",
    "OK": "green",
    "NO THRESHOLD": "gray"
}

##################################################################################################################################################################
# GENERAL FOR PROJECT
##################################################################################################################################################################
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")
CONFIG_DIR = os.path.join(ROOT_DIR, "configs")
ROOT_DATA_DIR = os.path.join(ROOT_DIR, "data")
INPUT_DIR = os.path.join(ROOT_DATA_DIR, "in")
OUTPUT_DIR = os.path.join(ROOT_DATA_DIR, "out")

##################################################################################################################################################################
# GENERAL FOR FRAMEWORK
##################################################################################################################################################################
DQ_FRAMEWORK_INPUT_DIR = os.path.join(INPUT_DIR, "dq_framework")
DQ_FRAMEWORK_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "dq_framework")
MANUAL_CONFIGS_FILENAME = os.path.join(CONFIG_DIR, "manual.json")
DQ_FRAMEWORK_LOG_FILENAME = "dq_framework_execution.log"

##################################################################################################################################################################
# FOR FRAMEWORK INSTRUMENTS
##################################################################################################################################################################
# Plumbline
PLUMBLINE_INSTRUMENT_NAME = "plumbline"
PLUMBLINE_INPUT_DATA_DIR = os.path.join(DQ_FRAMEWORK_INPUT_DIR, PLUMBLINE_INSTRUMENT_NAME)
PLUMBLINE_MAIN_OUTPUT_DIR = os.path.join(DQ_FRAMEWORK_OUTPUT_DIR, PLUMBLINE_INSTRUMENT_NAME)
PLUMBLINE_TIMESTAMP_OUTPUT_DIR = os.path.join(PLUMBLINE_MAIN_OUTPUT_DIR, TIMESTAMP_FOLDER)
PLUMBLINE_OUTPUT_PROFILING_DIR = os.path.join(PLUMBLINE_TIMESTAMP_OUTPUT_DIR, "profiling")
PLUMBLINE_OUTPUT_PROFILING_VISUALS_DIR = os.path.join(PLUMBLINE_TIMESTAMP_OUTPUT_DIR, "profiling_visuals")
PLUMBLINE_OUTPUT_DQCHECK_DIR = os.path.join(PLUMBLINE_TIMESTAMP_OUTPUT_DIR, "dqchecks")
PLUMBLINE_OUTPUT_DQCHECK_VISUALS_DIR = os.path.join(PLUMBLINE_TIMESTAMP_OUTPUT_DIR, "dqchecks_visuals")
PLUMBLINE_OUTPUT_THRESHOLD_VALIDATOR_DIR = os.path.join(PLUMBLINE_TIMESTAMP_OUTPUT_DIR, "threshold_validator")
PLUMBLINE_OUTPUT_THRESHOLD_VALIDATOR_VISUALS_DIR = os.path.join(PLUMBLINE_TIMESTAMP_OUTPUT_DIR, "threshold_validator_visuals")
PLUMBLINE_LOG_DIR = os.path.join(PLUMBLINE_TIMESTAMP_OUTPUT_DIR, "log")
PLUMBLINE_RUN_MODES = ["automatic", "manual"]
PLUMBLINE_DESCLOCS_OUTPUT_DIR = os.path.join(PLUMBLINE_TIMESTAMP_OUTPUT_DIR, "deslocs")
PLUMBLINE_DESCLOCS_OUTPUT_DIR = os.path.join(PLUMBLINE_TIMESTAMP_OUTPUT_DIR, "displacements_visuals")


# new instrument
# newInstrumentName_INSTRUMENT_NAME = "plumbline"
# newInstrumentName_INPUT_DATA_DIR = os.path.join(INPUT_DATA_DIR, PLUMBLINE_INSTRUMENT_NAME)
# newInstrumentName_MAIN_OUTPUT_DIR = os.path.join(OUTPUT_DIR, PLUMBLINE_INSTRUMENT_NAME)
# newInstrumentName_TIMESTAMP_OUTPUT_DIR = os.path.join(PLUMBLINE_MAIN_OUTPUT_DIR, TIMESTAMP_FOLDER)
# newInstrumentName_OUTPUT_PROFILING_DIR = os.path.join(PLUMBLINE_TIMESTAMP_OUTPUT_DIR, "profiling")
# newInstrumentName_OUTPUT_DQCHECK_DIR = os.path.join(PLUMBLINE_TIMESTAMP_OUTPUT_DIR, "dq_check_report")
# newInstrumentName_OUTPUT_DQCHECK_VISUALS_DIR = os.path.join(PLUMBLINE_TIMESTAMP_OUTPUT_DIR, "dq_check_report_visuals")
# newInstrumentName_OUTPUT_THRESHOLD_VALIDATOR_DIR = os.path.join(PLUMBLINE_TIMESTAMP_OUTPUT_DIR, "dq_threshold_validator")
# newInstrumentName_OUTPUT_THRESHOLD_VALIDATOR_VISUALS_DIR = os.path.join(PLUMBLINE_TIMESTAMP_OUTPUT_DIR, "dq_threshold_validator_visuals")
# newInstrumentName_LOG_DIR = os.path.join(PLUMBLINE_TIMESTAMP_OUTPUT_DIR, "log")

# list of available instruments
FRAMEWORK_AVAILABLE_INSTRUMENTS = [PLUMBLINE_INSTRUMENT_NAME]

```

### Manual full configuration file
| Parameter             | Definition |
|:----------------------| :--- |
| `plumbline`           | Main node under which all other variables will be nested. Each instrument should have its own tree. |
| `input_files_format`  | File extension of the input files for the instrument. |
| `profiling_columns`   | Columns list to be used in the Profiling step, for each of the reading modes. |
| `dq_checks`           | Main node for variables related to DQ checks. Each dimension should be nested under this node and contain its respective variables for each operation mode. |
| `threshold_validator` | Main node for variables related to threshold validators. Each dimension should be nested under this node and contain its respective variables for each operation mode. |


### configuration of the manual.json configuration file
```
{
    "plumbline": {
        "input_files_format": ".txt",
        "profiling_columns": {
            "automatic": [
                "ANO",
                "MES",
                "DIA",
                "HORA",
                "MINUTO",
                "DESLOCRADIALABS",
                "DESLOCTANGABS"
            ],
            "manual": [
                "ANO",
                "MES",
                "DIA",
                "HORA",
                "MINUTO",
                "DESLOCRADIALABS",
                "DESLOCTANGABS"
            ]
        },
        "dq_checks": {
            "Completeness": {
                "automatic": {
                    "max_allowed_records_per_day": 24,
                    "max_allowed_records_per_hour": 1,
                    "max_allowed_records_per_minute": 1,
                    "max_days_missing_data": 0,
                    "max_hours_missing_data": 0,
                    "max_minutes_missing_data": 0
                },
                "manual": {
                    "max_allowed_records_per_day": 1,
                    "max_allowed_records_per_hour": 1,
                    "max_allowed_records_per_minute": 1,
                    "max_days_missing_data": 14,
                    "max_hours_missing_data": 0,
                    "max_minutes_missing_data": 0
                }
            },
            "Timeliness": {
                "automatic": {
                    "max_interval_days": 0,
                    "max_interval_hours": 1,
                    "max_interval_minutes": 60
                },
                "manual": {
                    "max_interval_days": 14,
                    "max_interval_hours": 0,
                    "max_interval_minutes": 0
                }
            }
        },
        "threshold_validator": {
            "Completeness": {
                "automatic": {
                    "limit_factor": 1.05,
                    "days_with_multiple_records_abs": 0,
                    "days_with_multiple_records_prctg": 0,
                    "hours_with_multiple_records_abs": 0,
                    "hours_with_multiple_records_prctg": 0,
                    "minutes_with_multiple_records_abs": 0,
                    "minutes_with_multiple_records_prctg": 0,
                    "missing_data_day_abs": 0,
                    "missing_data_day_prctg": 0,
                    "missing_data_hour_abs": 0,
                    "missing_data_hour_prctg": 0,
                    "missing_data_minute_abs": 0,
                    "missing_data_minute_prctg": 0,
                    "missing_DESLOCRADIALABS_abs": 0,
                    "missing_DESLOCRADIALABS_prctg": 0,
                    "missing_DESLOCTANGABS_abs": 0,
                    "missing_DESLOCTANGABS_prctg": 0,
                    "redundant_records_day_abs": 0,
                    "redundant_records_hours_abs": 0,
                    "redundant_records_minutes_abs": 0
                },
                "manual": {
                    "limit_factor": 1.05,
                    "days_with_multiple_records_abs": 0,
                    "days_with_multiple_records_prctg": 0,
                    "missing_data_day_abs": 0,
                    "missing_data_day_prctg": 0,
                    "missing_data_hour_abs": 0,
                    "missing_data_hour_prctg": 0,
                    "missing_data_minute_abs": 0,
                    "missing_data_minute_prctg": 0,
                    "missing_DESLOCRADIALABS_abs": 0,
                    "missing_DESLOCRADIALABS_prctg": 0,
                    "missing_DESLOCTANGABS_abs": 0,
                    "missing_DESLOCTANGABS_prctg": 0,
                    "redundant_records_day_abs": 0,
                    "redundant_records_hours_abs": 0,
                    "redundant_records_minutes_abs": 0
                }
            },
            "Timeliness": {
                "automatic": {
                    "limit_factor": 1.05,
                    "data_day_density_abs": 24,
                    "data_hour_density_abs": 1,
                    "data_minute_density_abs": 1,
                    "days_apart_previous_record_count_abs": 1,
                    "days_apart_previous_record_proportion_prctg": 0,
                    "hours_apart_previous_record_count_abs": 1,
                    "hours_apart_previous_record_proportion_prctg": 0,
                    "interval_days_abs": 1,
                    "interval_days_prctg": 0,
                    "interval_hours_abs": 1,
                    "interval_hours_prctg": 0,
                    "interval_minutes_abs": 60,
                    "interval_minutes_prctg": 0,
                    "max_gap_days_abs": 0,
                    "max_gap_hours_abs": 0,
                    "max_gap_minutes_abs": 0,
                    "minutes_apart_previous_record_count_abs": 0,
                    "minutes_apart_previous_record_proportion_prctg": 0
                },
                "manual": {
                    "limit_factor": 1.05,
                    "data_day_density_abs": 0.07,
                    "days_apart_previous_record_count_abs": 1,
                    "days_apart_previous_record_proportion_prctg": 0,
                    "interval_days_abs": 14,
                    "interval_days_prctg": 0,
                    "max_gap_days_abs": 0
                }
            }
        }
    }
}


```


## DQ Checks configuration
### Manual configurations for Completeness Data Quality Checks in automatic reading mode
| Variable                         | Description | Value |
|:---------------------------------| :--- | :--- |
| `max_allowed_records_per_day`    | Maximum number of records expected per day | 24 |
| `max_allowed_records_per_hour`   | Maximum number of records expected per hour | 1 |
| `max_allowed_records_per_minute` | Maximum number of records expected per minute | 1 |
| `max_days_missing_data`          | Maximum number of days allowed with missing data | 0 |
| `max_hours_missing_data`         | Maximum number of hours allowed with missing data | 0 |
| `max_minutes_missing_data`       | Maximum number of minutes allowed with missing data | 0 |

### Manual configurations for Completeness dimension DQ Checks
| Variable                         | Description | Value |
|:---------------------------------| :--- | :--- |
| `max_allowed_records_per_day`    | Maximum number of records expected per day | 1 |
| `max_allowed_records_per_hour`   | Maximum number of records expected per hour | 1 |
| `max_allowed_records_per_minute` | Maximum number of records expected per minute | 1 |
| `max_days_missing_data`          | Maximum number of days allowed with missing data | 14 |
| `max_hours_missing_data`         | Maximum number of hours allowed with missing data | 0 |
| `max_minutes_missing_data`       | Maximum number of minutes allowed with missing data | 0 |


### Manual configurations for Timeliness Data Quality Checks in automatic reading mode
| Variable               | Description | Value |
|:-----------------------| :--- | :--- |
| `max_interval_days`    | Maximum acceptable interval in days between two consecutive records | 0 |
| `max_interval_hours`   | Maximum acceptable interval in hours between two consecutive records | 1 |
| `max_interval_minutes` | Maximum acceptable interval in minutes between two consecutive records | 60 |

### Manual configurations for Timeliness dimension DQ Checks
| Variable              | Description | Value |
|:----------------------| :--- | :--- |
| `max_interval_days`    | Maximum acceptable interval in days between two consecutive records | 14 |
| `max_interval_hours`   | Maximum acceptable interval in hours between two consecutive records | 0 |
| `max_interval_minutes` | Maximum acceptable interval in minutes between two consecutive records | 0 |


## Threshold Validator configurations

### Manual configurations for Completeness Threshold Validator in automatic reading mode
| DQ Check                              | Description | Value |
|:--------------------------------------| :--- | :--- |
| `limit_factor`                        | Tolerance multiplier for classifying WARNING vs ALERT | 1 |
| `missing_DESLOCRADIALABS_prctg`       | Percentage of missing values in the DESLOCRADIALABS field | 0 |
| `missing_DESLOCRADIALABS_abs`         | Absolute number of missing values in the DESLOCRADIALABS field | 0 |
| `missing_DESLOCTANGABS_prctg`         | Percentage of missing values in the DESLOCTANGABS field | 0 |
| `missing_DESLOCTANGABS_abs`           | Absolute number of missing values in the DESLOCTANGABS field | 0 |
| `missing_data_day_prctg`              | Percentage of days with missing data | 0 |
| `missing_data_day_abs`                | Number of days with missing data | 0 |
| `missing_data_hour_prctg`             | Percentage of hours with missing data | 0 |
| `missing_data_hour_abs`               | Number of hours with missing data | 0 |
| `missing_data_minute_prctg`           | Percentage of minutes with missing data | 0 |
| `missing_data_minute_abs`             | Absolute number of minutes with missing data | 0 |
| `ngaps_data_day_abs`                  | Number of gaps (interruptions) per day | 0 |
| `ngaps_data_hour_abs`                 | Number of gaps per hour | 0 |
| `ngaps_data_minute_abs`               | Number of gaps per minute | 0 |
| `days_with_multiple_records_abs`      | Absolute number of days with multiple (redundant) records | 0 |
| `days_with_multiple_records_prctg`    | Percentage of days with multiple records | 0 |
| `hours_with_multiple_records_abs`     | Absolute number of hours with multiple records | 0 |
| `hours_with_multiple_records_prctg`   | Percentage of hours with multiple records | 0 |
| `minutes_with_multiple_records_abs`   | Absolute number of minutes with multiple records | 0 |
| `minutes_with_multiple_records_prctg` | Percentage of minutes with multiple records | 0 |
| `data_day_density_abs`                | Expected record density per day | 1 |
| `data_hour_density_abs`               | Expected record density per hour | 1 |
| `data_minute_density_abs`             | Expected record density per minute | 1 |
| `redundant_records_day_abs`           | Number of redundant records per day | 0 |
| `redundant_records_hours_abs`         | Number of redundant records per hour | 0 |
| `redundant_records_minutes_abs`       | Number of redundant records per minute | 0 |

### Manual configurations for Completeness Threshold Validator in manual reading mode
| DQ Check                              | Description | Value |
|:--------------------------------------| :--- | :--- |
| `limit_factor`                        | Tolerance multiplier for classifying WARNING vs ALERT | 1 |
| `missing_DESLOCRADIALABS_prctg`       | Percentage of missing values in the DESLOCRADIALABS field | 0 |
| `missing_DESLOCRADIALABS_abs`         | Absolute number of missing values in the DESLOCRADIALABS field | 0 |
| `missing_DESLOCTANGABS_prctg`         | Percentage of missing values in the DESLOCTANGABS field | 0 |
| `missing_DESLOCTANGABS_abs`           | Absolute number of missing values in the DESLOCTANGABS field | 0 |
| `missing_data_day_prctg`              | Percentage of days with missing data | 0 |
| `missing_data_day_abs`                | Number of days with missing data | 0 |
| `missing_data_hour_prctg`             | Percentage of hours with missing data | 0 |
| `missing_data_hour_abs`               | Number of hours with missing data | 0 |
| `missing_data_minute_prctg`           | Percentage of minutes with missing data | 0 |
| `missing_data_minute_abs`             | Absolute number of minutes with missing data | 0 |
| `ngaps_data_day_abs`                  | Number of gaps (interruptions) per day | 0 |
| `ngaps_data_hour_abs`                 | Number of gaps per hour | 0 |
| `ngaps_data_minute_abs`               | Number of gaps per minute | 0 |
| `days_with_multiple_records_abs`      | Absolute number of days with multiple (redundant) records | 0 |
| `days_with_multiple_records_prctg`    | Percentage of days with multiple records | 0 |
| `hours_with_multiple_records_abs`     | Absolute number of hours with multiple records | 0 |
| `hours_with_multiple_records_prctg`   | Percentage of hours with multiple records | 0 |
| `minutes_with_multiple_records_abs`   | Absolute number of minutes with multiple records | 0 |
| `minutes_with_multiple_records_prctg` | Percentage of minutes with multiple records | 0 |
| `data_day_density_abs`                | Expected record density per day | 1 |
| `data_hour_density_abs`               | Expected record density per hour | 1 |
| `data_minute_density_abs`             | Expected record density per minute | 1 |
| `redundant_records_day_abs`           | Number of redundant records per day | 0 |
| `redundant_records_hours_abs`         | Number of redundant records per hour | 0 |
| `redundant_records_minutes_abs`       | Number of redundant records per minute | 0 |

### Manual configurations for Timeliness Threshold Validator in automatic reading mode
| DQ Check                                         | Description | Value |
|:-------------------------------------------------| :--- | :--- |
| `limit_factor`                                   | Tolerance multiplier for classifying WARNING vs ALERT | 1 |
| `interval_days_prctg`                            | Percentage deviation from expected day interval | 1 |
| `interval_days_abs`                              | Average interval in days between records | 1 |
| `interval_hours_prctg`                           | Percentage deviation from expected hour interval | 1 |
| `interval_hours_abs`                             | Average interval in hours between records | 1 |
| `interval_minutes_prctg`                         | Percentage deviation from expected minute interval | 1 |
| `interval_minutes_abs`                           | Average interval in minutes between records | 1 |
| `days_apart_previous_record_proportion_prctg`    | Proportion of gap between current and previous record (days) | 1 |
| `max_gap_days_abs`                               | Maximum number of consecutive days without records | 0 |
| `days_apart_previous_record_count_abs`           | Number of days between the current and previous record | 1 |
| `hours_apart_previous_record_proportion_prctg`   | Proportion of gap between current and previous record (hours) | 0 |
| `max_gap_hours_abs`                              | Maximum number of consecutive hours without records | 0 |
| `hours_apart_previous_record_count_abs`          | Number of hours between the current and previous record | 1 |
| `minutes_apart_previous_record_proportion_prctg` | Proportion of gap between current and previous record (minutes) | 0 |
| `max_gap_minutes_abs`                            | Maximum number of consecutive minutes without records | 0 |
| `minutes_apart_previous_record_count_abs`        | Number of minutes between the current and previous record | 0 |

### Manual configurations for Timeliness Threshold Validator in manual reading mode
| DQ Check                                         | Description | Value |
|:-------------------------------------------------| :--- | :--- |
| `limit_factor`                                   | Tolerance multiplier for classifying WARNING vs ALERT | 1 |
| `interval_days_prctg`                            | Percentage deviation from expected day interval | 1 |
| `interval_days_abs`                              | Average interval in days between records | 1 |
| `interval_hours_prctg`                           | Percentage deviation from expected hour interval | 1 |
| `interval_hours_abs`                             | Average interval in hours between records | 1 |
| `interval_minutes_prctg`                         | Percentage deviation from expected minute interval | 1 |
| `interval_minutes_abs`                           | Average interval in minutes between records | 1 |
| `days_apart_previous_record_proportion_prctg`    | Proportion of gap between current and previous record (days) | 1 |
| `max_gap_days_abs`                               | Maximum number of consecutive days without records | 0 |
| `days_apart_previous_record_count_abs`           | Number of days between the current and previous record | 1 |
| `hours_apart_previous_record_proportion_prctg`   | Proportion of gap between current and previous record (hours) | 0 |
| `max_gap_hours_abs`                              | Maximum number of consecutive hours without records | 0 |
| `hours_apart_previous_record_count_abs`          | Number of hours between the current and previous record | 1 |
| `minutes_apart_previous_record_proportion_prctg` | Proportion of gap between current and previous record (minutes) | 0 |
| `max_gap_minutes_abs`                            | Maximum number of consecutive minutes without records | 0 |
| `minutes_apart_previous_record_count_abs`        | Number of minutes between the current and previous record | 0 |