"""
Plubmbline script
"""
import re
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from utils.dq_utils import setup_logger
# CONFIG inputs imports
from configs.framework import DQ_FRAMEWORK_AVAILABLE_DIMENSION, PLUMBLINE_INSTRUMENT_NAME, PLUMBLINE_OUTPUT_DQCHECK_DIR, PLUMBLINE_OUTPUT_THRESHOLD_VALIDATOR_DIR, \
PLUMBLINE_OUTPUT_THRESHOLD_VALIDATOR_VISUALS_DIR, PLUMBLINE_OUTPUT_DQCHECK_VISUALS_DIR, PLUMBLINE_INPUT_DATA_DIR, \
PLUMBLINE_RUN_MODES, PLUMBLINE_OUTPUT_PROFILING_DIR, PLUMBLINE_OUTPUT_PROFILING_VISUALS_DIR, PLUMBLINE_DISPLACEMENTS_OUTPUT_DIR
from src.dq_framework.plumbline.profiling.data_profiler import generate_profiling_html_report, generate_year_month_distribution, generate_year_distribution, generate_profiling_csv_report
from src.dq_framework.plumbline.dq_checks.dq_checks import *
from src.dq_framework.plumbline.threshold_validator.dq_threshold_validator import *
from src.dq_framework.utils.dq_utils import *
from src.dq_framework.plumbline.visuals.dq_checks.dq_checks_visuals import *
from src.dq_framework.plumbline.visuals.threshold_validator.dq_threshold_validator_visuals import *
from src.dq_framework.plumbline.visuals.displacements.displacements_visuals import *


def run_application_layer(in_plumbline_id: str, in_sensor_data_df: pd.DataFrame, in_read_mode) -> None:
    """
    Executes the application logic for a single plumbline sensor file, applying all defined Data Quality checks
    and generating profiling, metric, threshold, and displacement outputs.

    This function orchestrates the complete evaluation pipeline for a given plumbline sensor file:
    1. Loads instrument-specific configuration settings.
    2. Generates profiling reports (yearly and monthly distributions + HTML summary).
    3. Applies Data Quality checks (Timeliness and Completeness) based on read mode.
    4. Validates each metric against dimension-specific thresholds.
    5. Saves all metrics and threshold validation outputs to CSV.
    6. Generates corresponding visualizations (DQ checks, threshold status, and displacements).

    Args:
        in_plumbline_id (str): Unique identifier of the plumbline sensor (e.appendix_g., '49350').
        in_sensor_data_df (pd.DataFrame): Preprocessed DataFrame containing the sensor's data.
        in_read_mode (str): Reading mode of the file ('manual' or 'automatic').

    Returns:
        None. All outputs (CSV and plots) are stored in their respective configured directories.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)

    instrument_configs = load_manual_config_file(PLUMBLINE_INSTRUMENT_NAME)

    all_years = in_sensor_data_df["ANO"].unique()

    for year in all_years:
        dados_ano = in_sensor_data_df[in_sensor_data_df["ANO"] == year]
        logger_message = "Running Data Profiler (Year & Year-Month Distribution & Profiler"
        logger.info(format_date_logger() + f"\n\n***{logger_message}\t\t***")
        generate_year_distribution(dados_ano, PLUMBLINE_OUTPUT_PROFILING_DIR, PLUMBLINE_OUTPUT_PROFILING_VISUALS_DIR, in_plumbline_id, in_read_mode, year)
        generate_year_month_distribution(dados_ano, PLUMBLINE_OUTPUT_PROFILING_DIR, PLUMBLINE_OUTPUT_PROFILING_VISUALS_DIR, in_plumbline_id, in_read_mode, year)
        generate_profiling_html_report(dados_ano, instrument_configs, PLUMBLINE_OUTPUT_PROFILING_VISUALS_DIR, in_plumbline_id, in_read_mode, year)
        generate_profiling_csv_report(dados_ano, instrument_configs, PLUMBLINE_OUTPUT_PROFILING_DIR, in_plumbline_id, in_read_mode, year)


        for dq_dimension in DQ_FRAMEWORK_AVAILABLE_DIMENSION:
            logger_message = "DQ Dimensions Evaluation"
            logger.info(format_date_logger() + f"\n\n***{logger_message}\t\t***")
            if in_read_mode == "automatic" :
                if dq_dimension == "Completeness":
                    dqchecks_output_dict = check_completeness_automatic(dados_ano, dq_dimension, instrument_configs, in_plumbline_id, year)
                elif dq_dimension == "Timeliness":
                    dqchecks_output_dict = check_timeliness_automatic(dados_ano, dq_dimension, instrument_configs, in_plumbline_id, year)
            elif in_read_mode == "manual" :
                if dq_dimension == "Completeness":
                    dqchecks_output_dict = check_completeness_manual(dados_ano, dq_dimension, instrument_configs, in_plumbline_id, year)
                elif dq_dimension == "Timeliness":
                    dqchecks_output_dict = check_timeliness_manual(dados_ano, dq_dimension, instrument_configs, in_plumbline_id, year)
            else:
                logger.info(format_date_logger() + f"\n\n***\tERROR UNKNOWN DQ Dimensions. System Exit.\t***")
                sys.exit(1)

            logger_message = "Writing DQ CHECKS Outputs to .csv files"
            logger.info(format_date_logger() + f"\n\n***{logger_message}\t\t***")
            save_dqchecks_results_to_csv(dqchecks_output_dict, dq_dimension, PLUMBLINE_OUTPUT_DQCHECK_DIR, in_plumbline_id, in_read_mode, year)

            dq_checks_abs_dict = {k: v for k, v in dqchecks_output_dict.items() if k.endswith("_abs")}
            dq_checks_prctg_dict = {k: v for k, v in dqchecks_output_dict.items() if k.endswith("_prctg")}

            logger.info(format_date_logger() + f"\n\n***\tGenerating DQ Checks Plots - for individual sensor(s) file(s)\t***")
            generate_dqcheck_absolute_metrics_plot(dq_checks_abs_dict, in_plumbline_id, PLUMBLINE_OUTPUT_DQCHECK_VISUALS_DIR, in_read_mode, year, dq_dimension)
            generate_dqcheck_percentage_metrics_plot(dq_checks_prctg_dict, in_plumbline_id, PLUMBLINE_OUTPUT_DQCHECK_VISUALS_DIR, in_read_mode, year, dq_dimension)

            logger_message = "Threshold Evaluation Evaluation"
            logger.info(format_date_logger() + f"\n\n***{logger_message}\t\t***")

            if in_read_mode == "automatic" :
                dimension_threshold_validator_results = validate_thresholds_automatic(dqchecks_output_dict, dq_dimension, instrument_configs)
            elif in_read_mode == "manual" :
                dimension_threshold_validator_results = validate_thresholds_manual(dqchecks_output_dict, dq_dimension, instrument_configs)
            else:
                logger_message = "ERROR UNKNOWN DQ Dimensions. System Exit."
                logger.error(format_date_logger() + f"\n\n***{logger_message}\t\t***")
                sys.exit(1)

            logger_message = "Writing Threshold Validator Outputs to .csv files"
            logger.info(format_date_logger() + f"\n\n***{logger_message}\t\t***")
            save_thresholdvalidator_results_to_csv(dimension_threshold_validator_results, dq_dimension, in_plumbline_id, PLUMBLINE_OUTPUT_THRESHOLD_VALIDATOR_DIR, in_read_mode, year)

            logger_message = "Generating Threshold Validator Plots - for individual sensor(s) file(s)"
            logger.info(format_date_logger() + f"\n\n***{logger_message}\t\t***")
            threshold_validator_abs_dict =  { metric: values for metric, values in dimension_threshold_validator_results.items() if metric.endswith("_abs")}
            threshold_validator_prctg_dict = { metric: values for metric, values in dimension_threshold_validator_results.items() if metric.endswith("_prctg")}

            generate_threshold_validator_absolute_metrics_plot(threshold_validator_abs_dict, in_plumbline_id, PLUMBLINE_OUTPUT_THRESHOLD_VALIDATOR_VISUALS_DIR, in_read_mode, year, dq_dimension)
            generate_threshold_validator_percentage_metrics_plot(threshold_validator_prctg_dict, in_plumbline_id, PLUMBLINE_OUTPUT_THRESHOLD_VALIDATOR_VISUALS_DIR, in_read_mode, year, dq_dimension)

            logger_message = "Generating Radial and Tangential Displacements"
            logger.info(format_date_logger() + f"\n\n***{logger_message}\t\t***")
            plot_monthly_radial_average_displacement(dados_ano, PLUMBLINE_DISPLACEMENTS_OUTPUT_DIR, in_plumbline_id, in_read_mode, year)
            plot_monthly_tangential_average_displacement(dados_ano, PLUMBLINE_DISPLACEMENTS_OUTPUT_DIR, in_plumbline_id, in_read_mode, year)

def process_individual_file(in_sensor_data_file: str, in_read_mode:str, in_year_list:list) -> None:
    """
    Loads, preprocesses, and applies the Data Quality Framework to an individual plumbline sensor file.

    The function reads a tab-separated text file, constructs time-based features,
    filters by year if applicable, cleans unused columns, and prepares the data for full DQ analysis.
    It then calls `run_application_layer()` to apply the complete processing pipeline.

    Args:
        in_sensor_data_file (str): Filename of the plumbline sensor data file (e.appendix_g., '49350.txt').
        in_read_mode (str): Reading mode ('manual' or 'automatic').
        in_year_list (list): List of years to filter the dataset. Use ['all'] to skip filtering.

    Returns:
        None. Logs and output files are generated for each step (profiling, DQ checks, thresholds, plots).
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"PLUMBLINE"
    logger_module_info = f"PLUMBLINE INDIVIDUAL FILE PROCESSING"

    logger_message = f"PROCESSING {in_sensor_data_file} file for {in_read_mode} reading mode"
    logger_starter_message = f"\n\n\t##########\t\t{logger_message}\t\t##########\t\n"
    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        sensor_data_df = pd.read_csv( os.path.join(PLUMBLINE_INPUT_DATA_DIR, in_sensor_data_file), sep='\t')
        if in_year_list != ["all"]:
            year_list_int = [int(y) for y in in_year_list]
            sensor_data_df = sensor_data_df[sensor_data_df["ANO"].isin(year_list_int)]

        columns_to_remove = ["ESTADODESLOCRADIALABS", "ESTADODESLOCTANGABS"]

        for column in columns_to_remove:
            if column in sensor_data_df.columns:
                sensor_data_df.drop(column, axis=1, inplace=True)

        month_map_str = {
            "01": "January", "02": "February", "03": "March", "04": "April",
            "05": "May", "06": "June", "07": "July", "08": "August",
            "09": "September", "10": "October", "11": "November", "12": "December"
        }

        sensor_data_df["ANO_STR"] = sensor_data_df["ANO"].astype(str)
        sensor_data_df["MES_STR"] = sensor_data_df["MES"].astype(str).str.zfill(2)
        sensor_data_df["MONTH_NAME_EN"] = sensor_data_df["MES_STR"].map(month_map_str)
        sensor_data_df["YEAR_MONTH_STR"] = sensor_data_df["ANO_STR"].str.cat(sensor_data_df["MONTH_NAME_EN"], sep="_")
        sensor_data_df["DATA_MONTH"] = pd.to_datetime({"year": sensor_data_df["ANO"], "month": sensor_data_df["MES"], "day": 1})
        sensor_data_df["DATA_DAY"] = pd.to_datetime(dict(year=sensor_data_df["ANO"], month=sensor_data_df["MES"], day=sensor_data_df["DIA"]))
        sensor_data_df["DATA_HOUR"] = pd.to_datetime(dict(year=sensor_data_df["ANO"], month=sensor_data_df["MES"], day=sensor_data_df["DIA"], hour=sensor_data_df["HORA"]))
        sensor_data_df["DATA_MINUTE"] = pd.to_datetime(dict(year=sensor_data_df["ANO"], month=sensor_data_df["MES"], day=sensor_data_df["DIA"], hour=sensor_data_df["HORA"], minute=sensor_data_df["MINUTO"]))
        sensor_data_df = sensor_data_df.sort_values("DATA_MINUTE")
        match = re.search(r"(\d+)(?=\.txt$)", in_sensor_data_file)
        plumbline_id = match.group(1) if match else None
        print(plumbline_id)
        plumbline_id = "00000" if plumbline_id == "49352" else plumbline_id

        run_application_layer(plumbline_id, sensor_data_df, in_read_mode)
    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)


def run_plumbline(in_read_mode:str, in_id_list:list, in_year_list):
    """
    Orchestrates the execution of the Data Quality Framework for multiple plumbline sensor files.

    This is the main execution function for plumbline instrumentation. It validates the environment, selects
    the appropriate files according to user input (read mode, ID list, year list), and runs the DQ pipeline
    on each selected file. It supports 'manual', 'automatic', and 'all' modes, and handles error cases explicitly.

    Args:
        in_read_mode (str): Reading mode ('manual', 'automatic', or 'all').
        in_id_list (list): List of sensor file IDs to be processed. Use ['all'] to include all available files.
        in_year_list (list): List of years to be processed. Use ['all'] to include all available years.

    Workflow:
        - Validates input/output/log directory structure.
        - Loads configuration and fetches available input files.
        - Filters files by ID and read mode.
        - Processes each file individually using `process_individual_file()`.
        - Logs all stages of execution.
        - Generates summary visual outputs.

    Returns:
        None. Executes the DQ pipeline and stores all relevant logs, reports, and visualizations.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"PLUMBLINE EXEC"
    logger_module_info = f"DQ CHECKS - SAVE .CSV"
    logger_starter_message = f"Starting DQ Framework"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        welcome_function()

        validate_directory_structure([PLUMBLINE_INPUT_DATA_DIR, PLUMBLINE_OUTPUT_PROFILING_DIR, PLUMBLINE_OUTPUT_DQCHECK_DIR, PLUMBLINE_OUTPUT_DQCHECK_VISUALS_DIR, PLUMBLINE_OUTPUT_THRESHOLD_VALIDATOR_DIR, PLUMBLINE_OUTPUT_THRESHOLD_VALIDATOR_VISUALS_DIR, PLUMBLINE_LOG_DIR, PLUMBLINE_OBSERVABILITY_DIR])

        instrument_configs = load_manual_config_file(PLUMBLINE_INSTRUMENT_NAME)

        prefix = ""
        if in_read_mode in ("automatic", "manual", "all"):
            if in_read_mode == "automatic":
                prefix = "RAD"
            elif in_read_mode == "manual":
                prefix = "RMD"

            logger_message = f"Read mode: {in_read_mode}"
            logger.info(generate_log_success_message(logger_module, logger_module_info, logger_message))
        else:
            e = "Invalid read mode"
            logger.error(generate_log_error_message(logger_module, logger_module_info, e))
            sys.exit(1)

        input_files = []

        all_files = get_all_files_in_directory(PLUMBLINE_INPUT_DATA_DIR, instrument_configs["input_files_format"])

        if in_read_mode == "all" and in_id_list == ["all"]:
            logger_message = "Reading all files for the different types of readings"
            logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_message))
            input_files = all_files

        elif in_read_mode == "all" and in_id_list != ["all"]:
            logger_message = "Reading all files for the specific id list"
            logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_message))
            for file_id in in_id_list:
                expected_suffix = file_id + instrument_configs["input_files_format"]
                matches = [f for f in all_files if f.endswith(expected_suffix)]
                if matches:
                    for m in matches:
                        input_files.append(m)
                        logger_message = "File " + m + " added to queue"
                        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_message))
                else:
                    logger_message = "Error selecting files"
                    logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_message))
                    sys.exit(1)

        elif in_read_mode in ("automatic", "manual") and in_id_list == ["all"]:
            logger_message = f"Getting {in_read_mode} readings for all files"
            logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_message))
            matched_files = [f for f in all_files if f.startswith(prefix)]
            if matched_files:
                for m in matched_files:
                    input_files.append(m)
                    logger_message = "File " + m + " added to queue"
                    logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_message))
            else:
                logger_message = "Error selecting files"
                logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_message))
                sys.exit(1)

        elif in_read_mode in ("automatic", "manual") and in_id_list != ["all"]:
            logger_message = f"Getting {in_read_mode} readings for all files"
            logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_message))
            for file_id in in_id_list:
                expected_suffix = file_id + instrument_configs["input_files_format"]
                matches = [f for f in all_files if f.startswith(prefix) and f.endswith(expected_suffix)]
                if matches:
                    for m in matches:
                        input_files.append(m)
                else:
                    logger_message = "Error selecting files"
                    logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_message))
                    sys.exit(1)
        else:
            logger_message = "Unknown combination"
            logger.error(generate_log_starting_message(logger_module, logger_module_info, logger_message))
            sys.exit(1)

        logger_message = f"Files for this run: {input_files}"
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_message))

        if in_read_mode == "all":
            for run_mode in PLUMBLINE_RUN_MODES:
                # Filtra os ficheiros de acordo com o modo
                if run_mode == "automatic":
                    filtered_files = [file for file in input_files if file.startswith("RAD")]
                elif run_mode == "manual":
                    filtered_files = [file for file in input_files if file.startswith("RMD")]
                else:
                    filtered_files = []

                for file in filtered_files:
                    logger_message = f"Processing file {file} - {run_mode} reading"
                    logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_message))
                    process_individual_file(file, run_mode, in_year_list)

        else:
            if in_read_mode == "automatic":
                filtered_files = [file for file in input_files if file.startswith("RAD")]
            elif in_read_mode == "manual":
                filtered_files = [file for file in input_files if file.startswith("RMD")]
            else:
                logger_message = f"Invalid read mode: {in_read_mode}"
                logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_message))
                sys.exit(1)


            for file in filtered_files:
                logger_message = f"Processing file {file} - {in_read_mode} reading"
                logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_message))
                process_individual_file(file, in_read_mode, in_year_list)

        end_function()
    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)
