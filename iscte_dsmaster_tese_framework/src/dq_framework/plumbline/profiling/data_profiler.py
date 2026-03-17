"""
This script is responsible by implementing Data Proflining techniques.
It uses ydataProfiling and generates year and year_month profile distribution
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.dq_framework.utils.dq_utils import generate_log_starting_message, generate_log_success_message, generate_log_error_message
from utils.dq_utils import setup_logger
from configs.framework import PLUMBLINE_LOG_DIR
import pandas as pd
from ydata_profiling import ProfileReport
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


def generate_profiling_html_report(in_sensor_data: pd.DataFrame, in_instrument_configs:dict, in_output_visual_dir: str, in_plumbline_id:str, in_read_mode:str, in_year: int) -> None:
    """
    Generates a data profiling report for sensor data of a single joint (plumbline).

    This function produces an interactive HTML profiling report using the `ydata_profiling.ProfileReport` library.
    It selects only the configured columns for analysis and provides a detailed overview of the dataset.

    Args:
        in_sensor_data (pd.DataFrame): Input sensor dataset.
        in_instrument_configs (dict): Configuration dictionary containing the list of columns (key: 'profiling_columns').
        in_output_visual_dir (str): Directory where the HTML report will be saved.
        in_plumbline_id (str): Identifier of the plumbline or joint for naming the output files.
        in_read_mode (str): Mode of reading sensor data (e.appendix_g., "manual", "automatic").
        in_year (int): Year of the data.

    Returns:
        None

    Outputs:
        - Interactive HTML file with profiling results.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"PROFILING"
    logger_module_info = f"GENERATING PROFILING HTML REPORT"
    logger_starter_message = f"Generating Data Profiling Report - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings) - Data Profiling Report"

    profiling_html_report_filename = f"ProfilingSummaryReport_{in_read_mode}_{in_year}_{in_plumbline_id}.html"
    profiling_html_report_full_filename = os.path.join(in_output_visual_dir, profiling_html_report_filename)

    logger_success_message = f"Data Profiling html report successfully generated: {profiling_html_report_full_filename}"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        profiling_columns = in_instrument_configs["profiling_columns"][in_read_mode]
        df_filtered = in_sensor_data[profiling_columns].copy()

        profile_html = ProfileReport(df_filtered,
                                     title=f"Profiling SummaryReport - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings) - Profiling Output",
                                     minimal=True, explorative=True)  # remove minial to perform full analysis

        os.makedirs(in_output_visual_dir, exist_ok=True)
        profile_html.to_file(profiling_html_report_full_filename)
        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)

def generate_profiling_csv_report(in_sensor_data: pd.DataFrame, in_instrument_configs:dict, in_output_results_dir: str, in_plumbline_id:str, in_read_mode:str, in_year: int) -> None:
    """
    Generates a descriptive statistics CSV profiling report for sensor data of a single joint (plumbline).

    This function uses pandas `.describe()` to create summary statistics for the columns
    configured in the instrument configuration.

    Args:
        in_sensor_data (pd.DataFrame): Input sensor dataset.
        in_instrument_configs (dict): Configuration dictionary containing the list of columns (key: 'profiling_columns').
        in_output_results_dir (str): Directory where the CSV file will be saved.
        in_plumbline_id (str): Identifier of the plumbline or joint.
        in_read_mode (str): Mode of reading sensor data (e.appendix_g., "manual", "automatic").
        in_year (int): Year of the data.

    Returns:
        None

    Outputs:
        - CSV file with descriptive statistics for the selected columns.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"PROFILING"
    logger_module_info = f"GENERATING PROFILING CSV REPORT"
    logger_starter_message = f"Generating Data Profiling Report - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings) - Data Profiling Report"

    profiling_csv_report_filename = f"ProfilingSummary_{in_read_mode}_{in_year}_{in_plumbline_id}.csv"
    profiling_csv_report_full_filename = os.path.join(in_output_results_dir, profiling_csv_report_filename)

    logger_success_message = f"Data Profiling csv report successfully generated: {profiling_csv_report_full_filename}"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        profiling_columns = in_instrument_configs["profiling_columns"][in_read_mode]

        df_filtered = in_sensor_data[profiling_columns].copy()

        os.makedirs(in_output_results_dir, exist_ok=True)
        df_filtered.describe(include='all').to_csv(profiling_csv_report_full_filename)

        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)


def generate_year_distribution(in_sensor_data: pd.DataFrame, in_ouput_results_output_dir: str, in_output_visual_dir: str, in_plumbline_id: str, in_read_mode: str, in_year: int) -> None:
    """
    Generates a summary and visualisation of the total number of sensor readings per year.

    This function groups the dataset by 'ANO_STR' and counts the number of records per year.
    It exports the results to a CSV file and creates a bar chart for visual inspection.

    Args:
        in_sensor_data (pd.DataFrame): DataFrame containing at least the 'ANO_STR' column.
        in_ouput_results_output_dir (str): Directory to save the CSV report.
        in_output_visual_dir (str): Directory to save the visual bar plot.
        in_plumbline_id (str): Identifier of the plumbline or joint.
        in_read_mode (str): Mode of reading sensor data.
        in_year (int): Year of the data.

    Returns:
        None

    Outputs:
        - CSV file summarising yearly record distribution.
        - Bar plot image showing total readings per year.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"REPORTING"
    logger_module_info = f"GENERATING YEAR PROFILING"

    try:
        logger = setup_logger(PLUMBLINE_LOG_DIR)
        logger_starter_message = f"Generating Year Data Profiling csv Report - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings) - Year Data Profiling Report"

        csv_filename = f"ProfilingSummaryYear_{in_read_mode}_{in_year}_{in_plumbline_id}.csv"
        csv_full_filename = os.path.join(in_ouput_results_output_dir, csv_filename)

        logger_success_message = f"Year Data Profiling csv report successfully generated: {csv_filename}"

        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        # Gerar distribuição por ANO e MES
        distribution_df = (
            in_sensor_data
            .groupby(["ANO_STR"])
            .size()
            .reset_index(name="TOTAL_RECORDS")
        )

        # Criar diretoria se necessário
        distribution_df.insert(0, "READ_MODE", in_read_mode)
        distribution_df.insert(0, "PLUMBLINE_ID", in_plumbline_id)
        os.makedirs(in_ouput_results_output_dir, exist_ok=True)
        #distribution_df.to_csv(csv_full_filename, sep=";", index=False)
        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

        try:
            logger = setup_logger(PLUMBLINE_LOG_DIR)
            logger_module = f"REPORTING"
            logger_module_info = f"GENERATING YEAR PROFILING - VISUAL"
            logger_starter_message = f"Generating Year Data Profiling plot - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings) - Year Data Profiling Report"


            plot_title = f"Year Data Profiling - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings)"
            plot_filename = f"ProfilingSummaryYear_{in_read_mode}_{in_year}_{in_plumbline_id}.png"
            full_plot_path = os.path.join(in_output_visual_dir, plot_filename)

            logger_success_message = f"Year Data Profiling plot successfully generated: {full_plot_path}"

            logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
            plt.figure(figsize=(15, 10))

            bars = plt.bar(distribution_df["ANO_STR"], distribution_df["TOTAL_RECORDS"], width=0.1)

            for bar in bars:
                height = bar.get_height()
                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + 50,
                    f"{int(height)}",
                    ha='center',
                    va='center',
                    fontsize=10
                )

            plt.xlabel("Year")
            plt.ylabel("# Readings")
            plt.xticks(rotation=45)
            plt.title(plot_title)
            os.makedirs(in_output_visual_dir, exist_ok=True)
            #plt.savefig(full_plot_path)
            plt.close()

            logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))
        except Exception as e:
            logger.error(generate_log_error_message(logger_module, logger_module_info, e))
            sys.exit(1)
    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)
def generate_year_month_distribution(in_sensor_data: pd.DataFrame, in_output_results_dir: str, in_output_visual_dir: str, in_plumbline_id: str, in_read_mode: str, in_year: int) -> None:
    """
    Generates a summary and visualisation of the total number of sensor readings per month and year.

    This function groups the dataset by 'YEAR_MONTH_STR' and 'DATA_MONTH',
    counts the number of records for each month, and creates both a CSV report and a bar chart.

    Args:
        in_sensor_data (pd.DataFrame): DataFrame containing 'YEAR_MONTH_STR' and 'DATA_MONTH' columns.
        in_output_results_dir (str): Directory to save the CSV report.
        in_output_visual_dir (str): Directory to save the visual bar plot.
        in_plumbline_id (str): Identifier of the plumbline or joint.
        in_read_mode (str): Mode of reading sensor data.
        in_year (int): Year of the data.

    Returns:
        None

    Outputs:
        - CSV file summarising monthly record distribution.
        - Bar plot image showing total readings per month.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"REPORTING"
    logger_module_info = f"GENERATING YEAR PROFILING"

    try:
        logger = setup_logger(PLUMBLINE_LOG_DIR)
        logger_starter_message = f"Generating Year-Month Data Profiling csv Report - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings) - Year-Month Data Profiling Report"

        csv_filename = f"ProfilingSummaryYearMonth_{in_read_mode}_{in_year}_{in_plumbline_id}.csv"
        csv_full_filename = os.path.join(in_output_results_dir, csv_filename)

        logger_success_message = f"Year-Month Data Profiling csv report successfully generated: {csv_full_filename}"

        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        # Gerar distribuição por ANO e MES

        distribution_df = in_sensor_data.groupby(["YEAR_MONTH_STR", "DATA_MONTH"]).size().reset_index(name="TOTAL_RECORDS")

        total_year_records = in_sensor_data.shape[0]

        # Ordenar por YEAR_MONTH (datetime)
        df_grouped_sorted = distribution_df.sort_values("DATA_MONTH")

        # Criar diretoria se necessário
        df_grouped_sorted.insert(0, "READ_MODE", in_read_mode)
        df_grouped_sorted.insert(0, "PLUMBLINE_ID", in_plumbline_id)
        os.makedirs(in_output_results_dir, exist_ok=True)
        df_grouped_sorted = df_grouped_sorted.sort_values(by=["DATA_MONTH"], ascending=[True])
        df_grouped_sorted = df_grouped_sorted.sort_values(by=["DATA_MONTH"], ascending=[True])
        df_grouped_sorted.to_csv(csv_full_filename, sep=";", index=False)
        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

        try:
            logger = setup_logger(PLUMBLINE_LOG_DIR)
            logger_module = f"REPORTING"
            logger_module_info = f"GENERATING YEAR-MONTHLY PROFILING - VISUAL"
            logger_starter_message = f"Generating Year-Month Data Profiling plot - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings) - Year-MONTHLY Data Profiling Report"
            logger_success_message = f"Year-Monthly Data Profiling plot successfully generated: "

            plot_title = f"Year-Month Data Profiling - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings) - Total of {total_year_records} readings"
            plot_filename = f"ProfilingSummaryYearMonth_{in_read_mode}_{in_year}_{in_plumbline_id}.png"
            full_plot_path = os.path.join(in_output_visual_dir, plot_filename)

            logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
            plt.figure(figsize=(15, 10))

            bars = plt.bar(df_grouped_sorted["YEAR_MONTH_STR"], df_grouped_sorted["TOTAL_RECORDS"])

            for bar in bars:
                height = bar.get_height()
                plt.text(
                    bar.get_x() + bar.get_width() / 2,  # centro da barra no eixo x
                    height + 10,  # meio da barra no eixo y
                    f"{int(height)}",  # valor a mostrar
                    ha='center',  # horizontal alignment
                    va='center',  # vertical alignment
                    fontsize=9
                )

            plt.xlabel("Year_Month")
            plt.ylabel("# Readings")
            plt.title(plot_title)
            plt.xticks(rotation=45)
            os.makedirs(in_output_visual_dir, exist_ok=True)
            plt.savefig(full_plot_path)
            plt.close()

            logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))
        except Exception as e:
            logger.error(generate_log_error_message(logger_module, logger_module_info, e))
            sys.exit(1)
    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)