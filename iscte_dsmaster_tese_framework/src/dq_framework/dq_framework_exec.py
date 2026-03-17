# =============================================================================
# SCRIPT: dq_framework_main.py
# PROJECT: Data Quality Framework for Sensor-Based Structural Health Monitoring
# AUTHOR: Diogo Fernandes
# DATE: [INSERIR DATA AQUI]
#
# DESCRIPTION:
#   Main execution script for running the Data Quality Framework.
#   Supports sensor data quality assessment using predefined checks and thresholds.
#   Currently implemented for 'plumbline' instruments in 'joint' mode.
#
# FUNCTIONALITY:
#   - Parses command-line arguments for instrument, mode, and file list
#   - Validates environment and directory structure
#   - Loads configuration and dispatches to instrument-specific logic
#   - Applies DQ checks and threshold validators
#   - Saves results to structured outputs and generates visualizations
#
# USAGE EXAMPLE:
#   python dq_framework_main.py --instrument plumbline --mode joint --file_list all
#   python dq_framework_main.py --instrument plumbline --mode joint --file_list 49350.txt 49351.txt
#
# =============================================================================
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import argparse
from utils.dq_utils import setup_logger, format_date_logger
# CONFIG inputs imports
from configs.framework import FRAMEWORK_AVAILABLE_INSTRUMENTS, PLUMBLINE_INSTRUMENT_NAME, PLUMBLINE_LOG_DIR
from src.dq_framework.plumbline.plumbline_exec import run_plumbline


def run_data_quality_framework() -> None:
    """
    Entry point for executing the Data Quality Framework via command-line interface (CLI).

    This function parses CLI arguments, validates the selected instrument and execution mode,
    and delegates the execution to the corresponding instrument-specific function (e.appendix_g., `run_plumbline`).

    Expected CLI arguments:
        --instrument : Instrument name to evaluate (e.appendix_g., 'plumbline').
        --mode       : Execution mode. Currently only 'joint' is supported.
        --file_list  : List of filenames to process (e.appendix_g., '49350.txt'), or 'all' to evaluate all files.

    Example usage:
        python dq_framework_main.py --instrument plumbline --mode joint --file_list 49350.txt 49351.txt

    Output:
        Executes the framework logic for the specified instrument and mode.
        Logs the execution metadata and progress throughout the process.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--instrument", required=True, choices= FRAMEWORK_AVAILABLE_INSTRUMENTS, help=f"Available instruments: {FRAMEWORK_AVAILABLE_INSTRUMENTS}")
    parser.add_argument("--mode", required=True, choices=["manual", "automatic", "all"], help="Acquisition mode: 'automatic' (RA) or 'manual' (RM)")
    parser.add_argument("--id_list", nargs="+", required=True, help="List of IDs to process (e.appendix_g., 49352 49353) or 'all'")
    parser.add_argument("--year_list", nargs="+", required=True, help="List of years to process (e.appendix_g., 2025 2024) or 'all'")

    args = parser.parse_args()
    arg_instrument = args.instrument
    arg_mode = args.mode
    arg_id_list = args.id_list
    arg_year_list = args.year_list



    if arg_instrument in FRAMEWORK_AVAILABLE_INSTRUMENTS:
        if arg_instrument == PLUMBLINE_INSTRUMENT_NAME:
            logger = setup_logger(PLUMBLINE_LOG_DIR)
            logger.info("\n\n\n\n\n[OK]\t[FRAMEWORK INSTRUMENT EVALUATION]\t" + format_date_logger() + f"\tArguments used for this run: \nInstrument: {arg_instrument}\nMode: {arg_mode}\nIDs List: {arg_id_list}\nYear List: {arg_year_list}")
            run_plumbline(arg_mode, arg_id_list, arg_year_list)


"""
=============================================================================
Entry point for the script execution.

When this script is executed directly (not imported as a module), it will:
  - Optionally clear pre-defined output directories (commented out by default).
  - Call the main entrypoint function `run_data_quality_framework()` which:
      - Parses CLI arguments
      - Dispatches execution based on instrument and mode
      - Runs the full data quality workflow

Example:
  python dq_framework_main.py --instrument plumbline --mode joint --file_list all
=============================================================================
"""
if __name__ == "__main__":
    #folders_to_clear = [PLUMBLINE_MAIN_OUTPUT_DIR]
    #folders_to_clear = [OUTPUT_DIR]
    #clear_directories_content(folders_to_clear)

    run_data_quality_framework()

