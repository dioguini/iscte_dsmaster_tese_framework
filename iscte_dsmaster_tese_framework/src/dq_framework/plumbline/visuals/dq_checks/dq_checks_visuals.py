"""
This script is responsible for creating visuals for DQ Checks
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.dq_framework.utils.dq_utils import generate_log_starting_message, generate_log_success_message, generate_log_error_message
from utils.dq_utils import setup_logger, format_date_logger, create_directory
from configs.framework import PLUMBLINE_LOG_DIR
import pandas as pd
import matplotlib.pyplot as plt


def create_dqcheck_visual_plot(in_dqchecks_results_dict: dict, in_plot_title: str, in_full_output_visual_dir: str) -> None:
    """
    Generates a horizontal bar chart to visually represent the results of Data Quality (DQ) check metrics.

    Each bar corresponds to a specific metric and its computed value, enabling visual interpretation
    of metric magnitudes and their relative differences.

    Args:
        in_dqchecks_results_dict (dict): Dictionary with metric names as keys and their numerical values as values.
        in_plot_title (str): Title to be displayed on the chart.
        in_full_output_visual_dir (str): Full path (including filename) where the PNG chart will be saved.

    Returns:
        None. Saves the chart as a .png file in the specified output directory.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"REPORTING"
    logger_module_info = f"DQ CHECKS - VISUAL"
    logger_starter_message = f"Generating visual file"
    logger_success_message = f"Plot generated"

    plot_x_label = f"Value"
    plot_y_label = f"DQ Check"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        plt.figure(figsize=(21, 10))

        # Convert dict to DataFrame
        df = pd.DataFrame(list(in_dqchecks_results_dict.items()), columns=["metric", "value"])
        df = df.sort_values(by="value", ascending=True)

        bars = plt.barh(df['metric'], df['value'])

        for bar in bars:
            plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2,
                     f"{bar.get_width():.4f}", va='center', fontsize=12)

        plt.title(in_plot_title, fontsize=13)
        plt.xlabel(plot_x_label, fontsize=13)
        plt.ylabel(plot_y_label, fontsize=13)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()
        plt.savefig(in_full_output_visual_dir, bbox_inches='tight')
        plt.close()

        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)


def generate_dqcheck_absolute_metrics_plot(in_abs_metrics:dict, in_plumbline_id: str, in_output_visual_dir: str, in_read_mode:str, in_year:int, in_dq_dimension: str) -> None:
    """
    Generates a bar plot of absolute-type metrics (suffix `_abs`) resulting from Data Quality checks for a specific sensor file.

    This function filters and visualizes only metrics that are expressed in absolute terms (e.appendix_g., count, time interval),
    typically excluding proportions or percentages. The generated plot is stored as a PNG.

    Args:
        in_abs_metrics (dict): Dictionary of absolute metric names and their corresponding values.
        in_plumbline_id (str): Unique identifier of the plumb line sensor file.
        in_output_visual_dir (str): Output directory where the plot will be saved.
        in_read_mode (str): Reading mode of the sensor data (e.appendix_g., 'manual' or 'automatic').
        in_year (int): Reference year of the analysis.
        in_dq_dimension (str): Name of the Data Quality dimension under analysis (e.appendix_g., 'Timeliness').

    Returns:
        None. Saves the absolute metrics plot to the output directory.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"REPORTING"
    logger_module_info = f"DQ CHECKS - VISUAL"
    logger_starter_message = f"Generating DQ Checks Report for Absolute metric type - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings) - Absolute Metric Type "

    plot_title = f"DQ Checks - {in_dq_dimension} - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings) - Absolute Metric Type"
    plot_filename = f"DQcheck_{in_dq_dimension}_{in_read_mode}_{in_year}_{in_plumbline_id}_AbsoluteMetrics.png"
    full_plot_path = os.path.join(in_output_visual_dir, plot_filename)

    logger_success_message = f"Plot saved in: {full_plot_path}"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        os.makedirs(in_output_visual_dir, exist_ok=True)
        create_dqcheck_visual_plot(in_abs_metrics, plot_title, full_plot_path)

        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)


def generate_dqcheck_percentage_metrics_plot(in_prctg_metrics: dict, in_plumbline_id: str, in_output_visual_dir: str, in_read_mode:str, in_year:int, in_dq_dimension: str) -> None:
    """
    Generates a bar plot of percentage-type metrics (suffix `_prctg`) resulting from Data Quality checks for a specific sensor file.

    The function visualizes proportion-based metrics, such as completeness or coverage rates, and outputs
    a dedicated PNG file per dimension, improving interpretability of relative quality indicators.

    Args:
        in_prctg_metrics (dict): Dictionary of percentage metric names and their corresponding values.
        in_plumbline_id (str): Unique identifier of the plumb line sensor file.
        in_output_visual_dir (str): Output directory where the plot will be saved.
        in_read_mode (str): Reading mode of the sensor data (e.appendix_g., 'manual' or 'automatic').
        in_year (int): Reference year of the analysis.
        in_dq_dimension (str): Name of the Data Quality dimension under analysis (e.appendix_g., 'Completeness').

    Returns:
        None. Saves the percentage metrics plot to the output directory.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"REPORTING"
    logger_module_info = f"DQ CHECKS - VISUAL"
    logger_starter_message = f"Generating DQ Checks Report for Percentage metric type - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings) - Percentage Metric Type"

    plot_title = f"DQ Checks - {in_dq_dimension} - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings) - Percentage Metric Type"
    plot_filename = f"DQcheck_{in_dq_dimension}_{in_read_mode}_{in_year}_{in_plumbline_id}_PercentageMetrics.png"
    full_plot_path = os.path.join(in_output_visual_dir, plot_filename)

    logger_success_message = f"Plot saved in: {full_plot_path}"
    
    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        create_dqcheck_visual_plot(in_prctg_metrics, plot_title, full_plot_path)

        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)
