""""
Utils scripts.
Some util functions are defined here to be used across the entire framework scripts.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import datetime
from typing import List
import json
import logging
import inspect
from configs.framework import MANUAL_CONFIGS_FILENAME, DQ_FRAMEWORK_LOG_FILENAME, PLUMBLINE_LOG_DIR


def welcome_function() -> None:
    """
    Prints a timestamped welcome message to the log.

    This function is typically used at the start of the DQ framework execution
    to signal the beginning of the run.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(format_date_logger() + f"\n\n\n\n***** STARTING Data Quality Framework - {timestamp} *****\n\n")


def end_function() -> None:
    """
    Prints a timestamped completion message to the log.

    Used to mark the end of the framework's execution.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(format_date_logger() + f"\n***** ENDED Quality Framework - {timestamp} *****\n")


def validate_directory_structure(directories: list) -> None:
    """
    Checks the existence of a list of directories and creates them if they do not exist.

    Args:
        directories (list): List of directory paths to validate or create.

    Returns:
        None. Creates missing directories and logs all operations.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"DQ UTILS"
    logger_module_info = f"VALIDATE DIRECTORY STRUCTURE"
    logger_starter_message = f"Validating directories"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        for dir_path in directories:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                logger_success_message = f"Directory created: {dir_path}"
                logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_success_message))
            else:
                logger_message = f"Directory exists: {dir_path}"
                logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_message))
    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)


def load_manual_config_file(in_instrument_name: str) -> dict:
    """
    Loads the manual configuration file (JSON) for a specific instrument.

    This function reads a centralized JSON configuration file and returns the
    subsection relevant to the specified instrument.

    Args:
        in_instrument_name (str): Name of the instrument (e.appendix_g., 'plumbline').

    Returns:
        dict: Dictionary containing the configuration parameters for the instrument.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"DQ UTILS"
    logger_module_info = f"VALIDATE DIRECTORY STRUCTURE"
    logger_starter_message = f"Loading manual configs for instrument {in_instrument_name}"
    logger_success_message = f"Manual configs successfully loaded for instrument {in_instrument_name}"

    try:
        with open(MANUAL_CONFIGS_FILENAME, "r", encoding="utf-8") as f:
            logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
            config_data = json.load(f)
            logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_success_message))
        return config_data.get(in_instrument_name, {})
    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)


def get_all_files_in_directory(in_input_data_dir: str, in_file_format: str) -> List[str]:
    """
    Retrieves all files within a specified directory that match a given file extension.

    This function scans the input directory and returns a list of all filenames ending with
    the provided file format (e.appendix_g., '.csv', '.txt'). It is a general-purpose utility used
    throughout the framework to locate input data files or output results such as DQ check
    reports and threshold validator outputs.

    Args:
        in_input_data_dir (str): Path to the directory to search for files.
        in_file_format (str): File extension or suffix to filter by (e.appendix_g., 'csv', 'txt').

    Returns:
        List[str]: List of filenames within the specified directory that match the given file format.

    Raises:
        SystemExit: If an exception occurs during directory access or listing.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"DQ UTILS"
    logger_module_info = f"VALIDATE DIRECTORY STRUCTURE"
    logger_starter_message = f"Loading all files in {in_input_data_dir}"
    logger_success_message = f"Files loaded successfully"

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        all_files_for_directory = [f for f in os.listdir(in_input_data_dir) if f.endswith(in_file_format)]
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_success_message))
        return all_files_for_directory
    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)


def setup_logger(in_log_dir: str) -> logging.Logger:
    """
    Initializes and returns a logger for the Data Quality Framework.

    The logger outputs messages to both the console (stdout) and a log file,
    and ensures no duplicate handlers are attached.

    Args:
        in_log_dir (str): Directory where the .log file should be stored.

    Returns:
        logging.Logger: Configured logger object.
    """
    logger = logging.getLogger("dq_framework_logger")
    logger.setLevel(logging.INFO)

    # Evitar handlers duplicados
    if not logger.handlers:
        # Handler para stdout
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Handler para ficheiro .log (se passado)
        if in_log_dir:
            full_log_dir = os.path.join(in_log_dir)
            os.makedirs(full_log_dir, exist_ok=True)
            log_file_path = os.path.join(full_log_dir, DQ_FRAMEWORK_LOG_FILENAME)
            file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            logger.info(f"[INFO]\t{format_date_logger()}\tLog file initialized at: {log_file_path}")
    return logger


def generate_log_starting_message(in_logger_module: str, in_logger_info_module: str, in_starting_message: str) -> str:
    """
    Generates a standardized 'STARTING' log message for a given module and function.

    Args:
        in_logger_module (str): Name of the higher-level module (e.appendix_g., 'DQ UTILS').
        in_logger_info_module (str): Name of the submodule or context.
        in_starting_message (str): Custom message describing the action.

    Returns:
        str: Formatted log message string.
    """
    logger_success_header = f"\t[{in_logger_module}]\t[{in_logger_info_module}]\t[STARTING]\t"
    logger_full_starter_message = f"\t{logger_success_header}\t(function: {inspect.currentframe().f_code.co_name})\t{in_starting_message})"
    return logger_full_starter_message


def generate_log_success_message(in_logger_module: str, in_logger_info_module: str, in_success_message: str) -> str:
    """
    Generates a standardized 'SUCCESS' log message for a given module and function.

    Args:
        in_logger_module (str): Name of the higher-level module.
        in_logger_info_module (str): Name of the submodule or context.
        in_success_message (str): Custom message describing the success.

    Returns:
        str: Formatted success log message.
    """
    logger_success_header = f"\t[{in_logger_module}]\t[{in_logger_info_module}]\t[SUCCESS]\t"
    logger_full_starter_message = f"\t{logger_success_header}\t(function: {inspect.currentframe().f_code.co_name})\t{in_success_message})"
    return logger_full_starter_message


def generate_log_error_message(in_logger_module: str, in_logger_info_module: str, in_exception) -> str:
    """
    Generates a standardized 'ERROR' log message for a given module and function.

    Args:
        in_logger_module (str): Name of the higher-level module.
        in_logger_info_module (str): Name of the submodule or context.
        in_exception (Exception): Exception object to include in the log.

    Returns:
        str: Formatted error log message with exception details.
    """
    logger_error_message = f"DQ Framework ended in error: "
    logger_error_header = f"\t[{in_logger_module}]\t[{in_logger_info_module}]\t[ERROR]\t"
    logger_full_error_message = f"\t{logger_error_header}\t(function: {inspect.currentframe().f_code.co_name})\t{logger_error_message}{str(in_exception)})"
    return logger_full_error_message


def format_date_logger():
    """
    Returns the current datetime in a formatted string for logging purposes.

    Format:
        YYYY-MM-DD HH:MM:SS

    Returns:
        str: Formatted current timestamp.
    """
    return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def create_directory(in_directory:str) -> None:
    """
    Creates the specified directory if it doesn't already exist.

    Uses `os.makedirs()` with `exist_ok=True` to avoid errors when the directory exists.

    Args:
        in_directory (str): Path to the directory to create.

    Returns:
        None. Logs success or failure of the creation process.
    """
    logger = setup_logger(PLUMBLINE_LOG_DIR)
    logger_module = f"DQ UTILS"
    logger_module_info = f"CREATE DIRECTORY"
    logger_starter_message = f"Creating directory {in_directory}"
    logger_success_message = f"{in_directory} successfully created "

    try:
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_starter_message))
        os.makedirs(in_directory, exist_ok=True)
        logger.info(generate_log_starting_message(logger_module, logger_module_info, logger_success_message))
    except Exception as e:
        logger.error(generate_log_error_message(logger_module, logger_module_info, e))
        sys.exit(1)
