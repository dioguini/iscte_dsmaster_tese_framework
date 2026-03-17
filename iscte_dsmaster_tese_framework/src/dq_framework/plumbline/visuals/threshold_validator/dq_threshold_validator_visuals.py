"""
This script is responsible for creating visuals for Threshold Validator
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.dq_framework.utils.dq_utils import  generate_log_starting_message, generate_log_error_message, generate_log_success_message
from utils.dq_utils import setup_logger, format_date_logger, create_directory
from configs.framework import PLUMBLINE_LOG_DIR, THRESHOLD_VALIDATOR_LABELS, STATUS_COLOR_MAP
import pandas as pd
import matplotlib.pyplot as plt


def create_threshold_validator_visual_plot(
    in_threshold_dict: dict,
    in_plot_title: str,
    in_full_output_visual_dir: str) -> None:
    """
    Generates a combined bar chart and table visualization from the output of the Threshold Validator.

    Each bar represents the number of metrics falling into each alert status category
    (OK, WARNING, ALERT, NO THRESHOLD), while the table below lists the detailed metrics
    with their values, thresholds, differences, and deviations.

    Args:
        in_threshold_dict (dict): Dictionary where each key is a metric name and each value is a tuple:
            (status, metric_value, threshold_value, threshold_diff, threshold_deviation_pct).
        in_plot_title (str): Title to display on the plot.
        in_full_output_visual_dir (str): Full path (including filename) where the PNG chart will be saved.

    Returns:
        None. Generates and saves the chart and table as a PNG file.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"REPORTING"
    logger_module_info = f"THRESHOLD VALIDATOR - VISUAL"
    logger_starter_message = f"Generating visual file"
    logger_success_message = f"Plot generated"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))

        # Convert dict to DataFrame
        df = pd.DataFrame.from_dict(
            in_threshold_dict,
            orient="index",
            columns=["status", "value", "threshold", "threshold_diff", "threshold_deviation_pct"]
        )
        df.insert(0, "metric", df.index)
        df.reset_index(drop=True, inplace=True)

        # Ensure correct status order
        df["status"] = pd.Categorical(
            df["status"],
            categories=THRESHOLD_VALIDATOR_LABELS,
            ordered=True
        )
        df = df.sort_values(by="status")

        # Count metrics by status
        status_counts = df["status"].value_counts().reindex(THRESHOLD_VALIDATOR_LABELS, fill_value=0)

        # === Plot creation ===
        fig, axs = plt.subplots(
            2, 1,
            figsize=(15, 9)  # Menor altura total
            #gridspec_kw={"height_ratios": [0.6, 1.4]},  # Gráfico mais compacto, mais espaço para tabela
            #constrained_layout=True  # Melhor distribuição de espaço
        )

        # Bar plot
        bar_colors = [STATUS_COLOR_MAP[status] for status in THRESHOLD_VALIDATOR_LABELS]
        bars = axs[0].bar(THRESHOLD_VALIDATOR_LABELS, status_counts.values, color=bar_colors)
        axs[0].set_title(in_plot_title)
        axs[0].set_ylabel("# DQ Checks")
        axs[0].tick_params(axis="x", labelrotation=0)
        axs[0].set_ylim(0, max(status_counts.values) + 1)

        for bar in bars:
            yval = bar.get_height()
            axs[0].text(
                bar.get_x() + bar.get_width() / 2,
                yval + 0.1,
                int(yval),
                ha="center",
                va="bottom",
                fontsize=9,
            )

        # Table creation
        table_data = df[["metric", "value", "threshold", "threshold_diff", "threshold_deviation_pct", "status"]].values.tolist()
        column_labels = [
            "Metric",
            "Metric Value",
            "Threshold Value",
            "Threshold Difference",
            "Threshold Deviation (Percentage)",
            "Alert Label",
        ]

        axs[1].axis("off")
        table = axs[1].table(
            cellText=table_data,
            colLabels=column_labels,
            loc="center",
            cellLoc="left"
        )
        #table.auto_set_font_size(False)
        #table.set_fontsize(10)
        table.scale(0.5, 1.5)  # Coloca a tabela mais compacta

        # Fit column widths dynamically
        col_max_lengths = [max([len(str(row[i])) for row in table_data] + [len(col_label)]) for i, col_label in
                           enumerate(column_labels)]
        total_length = sum(col_max_lengths)
        col_widths = [length / total_length for length in col_max_lengths]

        for (row, col), cell in table.get_celld().items():
            cell.set_width(col_widths[col])  # fator de ajuste visual

        plt.tight_layout()
        plt.savefig(in_full_output_visual_dir)
        plt.close()
        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)


def generate_threshold_validator_absolute_metrics_plot (in_threshold_validator_results: dict, in_plumbline_id: str, in_output_visual_dir: str, in_read_mode: str, in_year: int, in_dq_dimension:str) -> None:
    """
    Generates a Threshold Validator chart for absolute-type metrics (_abs) associated with a specific sensor
    and a given Data Quality (DQ) dimension.

    The chart visualizes the distribution of metrics across alert statuses and presents detailed threshold validation
    results for each absolute metric.

    Args:
        in_threshold_validator_results (dict): Dictionary containing threshold validation results for absolute metrics.
        in_plumbline_id (str): Unique identifier of the plumb line sensor (e.appendix_g., '49350').
        in_output_visual_dir (str): Directory where the chart will be saved.
        in_read_mode (str): Sensor read mode ('manual' or 'automatic').
        in_year (int): Reference year of the analysis.
        in_dq_dimension (str): DQ dimension being evaluated (e.appendix_g., 'Timeliness').

    Returns:
        None. Generates and saves the absolute metrics chart as a PNG file.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"REPORTING"
    logger_module_info = f"THRESHOLD VALIDATOR - VISUAL"
    logger_starter_message = f"Generating DQ Checks Report for Percentage metric type - {in_dq_dimension} - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings) - Absolute Metric Type "

    plot_title = f"Threshold Validator - {in_dq_dimension} - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings) - Absolute Metric Type"
    plot_filename = f"ThresholdValidator_{in_dq_dimension}_{in_read_mode}_{in_year}_{in_plumbline_id}_AbsoluteMetrics.png"
    full_plot_path = os.path.join(in_output_visual_dir, plot_filename)

    logger_success_message = f"Plot saved in: {full_plot_path}"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        os.makedirs(in_output_visual_dir, exist_ok=True)
        create_threshold_validator_visual_plot(in_threshold_validator_results, plot_title, full_plot_path)

        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)


def generate_threshold_validator_percentage_metrics_plot(in_threshold_validator_results, in_plumbline_id: str, in_output_visual_dir: str, in_read_mode: str, in_year: int, in_dq_dimension:str) -> None:
    """
    Generates a Threshold Validator chart for percentage-type metrics (_prctg) associated with a specific sensor
    and a given Data Quality (DQ) dimension.

    The chart shows the distribution of percentage metrics across alert statuses and includes a table
    with values, thresholds, differences, and percentage deviations per metric.

    Args:
        in_threshold_validator_results (dict): Dictionary containing threshold validation results for percentage metrics.
        in_plumbline_id (str): Unique identifier of the plumb line sensor (e.appendix_g., '49350').
        in_output_visual_dir (str): Directory where the chart will be saved.
        in_read_mode (str): Sensor read mode ('manual' or 'automatic').
        in_year (int): Reference year of the analysis.
        in_dq_dimension (str): DQ dimension being evaluated (e.appendix_g., 'Completeness').

    Returns:
        None. Generates and saves the percentage metrics chart as a PNG file.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"REPORTING"
    logger_module_info = f"THRESHOLD VALIDATOR - VISUAL"
    logger_starter_message = f"Generating DQ Checks Report for Percentage metric type - {in_dq_dimension} - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings) - Percentage Metric Type "

    plot_title = f"Threshold Validator - {in_dq_dimension} - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings) - Percentage Metric Type"
    plot_filename = f"ThresholdValidator_{in_dq_dimension}_{in_read_mode}_{in_year}_{in_plumbline_id}_PercentageMetrics.png"
    full_plot_path = os.path.join(in_output_visual_dir, plot_filename)

    logger_success_message = f"Plot saved in: {full_plot_path}"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        os.makedirs(in_output_visual_dir, exist_ok=True)
        create_threshold_validator_visual_plot(in_threshold_validator_results, plot_title, full_plot_path)

        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)
