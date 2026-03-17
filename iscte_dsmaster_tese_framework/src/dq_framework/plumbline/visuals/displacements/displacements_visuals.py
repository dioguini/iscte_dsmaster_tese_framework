
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.dq_framework.utils.dq_utils import generate_log_starting_message, generate_log_success_message, generate_log_error_message
from utils.dq_utils import setup_logger, format_date_logger, create_directory
from configs.framework import PLUMBLINE_LOG_DIR, MONTHLY_COLOR_PALETTE
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_monthly_radial_displacement(in_sensor_data_df: pd.DataFrame, in_output_visual_dir: str, in_plumbline_id: str, in_read_mode: str, in_year: int) -> None:
    """
    Generates a violin plot of monthly radial displacements for a specific sensor.

    The plot represents the distribution of displacement values for each month using
    a boxplot-augmented violin plot, helping to identify dispersion, skewness, and outliers
    in radial displacement data throughout the year.

    Args:
        in_sensor_data_df (pd.DataFrame): DataFrame containing at least the columns 'MONTH_NAME_EN' and 'DESLOCRADIALABS'.
        in_output_visual_dir (str): Path where the resulting image file will be saved.
        in_plumbline_id (str): Identifier of the plumbline sensor.
        in_read_mode (str): Reading mode, typically "manual" or "automatic".
        in_year (int): Year corresponding to the data being visualized.

    Returns:
        None. Saves a PNG image in the specified directory.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"REPORTING - DISPLACEMENTS"
    logger_module_info = f"MONTHLY RADIAL DISPLACEMENT - VISUAL"
    logger_starter_message = f"Generating monthly radial displacement plot - Monthly Radial Displacement - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings)"

    plot_title = f"Monthly Radial Displacement - Sensor#{in_plumbline_id} ({in_year} {in_read_mode} readings)"
    plot_x_label = f"Month"
    plot_y_label = f"Displacement (Radial)"

    plot_filename = f"MonthlyRadial_{in_read_mode}_{in_year}_{in_plumbline_id}.png"
    full_plot_path = os.path.join(in_output_visual_dir, plot_filename)

    logger_success_message = f"Plot saved in: {full_plot_path}"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        plt.figure(figsize=(15, 10))

        #plt.plot(in_sensor_data_df["MONTH_NAME_EN"], in_sensor_data_df["DESLOCRADIALABS"], marker="o", linestyle="-", color="royalblue", linewidth=2, markersize=8)

        sns.violinplot(data=in_sensor_data_df,
                       x="MONTH_NAME_EN",
                       y="DESLOCRADIALABS",
                       inner="box",
                       palette=MONTHLY_COLOR_PALETTE)

        plt.title(plot_title)
        plt.xlabel(plot_x_label)
        plt.ylabel(plot_y_label)
        plt.xticks(rotation=45)
        plt.tight_layout()
        os.makedirs(in_output_visual_dir, exist_ok=True)
        plt.savefig(full_plot_path)
        plt.close()

        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)


def plot_monthly_radial_average_displacement(in_sensor_data_df, in_output_visual_dir, in_plumbline_id, in_read_mode, in_year):
    """
    Generates a combined line and violin plot showing the monthly average and distribution of
    radial displacement values (`DESLOCRADIALABS`) for a specific sensor and year.

    Args:
        in_sensor_data_df (pd.DataFrame): DataFrame with 'MES' (month number), 'MONTH_NAME_EN', and 'DESLOCRADIALABS'.
        in_output_visual_dir (str): Directory where the plot will be saved.
        in_plumbline_id (str): Identifier of the plumb line sensor.
        in_read_mode (str): Reading mode ('manual' or 'automatic').
        in_year (int): Year under analysis.

    Returns:
        None. Saves the generated plot to the specified output directory.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"REPORTING - DISPLACEMENTS"
    logger_module_info = f"MONTHLY AVG RADIAL DISPLACEMENT - VISUAL"
    logger_starter_message = f"Generating monthly radial displacement plot - Monthly Radial Displacement - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings)"

    plot_title = f"Monthly Radial Displacement (Average) - Sensor#{in_plumbline_id} ({in_year} {in_read_mode} readings)"
    plot_x_label = f"Month"
    plot_y_label = f"Displacement (Radial - Average)"

    plot_filename = f"MonthlyRadialAvg_{in_read_mode}_{in_year}_{in_plumbline_id}.png"
    full_plot_path = os.path.join(in_output_visual_dir, plot_filename)

    logger_success_message = f"Plot saved in: {full_plot_path}"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        plt.figure(figsize=(15, 10))

        monthly_avg_df = in_sensor_data_df.groupby(["MONTH_NAME_EN", "MES"])["DESLOCRADIALABS"].mean().reset_index()

        monthly_avg_df = monthly_avg_df.sort_values(by="MES", ascending=True)

        plt.plot(monthly_avg_df["MONTH_NAME_EN"], monthly_avg_df["DESLOCRADIALABS"], marker="o", linestyle="-", color="royalblue")

        sns.violinplot(data=in_sensor_data_df,
                       x="MONTH_NAME_EN",
                       y="DESLOCRADIALABS",
                       inner="box",
                       palette=MONTHLY_COLOR_PALETTE)

        # Anotar os valores nas marcas
        for idx, val in enumerate(monthly_avg_df["DESLOCRADIALABS"]):
            plt.text(idx, val, f"{val:.2f}", ha='center', va='bottom', fontsize=9)

        plt.title(plot_title)
        plt.xlabel(plot_x_label)
        plt.ylabel(plot_y_label)
        plt.xticks(rotation=45)
        plt.tight_layout()
        os.makedirs(in_output_visual_dir, exist_ok=True)
        plt.savefig(full_plot_path)
        plt.close()

        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)


def plot_monthly_tangential_displacement(in_sensor_data_df: pd.DataFrame, in_output_visual_dir: str, in_plumbline_id: str, in_read_mode: str, in_year: int) -> None:
    """
    Generates a violin plot showing the monthly distribution of tangential displacement
    (`DESLOCTANGABS`) for a given sensor and year.

    Args:
        in_sensor_data_df (pd.DataFrame): DataFrame containing at least the columns 'MONTH_NAME_EN' and 'DESLOCTANGABS'.
        in_output_visual_dir (str): Directory where the generated plot image will be saved.
        in_plumbline_id (str): Identifier of the plumb line sensor.
        in_read_mode (str): Reading mode ('manual' or 'automatic').
        in_year (int): Year under analysis.

    Returns:
        None. Saves the generated plot to the specified output directory.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"REPORTING - DISPLACEMENTS"
    logger_module_info = f"MONTHLY TANGENTIAL DISPLACEMENT - VISUAL"
    logger_starter_message = f"Generating monthly tangential displacement plot - Monthly Tangential Displacement - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings)"
    logger_success_message = f"Plot saved in: "
    plot_title = f"Monthly Tangential Displacement - Sensor#{in_plumbline_id} ({in_year} {in_read_mode} readings)"
    plot_x_label = f"Month"
    plot_y_label = f"Displacement (Tangential)"

    plot_filename = f"MonthlyRadial_{in_read_mode}_{in_year}_{in_plumbline_id}.png"
    full_plot_path = os.path.join(in_output_visual_dir, plot_filename)

    logger_success_message = f"Plot saved in: {full_plot_path}"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        plt.figure(figsize=(15, 10))

        in_sensor_data_df = in_sensor_data_df.sort_values(by="MES")

        #plt.plot(in_sensor_data_df["MONTH_NAME_EN"], in_sensor_data_df["DESLOCTANGABS"], marker="o", linestyle="-", color="royalblue", linewidth=2, markersize=8)

        sns.violinplot(data=in_sensor_data_df,
                       x="MONTH_NAME_EN",
                       y="DESLOCTANGABS",
                       inner="box",
                       palette=MONTHLY_COLOR_PALETTE)

        plt.title(plot_title)
        plt.xlabel(plot_x_label)
        plt.ylabel(plot_y_label)
        plt.xticks(rotation=45)
        plt.tight_layout()
        os.makedirs(in_output_visual_dir, exist_ok=True)
        plt.savefig(full_plot_path)
        plt.close()

        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)


def plot_monthly_tangential_average_displacement(in_sensor_data_df, in_output_visual_dir, in_plumbline_id, in_read_mode, in_year):
    """
    Generates a combined line and violin plot showing the monthly average and distribution of
    tangential displacement values (`DESLOCTANGABS`) for a specific sensor and year.

    Args:
        in_sensor_data_df (pd.DataFrame): DataFrame with 'MES' (month number), 'MONTH_NAME_EN', and 'DESLOCTANGABS'.
        in_output_visual_dir (str): Directory where the plot will be saved.
        in_plumbline_id (str): Identifier of the plumb line sensor.
        in_read_mode (str): Reading mode ('manual' or 'automatic').
        in_year (int): Year under analysis.

    Returns:
        None. Saves the generated plot to the specified output directory.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"REPORTING - DISPLACEMENTS"
    logger_module_info = f"MONTHLY AVG TANGENTIAL DISPLACEMENT - VISUAL"
    logger_starter_message = f"Generating monthly tangential displacement plot - Monthly Tangential Displacement - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings)"

    plot_title = f"Monthly Tangential Displacement (Average) - Sensor#{in_plumbline_id} ({in_year} {in_read_mode} readings)"
    plot_x_label = f"Month"
    plot_y_label = f"Displacement (Tangential - Average)"

    plot_filename = f"MonthlyTangentialAvg_{in_read_mode}_{in_year}_{in_plumbline_id}.png"
    full_plot_path = os.path.join(in_output_visual_dir, plot_filename)

    logger_success_message = f"Plot saved in: {full_plot_path}"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        plt.figure(figsize=(15, 10))

        monthly_avg_df = in_sensor_data_df.groupby(["MONTH_NAME_EN", "MES"])["DESLOCTANGABS"].mean().reset_index()

        monthly_avg_df = monthly_avg_df.sort_values(by="MES", ascending=True)

        plt.plot(monthly_avg_df["MONTH_NAME_EN"], monthly_avg_df["DESLOCTANGABS"], marker="o", linestyle="-",color="royalblue")

        sns.violinplot(data=in_sensor_data_df,
                       x="MONTH_NAME_EN",
                       y="DESLOCTANGABS",
                       inner="box",
                       palette=MONTHLY_COLOR_PALETTE)

        # Anotar os valores nas marcas
        for idx, val in enumerate(monthly_avg_df["DESLOCTANGABS"]):
            plt.text(idx, val, f"{val:.2f}", ha='center', va='bottom', fontsize=9)

        plt.title(plot_title)
        plt.xlabel(plot_x_label)
        plt.ylabel(plot_y_label)
        plt.xticks(rotation=45)
        plt.tight_layout()
        os.makedirs(in_output_visual_dir, exist_ok=True)
        plt.savefig(full_plot_path)
        plt.close()

        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)


def plot_radial_moving_average_displacement(in_sensor_data_df, in_output_visual_dir, in_plumbline_id, in_read_mode, in_year, in_instrument_configs) -> None:
    """
    Generates a time series plot showing raw and moving average of radial displacement (`DESLOCRADIALABS`)
    over time (daily resolution) for a given sensor and year. The rolling window is configured via the
    instrument configuration file.

    Args:
        in_sensor_data_df (pd.DataFrame): DataFrame containing 'DATA_DAY', 'DESLOCRADIALABS', and 'MONTH_NAME_EN'.
        in_output_visual_dir (str): Directory to save the generated plot.
        in_plumbline_id (str): Identifier of the plumb line sensor.
        in_read_mode (str): Reading mode ('manual' or 'automatic').
        in_year (int): Year under analysis.
        in_instrument_configs (dict): Dictionary containing the rolling window definition under
            in_instrument_configs["displacements"][in_read_mode]["DESLOCRADIALABS"]["rolling_window"].

    Returns:
        None. Saves the generated time series plot to the specified output directory.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"REPORTING - DISPLACEMENTS"
    logger_module_info = f"MONTHLY MOVING AVG RADIAL DISPLACEMENT - VISUAL"
    logger_starter_message = f"Generating monthly moving average radial displacement plot - Monthly Moving Average Radial Displacement - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings)"

    plot_x_label = f"Month"
    plot_y_label = f"Monthly Moving Average Radial Displacement"

    plot_filename = f"MonthlyRadialMovingAvg_{in_read_mode}_{in_year}_{in_plumbline_id}.png"
    full_plot_path = os.path.join(in_output_visual_dir, plot_filename)

    logger_success_message = f"Plot saved in: {full_plot_path}"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        plt.figure(figsize=(15, 10))

        DESLOCRADIALABS_config = in_instrument_configs["displacements"][in_read_mode]["DESLOCRADIALABS"]
        DESLOCRADIALABS_rolling_window = DESLOCRADIALABS_config["rolling_window"]

        plot_title = f"Monthly Moving Average Radial Displacement with rolling window {DESLOCRADIALABS_rolling_window} - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings)"
        
        # Sort by date
        sorted_df = in_sensor_data_df.sort_values("DATA_DAY").copy()

        # Apply rolling averages
        sorted_df["MA_DESLOCRADIALABS"] = sorted_df["DESLOCRADIALABS"].rolling(window=DESLOCRADIALABS_rolling_window,min_periods=1).mean()

        # Plot
        plt.plot(sorted_df["DATA_DAY"], sorted_df["DESLOCRADIALABS"], label="Radial (raw)", color="royalblue", alpha=0.4)

        plt.plot(sorted_df["DATA_DAY"], sorted_df["MA_DESLOCRADIALABS"], label=f"Radial MA ({DESLOCRADIALABS_rolling_window}d)", color="blue", linewidth=2)

        plt.xticks(ticks=sorted_df["DATA_DAY"][::max(1, len(sorted_df) // 12)],  # evitar overload
                   labels=sorted_df["MONTH_NAME_EN"][::max(1, len(sorted_df) // 12)],
                   rotation=45)

        plt.title(plot_title)
        plt.xlabel(plot_x_label)
        plt.ylabel(plot_y_label)
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        os.makedirs(in_output_visual_dir, exist_ok=True)
        plt.savefig(full_plot_path)
        plt.close()

        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)


def plot_tangential_moving_average_displacement(in_sensor_data_df, in_output_visual_dir, in_plumbline_id, in_read_mode, in_year, in_instrument_configs) -> None:
    """
    Generates a time series plot showing raw and moving average of tangential displacement (`DESLOCTANGABS`)
    over time (daily resolution) for a given sensor and year. The rolling window is configured via the
    instrument configuration file.

    Args:
        in_sensor_data_df (pd.DataFrame): DataFrame containing 'DATA_DAY', 'DESLOCTANGABS', and 'MONTH_NAME_EN'.
        in_output_visual_dir (str): Directory to save the generated plot.
        in_plumbline_id (str): Identifier of the plumb line sensor.
        in_read_mode (str): Reading mode ('manual' or 'automatic').
        in_year (int): Year under analysis.
        in_instrument_configs (dict): Dictionary containing the rolling window definition under
            in_instrument_configs["displacements"][in_read_mode]["DESLOCTANGABS"]["rolling_window"].

    Returns:
        None. Saves the generated time series plot to the specified output directory.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"REPORTING - DISPLACEMENTS"
    logger_module_info = f"MONTHLY MOVING AVG TANGENTIAL DISPLACEMENT - VISUAL"
    logger_starter_message = f"Generating monthly moving average tangential displacement plot - Monthly Moving Average Tangential Displacement - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings)"


    plot_x_label = f"Month"
    plot_y_label = f"Monthly Moving Average Tangential Displacement"

    plot_filename = f"MonthlyTangentialMovingAvg_{in_read_mode}_{in_year}_{in_plumbline_id}.png"
    full_plot_path = os.path.join(in_output_visual_dir, plot_filename)

    logger_success_message = f"Plot saved in: {full_plot_path}"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        plt.figure(figsize=(15, 10))

        deslocatangabs_config = in_instrument_configs["displacements"][in_read_mode]["DESLOCTANGABS"]
        deslocatangabs_rolling_window = deslocatangabs_config["rolling_window"]

        plot_title = f"Monthly Moving Average Tangential Displacement with rolling window {deslocatangabs_rolling_window} - Sensor#{in_plumbline_id} ({in_year}, {in_read_mode} readings)"

        # Sort by date
        sorted_df = in_sensor_data_df.sort_values("DATA_DAY").copy()

        # Apply rolling averages
        sorted_df["MA_DESLOCTANGABS"] = sorted_df["DESLOCTANGABS"].rolling(window=deslocatangabs_rolling_window,min_periods=1).mean()

        # Plot
        plt.plot(sorted_df["DATA_DAY"], sorted_df["DESLOCTANGABS"], label="Tangential (raw)", color="royalblue", alpha=0.4)

        plt.plot(sorted_df["DATA_DAY"], sorted_df["MA_DESLOCTANGABS"], label=f"Tangential MA ({deslocatangabs_rolling_window}d)", color="blue", linewidth=2)

        plt.xticks(ticks=sorted_df["DATA_DAY"][::max(1, len(sorted_df) // 12)],  # evitar overload
                   labels=sorted_df["MONTH_NAME_EN"][::max(1, len(sorted_df) // 12)],
                   rotation=45)

        plt.title(plot_title)
        plt.xlabel(plot_x_label)
        plt.ylabel(plot_y_label)
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        os.makedirs(in_output_visual_dir, exist_ok=True)
        plt.savefig(full_plot_path)
        plt.close()

        logger.info(generate_log_success_message(logger_module, logger_module_info, logger_success_message))

    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)
