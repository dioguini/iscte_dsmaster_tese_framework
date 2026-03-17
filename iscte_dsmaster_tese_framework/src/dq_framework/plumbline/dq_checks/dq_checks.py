"""
This script is responsible by implementing the different Data Quality Checks that will run for each joint (when reading individual senors dq_framework files).
Each check should always have a description for a better understanding.
The return should be a dictionary. Don't forget to add a threshold then to be compared with (in configs/configs.py
NOTE:
    ALWAYS add
       -> _prctg (when a metric is a Percentage)
       -> _abs (when a metric is a Absolute OR not a Percentage metric)
    It's helpful for visuals.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from utils.dq_utils import setup_logger, format_date_logger, create_directory
from src.dq_framework.utils.dq_utils import generate_log_starting_message, generate_log_success_message, generate_log_error_message
from configs.framework import PLUMBLINE_LOG_DIR, PLUMBLINE_OBSERVABILITY_DIR
import pandas as pd
from typing import Dict, List


def check_completeness_automatic(in_sensor_data: pd.DataFrame, in_dq_dimension: str, in_instrument_configs: dict, in_plumbline_id:str, in_year:str) -> Dict[str, float]:
    """
    Evaluates the data completeness of a sensor dataset for a single joint (plumbline sensor) in automatic mode.

    This function computes metrics related to:
    - Missing data across time references (day, hour, minute) and displacement values.
    - Frequency of excessive readings per time unit (day, hour, minute).
    - Redundant records per time unit.
    These are used to assess the completeness and reliability of automatic sensor data.

    Args:
        in_sensor_data (pd.DataFrame): The input dataset, must contain timestamp columns and displacement values.
        in_dq_dimension (str): The data quality dimension (typically "Completeness").
        in_instrument_configs (dict): Dictionary with instrument-specific configuration thresholds.

    Returns:
        Dict[str, float]: Dictionary containing completeness metrics, with suffixes:
            - _abs for absolute values (counts)
            - _prctg for percentage-based metrics
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"DQ CHECKS"
    logger_module_info = f"RUNNING DQ CHECKS - COMPLETENESS AUTOMATIC READINGS"
    logger_starter_message = f"Running DQ Checks for Completeness Automatic readings"
    logger_success_message = f"Dictionary saved in memory"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        completeness_config = in_instrument_configs["dq_checks"][in_dq_dimension]["automatic"]

        max_allowed_per_day = completeness_config["max_allowed_records_per_day"]
        max_allowed_per_hour = completeness_config["max_allowed_records_per_hour"]
        max_allowed_per_minute = completeness_config["max_allowed_records_per_minute"]

        missing_DESLOCRADIALABS_prctg = in_sensor_data["DESLOCRADIALABS"].isna().mean()
        missing_DESLOCRADIALABS_abs = int(in_sensor_data["DESLOCRADIALABS"].isna().sum())

        missing_DESLOCTANGABS_prctg = in_sensor_data["DESLOCTANGABS"].isna().mean()
        missing_DESLOCTANGABS_abs = int(in_sensor_data["DESLOCTANGABS"].isna().sum())

        # Missing values
        missing_data_day_prctg = in_sensor_data["DATA_DAY"].isna().mean()
        missing_data_day_abs = int(in_sensor_data["DATA_DAY"].isna().sum())

        missing_data_hour_prctg = in_sensor_data["DATA_HOUR"].isna().mean()
        missing_data_hour_abs = int(in_sensor_data["DATA_HOUR"].isna().sum())

        missing_data_minute_prctg = in_sensor_data["DATA_MINUTE"].isna().mean()
        missing_data_minute_abs = int(in_sensor_data["DATA_MINUTE"].isna().sum())

        # Records per day
        records_per_day = in_sensor_data.groupby("DATA_DAY").size()
        days_with_multiple_records_abs = int((records_per_day > max_allowed_per_day).sum())
        total_days = records_per_day.shape[0]
        days_with_multiple_records_prctg = days_with_multiple_records_abs / total_days if total_days > 0 else 0

        records_per_hour_agg = in_sensor_data.groupby("DATA_HOUR").size()
        hours_with_multiple_records_abs = int((records_per_hour_agg > max_allowed_per_hour).sum())
        total_hours = records_per_hour_agg.shape[0]
        hours_with_multiple_records_prctg = hours_with_multiple_records_abs / total_hours if total_hours > 0 else 0

        records_per_minute = in_sensor_data.groupby("DATA_MINUTE").size()
        minutes_with_multiple_records_abs = int((records_per_minute > max_allowed_per_minute).sum())
        total_minutes = records_per_minute.shape[0]
        minutes_with_multiple_records_prctg = minutes_with_multiple_records_abs / total_minutes if total_minutes > 0 else 0

        # Redundancy
        redundant_records_day_abs = int((records_per_day[records_per_day > max_allowed_per_day] - max_allowed_per_day).sum())
        redundant_records_hours_abs = int((records_per_hour_agg[records_per_hour_agg > max_allowed_per_hour] - max_allowed_per_hour).sum())
        redundant_records_minutes_abs = int((records_per_minute[records_per_minute > max_allowed_per_minute] - max_allowed_per_minute).sum())

        ##############################
        # Observability
        ##############################
        # Identificar horas com mais de 1 registo
        multiple_hours_obs_idx = records_per_hour_agg[records_per_hour_agg > max_allowed_per_hour].index

        # Obter os registos dessas horas
        multiple_hours_obs_df = in_sensor_data[in_sensor_data["DATA_HOUR"].isin(multiple_hours_obs_idx)].copy()

        # Adicionar coluna TOTAL
        multiple_hours_obs_df["TOTAL"] = multiple_hours_obs_df["DATA_HOUR"].map(records_per_hour_agg.to_dict())


        multiple_hours_obs_df_agg = (
            multiple_hours_obs_df
            .groupby(["ANO", "MES", "DIA", "HORA"])
            .size()
            .reset_index(name="TOTAL")
        )

        multiple_hours_obs_df_agg["COUNT"] = 1

        # [OBSERVABILITY] redundant_records_hours_abs
        # Calcular agregação por hora
        records_per_hour_agg = in_sensor_data.groupby("DATA_HOUR").size()

        # Identificar horas com excesso de registos
        redundant_hours_obs_idx = records_per_hour_agg[records_per_hour_agg > max_allowed_per_hour].index

        # Obter todos os registos dessas horas
        redundant_hours_obs_df = in_sensor_data[in_sensor_data["DATA_HOUR"].isin(redundant_hours_obs_idx)].copy()

        # Adicionar coluna TOTAL = número de registos por hora
        redundant_hours_obs_df["TOTAL"] = redundant_hours_obs_df["DATA_HOUR"].map(records_per_hour_agg.to_dict())


        redundant_hours_obs_df_agg = (
            redundant_hours_obs_df
            .groupby(["ANO", "MES", "DIA", "HORA"])
            .size()
            .reset_index(name="TOTAL")
        )

        redundant_hours_obs_df_agg["TOTAL"] = redundant_hours_obs_df_agg["TOTAL"]-1

        # Observability Layer
        save_observability_to_csv("detailed","hours_with_multiple_records_abs", multiple_hours_obs_df, in_plumbline_id, in_dq_dimension,"automatic",in_year, ["ANO", "MES", "DIA", "HORA", "MINUTO", "DESLOCRADIALABS", "DESLOCTANGABS"])
        save_observability_to_csv("detailed","redundant_records_hours_abs", redundant_hours_obs_df, in_plumbline_id, in_dq_dimension,"automatic", in_year, ["ANO", "MES", "DIA", "HORA", "MINUTO", "DESLOCRADIALABS", "DESLOCTANGABS"])

        # Observability Layer AGG
        save_observability_to_csv("aggregated","hours_with_multiple_records_abs", multiple_hours_obs_df_agg, in_plumbline_id, in_dq_dimension,"automatic",in_year, ["ANO", "MES", "DIA", "HORA", "COUNT"])
        save_observability_to_csv("aggregated","redundant_records_hours_abs", redundant_hours_obs_df_agg, in_plumbline_id, in_dq_dimension,"automatic", in_year, ["ANO", "MES", "DIA", "HORA", "TOTAL"])


        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

        return {
            "days_with_multiple_records_abs": days_with_multiple_records_abs,
            "days_with_multiple_records_prctg": round(days_with_multiple_records_prctg,2),
            "hours_with_multiple_records_abs": hours_with_multiple_records_abs,
            "hours_with_multiple_records_prctg": round(hours_with_multiple_records_prctg,2),
            "minutes_with_multiple_records_abs": minutes_with_multiple_records_abs,
            "minutes_with_multiple_records_prctg": round(minutes_with_multiple_records_prctg,2),
            "missing_data_day_abs": missing_data_day_abs,
            "missing_data_day_prctg": round(missing_data_day_prctg,2),
            "missing_data_hour_abs": missing_data_hour_abs,
            "missing_data_hour_prctg": round(missing_data_hour_prctg,2),
            "missing_data_minute_abs": missing_data_minute_abs,
            "missing_data_minute_prctg": round(missing_data_minute_prctg,2),
            "missing_DESLOCRADIALABS_abs": missing_DESLOCRADIALABS_abs,
            "missing_DESLOCRADIALABS_prctg": round(missing_DESLOCRADIALABS_prctg,2),
            "missing_DESLOCTANGABS_abs": missing_DESLOCTANGABS_abs,
            "missing_DESLOCTANGABS_prctg": round(missing_DESLOCTANGABS_prctg,2),
            "redundant_records_day_abs": redundant_records_day_abs,
            "redundant_records_hours_abs": redundant_records_hours_abs,
            "redundant_records_minutes_abs": redundant_records_minutes_abs
        }

    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)

def check_completeness_manual(in_sensor_data: pd.DataFrame, in_dq_dimension: str, in_instrument_configs: dict, in_plumbline_id:str, in_year:str) -> Dict[str, float]:
    """
    Evaluates the data completeness of a sensor dataset for a single joint (plumbline sensor) in manual mode.

    This function focuses on:
    - Identifying missing values in key columns.
    - Detecting days with more readings than expected.
    - Quantifying redundancy (extra records above expected frequency).
    These checks are adapted for lower-frequency, manual data acquisition.

    Args:
        in_sensor_data (pd.DataFrame): The input dataset with expected time and displacement fields.
        in_dq_dimension (str): The data quality dimension (e.appendix_g., "Completeness").
        in_instrument_configs (dict): Configuration dictionary with manual thresholds.

    Returns:
        Dict[str, float]: Dictionary containing completeness metrics:
            - _abs for absolute counts
            - _prctg for proportions of total
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"DQ CHECKS"
    logger_module_info = f"RUNNING DQ CHECKS - COMPLETENESS MANUAL READINGS"
    logger_starter_message = f"Running DQ Checks for Completeness Manual readings"
    logger_success_message = f"Dictionary saved in memory"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        completeness_config = in_instrument_configs["dq_checks"][in_dq_dimension]["manual"]
        max_allowed_per_day = completeness_config["max_allowed_records_per_day"]

        missing_DESLOCRADIALABS_prctg = in_sensor_data["DESLOCRADIALABS"].isna().mean()
        missing_DESLOCRADIALABS_abs = int(in_sensor_data["DESLOCRADIALABS"].isna().sum())

        missing_DESLOCTANGABS_prctg = in_sensor_data["DESLOCTANGABS"].isna().mean()
        missing_DESLOCTANGABS_abs = int(in_sensor_data["DESLOCTANGABS"].isna().sum())

        # Missing values
        missing_data_day_prctg = in_sensor_data["DATA_DAY"].isna().mean()
        missing_data_day_abs = int(in_sensor_data["DATA_DAY"].isna().sum())

        # Records per day
        records_per_day = in_sensor_data.groupby("DATA_DAY").size()
        days_with_multiple_records_abs = int((records_per_day > max_allowed_per_day).sum())
        total_days = records_per_day.shape[0]
        days_with_multiple_records_prctg = days_with_multiple_records_abs / total_days if total_days > 0 else 0

        # Redundancy
        redundant_records_day_abs = int((records_per_day[records_per_day > max_allowed_per_day] - 1).sum())

        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

        return {
            "days_with_multiple_records_abs": days_with_multiple_records_abs,
            "days_with_multiple_records_prctg": round(days_with_multiple_records_prctg,2),
            "missing_data_day_abs": missing_data_day_abs,
            "missing_data_day_prctg": round(missing_data_day_prctg,2),
            "missing_DESLOCRADIALABS_abs": missing_DESLOCRADIALABS_abs,
            "missing_DESLOCRADIALABS_prctg": round(missing_DESLOCRADIALABS_prctg,2),
            "missing_DESLOCTANGABS_abs": missing_DESLOCTANGABS_abs,
            "missing_DESLOCTANGABS_prctg": round(missing_DESLOCTANGABS_prctg,2),
            "redundant_records_day_abs": redundant_records_day_abs
        }
    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)


def check_timeliness_automatic(in_sensor_data: pd.DataFrame, in_dq_dimension: str, in_instrument_configs: dict, in_plumbline_id:str, in_year:str) -> Dict[str, float]:
    """
    Evaluates the timeliness of sensor data collected in automatic mode.

    This function measures:
    - Interval statistics between consecutive records (mean, std).
    - Proportions of intervals exceeding defined thresholds.
    - Largest gaps between readings.
    - Record density per time unit (day, hour, minute).
    These indicators are useful to validate temporal consistency in high-frequency sensors.

    Args:
        in_sensor_data (pd.DataFrame): Dataset with datetime fields for day, hour, and minute.
        in_dq_dimension (str): The data quality dimension (e.appendix_g., "Timeliness").
        in_instrument_configs (dict): Configuration with expected intervals and threshold limits.

    Returns:
        Dict[str, float]: Dictionary with timeliness metrics, using:
            - _abs for absolute gaps/counts
            - _prctg for relative proportions
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"DQ CHECKS"
    logger_module_info = f"RUNNING DQ CHECKS - TIMELINESS AUTOMATIC READINGS"
    logger_starter_message = f"Running DQ Checks for Timeliness Automatic readings"
    logger_success_message = f"Dictionary saved in memory"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))

        # load json params
        timeliness_config = in_instrument_configs["dq_checks"][in_dq_dimension]["automatic"]
        max_interval_days = timeliness_config["max_interval_days"]
        max_interval_hours = timeliness_config["max_interval_hours"]
        max_interval_minutes = timeliness_config["max_interval_minutes"]

        # sorting
        in_sensor_data = in_sensor_data.sort_values("DATA_DAY").copy()
        in_sensor_data["DAYS_BETWEEN_RECORDS"] = in_sensor_data["DATA_DAY"].diff().dt.days.fillna(0)

        in_sensor_data = in_sensor_data.sort_values("DATA_HOUR").copy()
        in_sensor_data["HOURS_BETWEEN_RECORDS"] = in_sensor_data["DATA_HOUR"].diff().dt.total_seconds().div(3600).fillna(0)

        in_sensor_data = in_sensor_data.sort_values("DATA_MINUTE").copy()
        in_sensor_data["MINUTES_BETWEEN_RECORDS"] = in_sensor_data["DATA_MINUTE"].diff().dt.total_seconds().div(60).fillna(0)

        # interval statistics
        interval_days_abs = in_sensor_data["DAYS_BETWEEN_RECORDS"].std()
        interval_days_prctg = in_sensor_data["DAYS_BETWEEN_RECORDS"].mean()

        interval_hours_abs = in_sensor_data["HOURS_BETWEEN_RECORDS"].std()
        interval_hours_prctg = in_sensor_data["HOURS_BETWEEN_RECORDS"].mean()

        interval_minutes_abs = in_sensor_data["MINUTES_BETWEEN_RECORDS"].std()
        interval_minutes_prctg = in_sensor_data["MINUTES_BETWEEN_RECORDS"].mean()

        # max gap(s)
        max_gap_days_abs = in_sensor_data["DAYS_BETWEEN_RECORDS"].max()
        max_gap_hours_abs = in_sensor_data["HOURS_BETWEEN_RECORDS"].max()
        max_gap_minutes_abs = in_sensor_data["MINUTES_BETWEEN_RECORDS"].max()

        # total breaking records
        days_apart_previous_record_count_abs = (in_sensor_data["DAYS_BETWEEN_RECORDS"] > max_interval_days).sum()
        hours_apart_previous_record_count_abs = (in_sensor_data["HOURS_BETWEEN_RECORDS"] > max_interval_hours).sum()
        minutes_apart_previous_record_count_abs = (in_sensor_data["MINUTES_BETWEEN_RECORDS"] > max_interval_minutes).sum()

        # percentage proportions
        total_records = len(in_sensor_data)
        days_apart_previous_record_proportion_prctg = days_apart_previous_record_count_abs / total_records
        hours_apart_previous_record_proportion_prctg = hours_apart_previous_record_count_abs / total_records
        minutes_apart_previous_record_proportion_prctg = minutes_apart_previous_record_count_abs / total_records

        # density
        data_day_density_abs = total_records / ((in_sensor_data["DATA_DAY"].max() - in_sensor_data["DATA_DAY"].min()).days + 1)
        delta_hours = (in_sensor_data["DATA_HOUR"].max() - in_sensor_data["DATA_HOUR"].min()).total_seconds() / 3600
        data_hour_density_abs = total_records / (delta_hours + 1)
        delta_minutes = (in_sensor_data["DATA_MINUTE"].max() - in_sensor_data["DATA_MINUTE"].min()).total_seconds() / 60
        data_minute_density_abs = total_records / (delta_minutes + 1)


        # max_gap_hours = in_sensor_data["GAP_HOURS"].max()

        # logger.info("\t[DEBUG]\t>> MAX GAP (hours): {max_gap_hours:.2f}\n")

        # # 3. Obter os registos consecutivos responsáveis
        # max_gap_index = in_sensor_data["GAP_HOURS"].idxmax()
        # previous_record = in_sensor_data.loc[max_gap_index - 1]
        # current_record = in_sensor_data.loc[max_gap_index]

        # logger.info(">>> Registos consecutivos com maior intervalo em horas:")
        # logger.info(f"Anterior: {previous_record['DATA_HOUR']} | DESLOCRADIALABS: {previous_record['DESLOCRADIALABS']}")
        # logger.info(f"Atual:    {current_record['DATA_HOUR']} | DESLOCRADIALABS: {current_record['DESLOCRADIALABS']}")

        # Conversão de colunas para datetime
        # Calcular gaps
        in_sensor_data["GAP_DAYS"] = in_sensor_data["DATA_DAY"].diff().dt.days

        # Identificar os dois registos consecutivos com maior gap
        max_gap_idx = in_sensor_data["GAP_DAYS"].idxmax()
        gap_df = in_sensor_data.loc[[max_gap_idx - 1, max_gap_idx]]


        ##############################
        # Observability
        ##############################

        # gaps
        gap_exceeds = in_sensor_data["GAP_DAYS"] > 1
        gap_indices = in_sensor_data.index[gap_exceeds]

        #identify pair records
        pair_rows = []
        for idx in gap_indices:
            if idx - 1 >= 0:
                pair_rows.append(in_sensor_data.loc[idx - 1])
                pair_rows.append(in_sensor_data.loc[idx])

        gap_days_df = pd.DataFrame(pair_rows)


        #save observability
        save_observability_to_csv("detailed", "days_apart_previous_record_count_abs", gap_days_df, in_plumbline_id, in_dq_dimension, "automatic", in_year, ["ANO", "MES", "DIA", "HORA", "MINUTO", "DESLOCRADIALABS", "DESLOCTANGABS", "DATETIME", "GAP_DAYS"])
        save_observability_to_csv("detailed", "max_gap_days_abs", gap_df, in_plumbline_id, in_dq_dimension,"automatic", in_year, ["ANO", "MES", "DIA", "HORA", "MINUTO", "DESLOCRADIALABS", "DESLOCTANGABS","DATETIME", "GAP_DAYS"])

        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

        return {
            "data_day_density_abs": round(data_day_density_abs, 2),
            "data_hour_density_abs": round(data_hour_density_abs, 2),
            "data_minute_density_abs": round(data_minute_density_abs, 2),
            "days_apart_previous_record_count_abs": round(days_apart_previous_record_count_abs, 2),
            "days_apart_previous_record_proportion_prctg": round(days_apart_previous_record_proportion_prctg, 2),
            "hours_apart_previous_record_count_abs": round(hours_apart_previous_record_count_abs, 2),
            "hours_apart_previous_record_proportion_prctg": round(hours_apart_previous_record_proportion_prctg, 2),
            "minutes_apart_previous_record_count_abs": round(minutes_apart_previous_record_count_abs, 2),
            "minutes_apart_previous_record_proportion_prctg": round(minutes_apart_previous_record_proportion_prctg, 2),
            "interval_days_abs": round(interval_days_abs, 2),
            "interval_days_prctg": round(interval_days_prctg, 2),
            "interval_hours_abs": round(interval_hours_abs, 2),
            "interval_hours_prctg": round(interval_hours_prctg, 2),
            "interval_minutes_abs": round(interval_minutes_abs, 2),
            "interval_minutes_prctg": round(interval_minutes_prctg, 2),
            "max_gap_days_abs": round(max_gap_days_abs, 2),
            "max_gap_hours_abs": round(max_gap_hours_abs, 2),
            "max_gap_minutes_abs": round(max_gap_minutes_abs, 2)
        }

    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)


def check_timeliness_manual(in_sensor_data: pd.DataFrame, in_dq_dimension: str, in_instrument_configs: dict, in_plumbline_id:str, in_year:str) -> Dict[str, float]:
    """
    Evaluates the timeliness of sensor data collected in manual mode.

    This function analyses:
    - Time intervals between readings (mean, std).
    - Gaps exceeding threshold duration (in days).
    - Largest time gap between two records.
    - Density of data points across the monitoring period.

    These indicators help determine if data acquisition follows expected manual frequency (e.appendix_g., every 14 days).

    Args:
        in_sensor_data (pd.DataFrame): Input sensor dataset with 'DATA_DAY' and 'DATA_HOUR' columns.
        in_dq_dimension (str): The DQ dimension under evaluation ("Timeliness").
        in_instrument_configs (dict): Configuration with allowed maximum interval in days.

    Returns:
        Dict[str, float]: Timeliness metrics with _abs for raw values and _prctg for percentages.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"DQ CHECKS"
    logger_module_info = f"RUNNING DQ CHECKS - TIMELINESS MANUAL READINGS"
    logger_starter_message = f"Running DQ Checks for Completeness Automatic readings"
    logger_success_message = f"Dictionary saved in memory"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        timeliness_config = in_instrument_configs["dq_checks"][in_dq_dimension]["manual"]
        max_interval_days = timeliness_config["max_interval_days"]

        in_sensor_data["DAYS_BETWEEN_RECORDS"] = in_sensor_data["DATA_DAY"].diff().dt.days

        interval_days_prctg = in_sensor_data["DAYS_BETWEEN_RECORDS"].mean()
        interval_days_abs = in_sensor_data["DAYS_BETWEEN_RECORDS"].std()

        days_apart_previous_record_proportion_prctg = (in_sensor_data["DAYS_BETWEEN_RECORDS"] > max_interval_days).sum()/ len(in_sensor_data)

        days_apart_previous_record_count_abs = (in_sensor_data["DAYS_BETWEEN_RECORDS"] > max_interval_days).sum()

        max_gap_days_abs = in_sensor_data["DAYS_BETWEEN_RECORDS"].max()

        # Density
        data_day_density_abs = len(in_sensor_data) / ((in_sensor_data["DATA_DAY"].max() - in_sensor_data["DATA_DAY"].min()).days + 1)

        # save observability
        # save_observability_to_csv("days_apart_previous_record_count_abs", gap_days_df, in_plumbline_id, in_dq_dimension, "automatic", in_year)
        # save_observability_to_csv("max_gap_days_abs", gap_df, in_plumbline_id, in_dq_dimension,"automatic",in_year)


        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

        return {
            "data_day_density_abs": round(data_day_density_abs,2),
            "days_apart_previous_record_count_abs": round(days_apart_previous_record_count_abs,2),
            "days_apart_previous_record_proportion_prctg": round(days_apart_previous_record_proportion_prctg,2),
            "interval_days_abs": round(interval_days_abs,2),
            "interval_days_prctg": round(interval_days_prctg,2),
            "max_gap_days_abs": round(max_gap_days_abs,2)
        }

    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)


def save_dqchecks_results_to_csv(in_dqcheck_results: Dict[str, float], in_dq_dimension: str, in_output_results_dir: str, in_plumbline_id: str, in_read_mode:str, in_year: int) -> None:
    """
    Saves Data Quality check results to a CSV file.

    This function transforms a dictionary of DQ results into a structured DataFrame,
    adds contextual metadata (sensor ID, year, read mode, DQ dimension),
    and writes it to a CSV file in the specified output directory.

    Args:
        in_dqcheck_results (Dict[str, float]): Dictionary containing metric names and values.
        in_dq_dimension (str): The DQ dimension to which the metrics belong (e.appendix_g., "Timeliness").
        in_output_results_dir (str): Target folder where the .csv file will be saved.
        in_plumbline_id (str): Unique identifier of the sensor.
        in_read_mode (str): Reading mode of the sensor (e.appendix_g., "manual", "automatic").
        in_year (int): Year of the data being evaluated.

    Returns:
        None. Saves the results directly to disk as a CSV file.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"DQ CHECKS"
    logger_module_info = f"DQ CHECKS - SAVE .CSV"
    logger_starter_message = f"Saving DQ Checks .csv for - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings) - {in_dq_dimension} Dimension"

    file_filename = f"DQCheck_{in_dq_dimension}_{in_read_mode}_{in_year}_{in_plumbline_id}.csv"
    full_file_path = os.path.join(in_output_results_dir, file_filename)
    logger_success_message = f"csv saved in: {full_file_path}"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        df_result = pd.DataFrame(in_dqcheck_results.items(), columns=["metric", "value"])
        df_result.insert(0, "dq_dimension", in_dq_dimension)
        df_result.insert(0, "read_mode", in_read_mode)
        df_result.insert(0, "year", in_year)
        df_result.insert(0, "plumbline_id", in_plumbline_id)
        df_result = df_result.sort_values(by=["metric"], ascending=[True])
        os.makedirs(in_output_results_dir, exist_ok=True)
        df_result.to_csv(full_file_path, index=False, sep=";")
        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)

def save_observability_to_csv(
    in_write_type: str,
    in_dqcheck: str,
    in_dqcheck_records_df: pd.DataFrame,
    in_plumbline_id: str,
    in_dq_dimension: str,
    in_read_mode: str,
    in_year: str,
    in_selected_columns: List[str]
) -> None:
    """
    Guarda o ficheiro detalhado de observability com base nas colunas fornecidas.

    Args:
        in_selected_columns (List[str]): Lista de colunas a guardar no ficheiro final.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = "OBSERVABILITY"
    logger_module_info = "OBSERVABILITY - SAVE DETAIL CSV"
    logger_starter_message = (
        f"[DETALHE] Saving records for check *{in_dqcheck}* "
        f"for Sensor#{in_plumbline_id} ({in_year}, {in_read_mode}) - {in_dq_dimension}"
    )

    if in_write_type == "detailed":
        filename = f"Observability_{in_dq_dimension}_{in_read_mode}_{in_year}_{in_plumbline_id}_{in_dqcheck}.csv"
    elif in_write_type == "aggregated":
        filename = f"ObservabilityAgg_{in_dq_dimension}_{in_read_mode}_{in_year}_{in_plumbline_id}_{in_dqcheck}.csv"
    else: # aggregated
        filename = f"Observability_UNKNOWN_{in_dq_dimension}_{in_read_mode}_{in_year}_{in_plumbline_id}_{in_dqcheck}.csv"

    full_path = os.path.join(PLUMBLINE_OBSERVABILITY_DIR, filename)

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))

        if in_dqcheck_records_df.empty:
            return

        selected_cols = [col for col in in_selected_columns if col in in_dqcheck_records_df.columns]
        in_dqcheck_records_df[selected_cols].to_csv(full_path, index=False, sep=";")

        logger.info(f"[SUCCESS] Observability (DETAIL) saved in: {full_path}")

    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)
