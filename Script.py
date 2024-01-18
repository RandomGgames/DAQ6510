import keyboard
import logging
import os
import pyvisa
import sys
import time
from DAQ6510 import DAQ6510
from EngineeringNotation import EngineeringNotation
logger = logging.getLogger()

__version__ = '1.0.1'

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

i = 0
measurements = 2
measure1 = list(None for _ in range(measurements))
measure2 = list(None for _ in range(measurements))

units = None

def keyboard_event(event):
    match event.event_type:
        case 'down':
            match event.is_keypad:
                case True:
                    match event.name:
                        case '+':
                            global i
                            global measure1
                            global measure2
                            global units
                            
                            if i < measurements:
                                measure1[i] = DAQ.measure()
                                DAQ.beep(0.1, 300)
                                logger.info(f'measure1[{i}] = {EngineeringNotation(measure1[i]).get_si_form(units)}')
                                i += 1
                            elif i >= measurements and i < measurements * 2:
                                j = i - measurements
                                measure2[j] = DAQ.measure()
                                DAQ.beep(0.1, 300)
                                logger.info(f'measure2[{j}] = {EngineeringNotation(measure2[j]).get_si_form(units)}')
                                i += 1
                            
                            if i == measurements * 2:
                                for k in range(measurements):
                                    percent_difference = ( (abs(measure1[k]-measure2[k])) / measure1[k] ) * 100
                                    logger.debug(f'{percent_difference = }')
                                    logger.info(f'measure1[{k}] = {EngineeringNotation(measure1[k]).get_si_form(units)}, measure2[{k}] = {EngineeringNotation(measure2[k]).get_si_form(units)}, %Diff: {round(percent_difference, 2)}%')
                                measure1 = list(None for _ in range(measurements))
                                measure2 = list(None for _ in range(measurements))
                                i = 0
                
                case False:
                    match event.name:
                        case 'r':
                            DAQ.set_function('RESISTANCE')
                            logger.info(f'Set function to Resistance.')
                            units = 'Ω'
                        
                        case 'v':
                            DAQ.set_function('DC_VOLTAGE')
                            logger.info(f'Set function to DC-Voltage.')
                            units = 'V'

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
    
    keyboard.hook(keyboard_event)
    keyboard.wait()

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
    logger.setLevel(logging.DEBUG)
    
    # Set logging level for module
    logging.getLogger('pyvisa').setLevel(logging.WARNING)
    
    try:
        main()
    except Exception as e:
        logger.exception(f'The script could no longer continue due to {repr(e)}.')
        exit(1)