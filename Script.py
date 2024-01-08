import logging
import os
import pyvisa
import sys
import time
from DAQ6510 import DAQ6510
from EngineeringNotation import EngineeringNotation
logger = logging.getLogger(__name__)

__version__ = '1.0.0'

def countdown(timer: int) -> None:
    max_str_length = 0
    
    while timer > 0:
        message = f'Measuring value1 in {timer}'
        max_str_length = max(len(message), max_str_length)
        while len(message) != max_str_length:
            message = f'{message} '
        print(message, end='\r')
        timer -= 1
        time.sleep(1)

def main() -> None:
    ip = '10.125.0.73'
    intrument_string = f'TCPIPn::{ip}::inst0::INSTR'
    timeout = 5000
    
    rm = pyvisa.ResourceManager()
    global DAQ
    DAQ = DAQ6510()
    DAQ.connect(rm, intrument_string, timeout)
    
    DAQ.set_measurement_filter_state('ON')
    DAQ.set_measurement_filter_count(20)
    
    DAQ.set_function('RESISTANCE')
    
    countdown(10)
    logger.debug(f'Measuring value1...')
    measure1 = DAQ.measure()
    logger.debug(f'{measure1 = }')
    logger.info(f'Value 1: {EngineeringNotation(measure1).get_si_form("Ω")}')
    
    countdown(10)
    logger.debug(f'Measuring value2...')
    measure2 = DAQ.measure()
    logger.debug(f'{measure2 = }')
    logger.info(f'Value 2: {EngineeringNotation(measure2).get_si_form("Ω")}')
    
    percent_difference = (abs(measure1-measure2)) / measure1 * 100
    logger.debug(f'{percent_difference = }')
    logger.info(f'Percent Difference: {round(percent_difference, 2)}%')

if __name__ == '__main__':
    # Clear latest.log if it exists
    if os.path.exists('latest.log'):
        open('latest.log', 'w').close()
    
    # File handler
    file_handler = logging.FileHandler('latest.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
    logger.addHandler(console_handler)
    
    # Set the overall logging level
    logger.setLevel(logging.INFO)
    
    # Set logging level for module
    logging.getLogger('pyvisa').setLevel(logging.WARNING)
    
    try:
        main()
    except Exception as e:
        logger.exception(f'The script could no longer continue due to {repr(e)}.')
        exit(1)