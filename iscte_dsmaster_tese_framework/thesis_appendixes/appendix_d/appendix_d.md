# Appendix Table of Contents

- [Appendix Table of Contents](#appendix-table-of-contents)
- [Appendix D - Application Layer](#appendix-d---application-layer)
  - [Execution parameters](#execution-parameters)
  - [Profiling](#profiling)
    - [File Naming Conventions for Year-Month Profiling module output](#file-naming-conventions-for-year-month-profiling-module-output)
    - [File Naming Conventions for ydata-Profiling output module outputs](#file-naming-conventions-for-ydata-profiling-output-module-outputs)
    - [Csv report header output description](#csv-report-header-output-description)
  - [DQ Checks](#dq-checks)
    - [File Naming Conventions for DQ Checks module output](#file-naming-conventions-for-dq-checks-module-output)
    - [Csv output file header file output from Data Quality Checks module](#csv-output-file-header-file-output-from-data-quality-checks-module)
  - [Threshold Validator](#threshold-validator)
    - [File Naming Conventions for Threshold Validator module output](#file-naming-conventions-for-threshold-validator-module-output)
    - [Csv output file header file output from Threshold Validator module](#csv-output-file-header-file-output-from-threshold-validator-module)
  - [Reporting](#reporting)
    - [File naming conventions for Reporting module outputs](#file-naming-conventions-for-reporting-module-outputs)
  - [Feedback Layer](#feedback-layer)
    - [Detailed DQ  Checks file naming convention produced for Feedback Layer](#detailed-dq--checks-file-naming-convention-produced-for-feedback-layer)


# Appendix D - Application Layer

## Execution parameters
Available arguments and respective possible inputs to execute the Application Layer via command line

| Argument | Description | Example |
| :--- | :--- | :--- |
| instrument | Defines the instrument to be processed (e.g., plumbline) | plumbline |
| mode | Indicates the type of readings to be evaluated (automatic or manual). When “all” is used, both automatic and manual will be processed. | manual / automatic / all |
| id_list | Specifies the list of sensor IDs to be analysed. When “all” is used, all sensors will be processed. | 00000 / 0000 00001 / all |
| year_list | Specifies the list of years to be considered, avoiding full processing of the entire dataset. When “all” is used, all years will be processed. | 2024 / 2023 2024 / all |

## Profiling
### File Naming Conventions for Year-Month Profiling module output
| File Type | Description | Naming Pattern | Example |
| :--- | :--- | :--- | :--- |
| .csv | Year-month-level profiling summary | ProfilingSummaryYearMonth_<READ_MODE>_<YEAR>_<SENSOR_ID>.csv | ProfilingSummaryYearMonth_automatic_2024_00000.csv |
| .png | Year-month-level profiling visualisation | ProfilingSummaryYearMonth_<READ_MODE>_<YEAR>_<SENSOR_ID>.png | ProfilingSummaryYearMonth_automatic_2024_00000.png |


### File Naming Conventions for ydata-Profiling output module outputs
| File Type | Description | Naming Pattern | Example |
| :--- | :--- | :--- | :--- |
| .csv | Summary of profiling metrics | ProfilingSummary_<READ_MODE>_<YEAR>_<SENSOR_ID>.csv | ProfilingSummary_automatic_2024_00000.csv |
| .html | Interactive profiling report | ProfilingSummaryReport_<READ_MODE>_<YEAR>_<SENSOR_ID>.html | ProfilingSummaryReport_automatic_2024_00000.html |


### Csv report header output description
| Field | Description |
| :--- | :--- |
| PLUMBLINE_ID | Plumb line sensor ID |
| READ_MODE | Reading mode |
| YEAR_MONTH_STR | Year and month of the record (string format) |
| DATA_MONTH | First day of the month (date format). Useful for sorting the records |
| TOTAL_RECORDS | Total number of records |


## DQ Checks
### File Naming Conventions for DQ Checks module output
| File Type | Description | Naming Pattern | Example |
| :--- | :--- | :--- | :--- |
| .csv | Summary of all the DQ Checks executed | DQCheck_<DQ_DIMENSION>_<READ_MODE>_<YEAR>_<SENSOR_ID>.csv | DQCheck_Completeness_automatic_2024_00000.csv |

### Csv output file header file output from Data Quality Checks module
| Field | Description |
| :--- | :--- |
| plumbline_id | Plumb line sensor ID |
| read_mode | Reading mode |
| year | Year of the record |
| dq_dimension | Data Quality dimension |
| check | Name of the calculated DQ Check |
| value | Observed value for the respective DQ Check |

## Threshold Validator
### File Naming Conventions for Threshold Validator module output
| File Type | Description | Naming Pattern | Example |
| :--- | :--- | :--- | :--- |
| .csv | Summary of all the Threshold Validator executed | ThresholdValidator_<DQ_DIMENSION>_<READ_MODE>_<YEAR>_<SENSOR_ID>.csv | ThresholdValidator_Completeness_automatic_2024_00000.csv |

### Csv output file header file output from Threshold Validator module
| Parameter | Definition |
| :--- | :--- |
| plumbline_id | Plumb line sensor ID |
| read_mode | Reading mode |
| year | Year of the record |
| dq_dimension | Data Quality dimension evaluated |
| check | Evaluated DQ Check |
| status | Alert classification (e.g. OK, ALERT) |
| value | Total evidence or observed value |



## Reporting
### File naming conventions for Reporting module outputs
| File Type | Description | Folder | Naming Pattern | Example |
| :--- | :--- | :--- | :--- | :--- |
| .png | Summary of all the DQ Checks executed (for Absolute type metrics). Horizontal bar chart type. | dq_checks_visuals | DQCheck_<DQ_DIMENSION>_<READ_MODE>_<PLUMBLINE_ID>_AbsoluteMetrics.png | DQCheck_Completeness_automatic_2024_00000_AbsoluteMetrics.png |
| .png | Summary of all the DQ Checks executed (for Percentage type metrics). Horizontal bar chart type. | dq_checks_visuals | DQCheck_<DQ_DIMENSION>_<READ_MODE>_<PLUMBLINE_ID>_PercentageMetrics.png | DQCheck_Completeness_automatic_2024_00000_PercentageMetrics.png |
| .png | Summary of all the Alerts identified. Vertical bar chart type metrics list detailed by Alert Type (for Absolute type metrics). | threshold_validator_checks_visuals | ThresholdValidator_<DQ_DIMENSION>_<READ_MODE>_<PLUMBLINE_ID>_AbsoluteMetrics.png | ThresholdValidator_Completeness_automatic_2023_00000_AbsoluteMetrics.png |
| .png | Summary of all the Alerts identified. Vertical bar chart type metrics list detailed by Alert Type (for Percentage type metrics). | threshold_validator_checks_visuals | ThresholdValidator_<DQ_DIMENSION>_<READ_MODE>_<PLUMBLINE_ID>_PercentageMetrics.png | ThresholdValidator_Completeness_automatic_2023_00000_PercentageMetrics.png |
| .png | Monthly Average Radial displacements, combined with Monthly Radial Absolute displacements. Violin chart type. | displacements_visuals | MonthlyRadialAvg_<READ_MODE>_<YEAR>_<SENSOR_ID>.png | MonthlyRadialAvg_automatic_2024_00000.png |
| .png | Monthly Average Tangential displacements, combined with Monthly Tangential Absolute displacements. Violin chart type. | displacements_visuals | MonthlyTangentialAvg_<READ_MODE>_<YEAR>_<SENSOR_ID>.png | MonthlyTangentialAvg_automatic_2024_00000.png |

## Feedback Layer
### Detailed DQ  Checks file naming convention produced for Feedback Layer
| File Type | Detailed level | Description | Naming Pattern | Example |
| :--- | :--- | :--- | :--- | :--- |
| .csv | Detailed | Detailed report for the different DQ Checks evaluated | Obervability_<DQ_DIMENSION_READ_MODE_<YEAR>_<SENSOR_ID>_<DQ_CHECK>.csv | Observability_Completeness_automatic_2024_0000_hours_with_multiple_records_abs.csv |
| .csv | Aggregated | Aggregated report for the different DQ Checks evaluated | ObervabilityAgg_<DQ_DIMENSION_READ_MODE_<YEAR>_<SENSOR_ID>_<DQ_CHECK>.csv | ObservabilityAgg_Completeness_automatic_2024_00000_hours_with_multiple_records_abs.csv |