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


MONTHLY_COLOR_PALETTE = [
    "#1f77b4",  # Janeiro — azul escuro (inverno)
    "#3b8fc4",  # Fevereiro — azul médio (inverno)
    "#5ca0c8",  # Março — azul claro (início primavera)
    "#f2c14e",  # Abril — amarelo dourado (primavera)
    "#f4a261",  # Maio — laranja suave (primavera)
    "#e76f51",  # Junho — laranja vivo (verão)
    "#ff5733",  # Julho — vermelho-alaranjado (verão)
    "#ff8c42",  # Agosto — laranja queimado (verão)
    "#f4a261",  # Setembro — laranja suave (outono)
    "#9e5f63",  # Outubro — vermelho ameno (outono)
    "#5c6e91",  # Novembro — azul acinzentado (outono/inverno)
    "#264653",  # Dezembro — azul petróleo (inverno)
]

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
DQ_FRAMEWORK_AVAILABLE_DIMENSION = ["Completeness", "Timeliness"]
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
PLUMBLINE_DISPLACEMENTS_OUTPUT_DIR = os.path.join(PLUMBLINE_TIMESTAMP_OUTPUT_DIR, "displacements_visuals")
PLUMBLINE_OBSERVABILITY_DIR = os.path.join(PLUMBLINE_TIMESTAMP_OUTPUT_DIR, "observability")
PLUMBLINE_LOG_DIR = os.path.join(PLUMBLINE_TIMESTAMP_OUTPUT_DIR, "log")
PLUMBLINE_RUN_MODES = ["automatic", "manual"]




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


