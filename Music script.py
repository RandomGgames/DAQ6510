import logging
import pyvisa
import sys
import time
from DAQ6510 import DAQ6510
logger = logging.getLogger(__name__)

def play_rick_roll_short():
    global DAQ
    DAQ.beep(duration=125/1000, frequency=440)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=125/1000, frequency=587)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=375/1000, frequency=740)
    DAQ.beep(duration=375/1000, frequency=740)
    DAQ.beep(duration=750/1000, frequency=659)

def play_rick_roll():
    global DAQ
    DAQ.beep(duration=125/1000, frequency=440)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=125/1000, frequency=587)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=375/1000, frequency=740)
    DAQ.beep(duration=375/1000, frequency=740)
    DAQ.beep(duration=750/1000, frequency=659)
    DAQ.beep(duration=125/1000, frequency=440)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=125/1000, frequency=587)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=375/1000, frequency=659)
    DAQ.beep(duration=375/1000, frequency=659)
    DAQ.beep(duration=375/1000, frequency=587)
    DAQ.beep(duration=125/1000, frequency=554)
    DAQ.beep(duration=375/1000, frequency=494)
    DAQ.beep(duration=125/1000, frequency=440)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=125/1000, frequency=587)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=250/1000, frequency=440)
    DAQ.beep(duration=250/1000, frequency=440)
    DAQ.beep(duration=250/1000, frequency=440)
    DAQ.beep(duration=500/1000, frequency=659)
    DAQ.beep(duration=1000/1000, frequency=587)
    DAQ.beep(duration=125/1000, frequency=440)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=125/1000, frequency=587)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=375/1000, frequency=740)
    DAQ.beep(duration=375/1000, frequency=740)
    DAQ.beep(duration=750/1000, frequency=659)
    DAQ.beep(duration=125/1000, frequency=440)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=125/1000, frequency=587)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=500/1000, frequency=880)
    DAQ.beep(duration=250/1000, frequency=554)
    DAQ.beep(duration=375/1000, frequency=587)
    DAQ.beep(duration=125/1000, frequency=554)
    DAQ.beep(duration=250/1000, frequency=494)
    DAQ.beep(duration=125/1000, frequency=440)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=125/1000, frequency=587)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=500/1000, frequency=587)
    DAQ.beep(duration=250/1000, frequency=659)
    DAQ.beep(duration=375/1000, frequency=554)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=500/1000, frequency=440)
    DAQ.beep(duration=250/1000, frequency=440)
    DAQ.beep(duration=500/1000, frequency=659)
    DAQ.beep(duration=1000/1000, frequency=587)
    DAQ.beep(duration=250/1000, frequency=494)
    DAQ.beep(duration=250/1000, frequency=554)
    DAQ.beep(duration=250/1000, frequency=587)
    DAQ.beep(duration=250/1000, frequency=494)
    DAQ.beep(duration=250/1000, frequency=659)
    DAQ.beep(duration=250/1000, frequency=740)
    DAQ.beep(duration=750/1000, frequency=659)
    DAQ.beep(duration=125/1000, frequency=440)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=125/1000, frequency=587)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=375/1000, frequency=740)
    DAQ.beep(duration=375/1000, frequency=740)
    DAQ.beep(duration=750/1000, frequency=659)
    DAQ.beep(duration=125/1000, frequency=440)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=125/1000, frequency=587)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=375/1000, frequency=659)
    DAQ.beep(duration=375/1000, frequency=659)
    DAQ.beep(duration=375/1000, frequency=587)
    DAQ.beep(duration=125/1000, frequency=554)
    DAQ.beep(duration=375/1000, frequency=494)
    DAQ.beep(duration=125/1000, frequency=440)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=125/1000, frequency=587)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=500/1000, frequency=587)
    DAQ.beep(duration=250/1000, frequency=659)
    DAQ.beep(duration=375/1000, frequency=554)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=250/1000, frequency=440)
    DAQ.beep(duration=250/1000, frequency=440)
    DAQ.beep(duration=250/1000, frequency=440)
    DAQ.beep(duration=500/1000, frequency=659)
    DAQ.beep(duration=1000/1000, frequency=587)
    DAQ.beep(duration=125/1000, frequency=440)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=125/1000, frequency=587)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=375/1000, frequency=740)
    DAQ.beep(duration=375/1000, frequency=740)
    DAQ.beep(duration=750/1000, frequency=659)
    DAQ.beep(duration=125/1000, frequency=440)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=125/1000, frequency=587)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=500/1000, frequency=880)
    DAQ.beep(duration=250/1000, frequency=554)
    DAQ.beep(duration=375/1000, frequency=587)
    DAQ.beep(duration=125/1000, frequency=554)
    DAQ.beep(duration=250/1000, frequency=494)
    DAQ.beep(duration=125/1000, frequency=440)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=125/1000, frequency=587)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=500/1000, frequency=587)
    DAQ.beep(duration=250/1000, frequency=659)
    DAQ.beep(duration=375/1000, frequency=554)
    DAQ.beep(duration=125/1000, frequency=494)
    DAQ.beep(duration=500/1000, frequency=440)
    DAQ.beep(duration=250/1000, frequency=440)
    DAQ.beep(duration=500/1000, frequency=659)
    DAQ.beep(duration=1000/1000, frequency=587)

def play_megalovania():
    global DAQ
    DAQ.beep(duration=130/1000, frequency=294)
    DAQ.beep(duration=261/1000, frequency=587)
    DAQ.beep(duration=391/1000, frequency=440)
    DAQ.beep(duration=261/1000, frequency=415)
    DAQ.beep(duration=261/1000, frequency=392)
    DAQ.beep(duration=261/1000, frequency=349)
    DAQ.beep(duration=130/1000, frequency=294)
    DAQ.beep(duration=130/1000, frequency=349)
    DAQ.beep(duration=130/1000, frequency=392)

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
    
    #play_megalovania()
    play_rick_roll_short()

if __name__ == '__main__':
    #if os.path.exists('latest.log'): open('latest.log', 'w').close() # Clear latest.log if it exists
    logging.basicConfig(
        level = logging.INFO,
        format = '%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        encoding = 'utf-8',
        handlers = [
            logging.FileHandler('latest.log', encoding = 'utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.getLogger('pyvisa').setLevel(logging.WARNING)
    
    try:
        main()
    except Exception as e:
        logger.exception(f'The script could no longer continue due to {repr(e)}.')
        exit(1)