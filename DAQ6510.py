import logging
import os
import sys
import typing
from enum import Enum
logger = logging.getLogger(__name__)

__version__ = '1.0.0'

class DAQ6510:
    user_manual = 'https://download.tek.com/manual/DAQ6510-900-01B_Aug_2019_User.pdf'
    reference_manual = 'https://download.tek.com/manual/DAQ6510-901-01_A_April_2018_Ref_DAQ6510-901-01A.pdf'
    functions_reference = reference_manual + '#page=117'
    
    def __init__(self) -> None:
        self.instrument = None
    
    def connect(self, resource_manager, resource_name, timeout, reset = False, clear = False) -> None:
        try:
            self.instrument = resource_manager.open_resource(resource_name)
            self.instrument_name = resource_name
            logger.debug(f'Connected to "{resource_name}"')
        except Exception as e:
            logger.error(f'Could not connect to "{resource_name}" due to {repr(e)}')
            raise e
        if reset:
            logger.debug(f'Resetting device...')
            self.send_command('reset()')
            logger.debug(f'Reset device.')
        if clear:
            logger.debug(f'Clearing device...')
            self.instrument.clear()
            logger.debug(f'Cleared device.')
        self.instrument.timeout = timeout
    
    def disconnect(self) -> True or Exception:
        logger.debug(f'Disconnecting from "{self.instrument_name}"...')
        try:
            self.instrument.close()
            logger.debug(f'Disconnected from "{self.instrument_name}"')
            return True
        except Exception as e:
            logger.error(f'An error occured while disconnecting from {self.instrument_name} due to {repr(e)}')
            raise e
    
    def query_command(self, command):
        logger.debug(f'Querying command: "{command}"...')
        try:
            query = self.instrument.query(command)
            logger.debug(f'Queried command.')
            return query
        except Exception as e:
            logger.error(f'An error occured while querying command due to {repr(e)}')
            raise e
    
    def send_command(self, command):
        try:
            self.instrument.write(command)
            logger.debug(f'Sent command "{command}".')
        except Exception as e:
            logger.error(f'An error occured while sending command "{command}" due to {repr(e)}')
    
    def beep(self, duration, frequency) -> None:
        logger.debug(f'Sending beep at {frequency}hz for {duration}s...')
        try:
            self.send_command(f'beeper.beep({duration}, {frequency})')
            logger.debug(f'Sent beep.')
        except Exception as e:
            logger.warning(f'An error occured while sending beep due to {repr(e)}')
    
    def reset(self) -> None:
        self.send_command('reset()')
    
    def id_query(self) -> query_command:
        return self.query_command('*IDN?')
    
    def LoadScriptFile(self, file_path) -> None:
        # This function opens the specified functions.lua file and trasfers its contents to the DMM's internal memory. All the functions defined in the file are callable by the controlling program. 
        with open(file_path, 'r') as f:
            contents = f.read()
            self.send_command('if loadfuncs ~= nil then script.delete(\'loadfuncs\') end')
            self.send_command(f'loadscript loadfuncs\n{contents}\nendscript')
            print(self.query_command('loadfuncs()'))
    
    def set_function(self, function: typing.Literal['DC_VOLTAGE', 'DC_CURRENT', 'RESISTANCE', 'ACV_FREQUENCY', 'AC_VOLTAGE', '4W_RESISTANCE', 'ACV_PERIOD', 'DC_CURRENT', 'DIODE', 'DCV_RATIO', 'AC_CURRENT', 'CAPACITANCE', 'DIGITIZE_CURRENT', 'TEMPERATURE', 'CONTINUITY', 'DIGITIZE_VOLTAGE']) -> None:
        self.send_command(f'dmm.measure.func = dmm.FUNC_{function}')
    
    def set_measurement_range(self, range) -> None:
        self.send_command(f'dmm.measure.range = {range}')
    
    def set_measure_NPLC(self, nplc) -> None:
        self.send_command(f'dmm.measure.nplc = {nplc}')
    
    def set_measurement_filter_count(self, count: int) -> None:
        self.send_command(f'dmm.measure.filter.count = {count}')
    
    def measure(self) -> query_command:
        return float(self.query_command('print(dmm.measure.read())')[:-1])

    def init(self) -> None:
        self.send_command('waitcomplete()')
        self.send_command('trigger.model.initiate()')
    
    def get_scan_status(self) -> query_command:
        return self.query_command('print(trigger.model.state())')
    
    def set_measurement_filter_state(self, state: typing.Literal['ON', 'OFF']) -> None:
        match state:
            case 'ON':
                self.send_command('dmm.measure.filter.enable = dmm.ON')
            case 'OFF':
                self.send_command('dmm.measure.filter.enable = dmm.OFF')
    
    def set_measurement_input_impedance(self, myZ: typing.Literal['Auto', '10M']) -> None:
        match myZ:
            case 'Auto':
                self.send_command('dmm.measure.inputimpedance = dmm.IMPEDANCE_AUTO')
            case '10M':
                self.send_command('dmm.measure.inputimpedance = dmm.IMPEDANCE_10M')
    
    def set_measurement_auto_zero(self, state: typing.Literal['ON', 'OFF']) -> None:
        match state:
            case 'OFF':
                self.send_command('dmm.measure.autozero.enable = dmm.OFF')
            case 'ON':
                self.send_command('dmm.measure.autozero.enable = dmm.ON')
    
    def set_measurement_filter_type(self, filter_type: typing.Literal['Repeating', 'Moving']) -> None:
        match filter_type:
            case 'Repeating':
                self.send_command('dmm.measure.filter.type = dmm.FILTER_REPEAT_AVG')
            case 'Moving':
                self.send_command('dmm.measure.filter.type = dmm.FILTER_MOVING_AVG')
    
    def set_function_Temperature(self, *args): # TODO Rework this
        # This function can be used to set up to three different measurement
        # function attributes, but they are expected to be in a certain
        # order....
        #   For simple front/rear terminal measurements:
        #       1. Transducer (TC/RTD/Thermistor)
        #       2. Transducer type
        #   For channel scan measurements:
        #       1. Channel string
        #       2. Transducer
        #       3. Transducer type
        if not (args):
            self.send_command('dmm.measure.func = dmm.FUNC_TEMPERATURE')
        else:
            if (type(args[0]) != str):
                self.send_command('dmm.measure.func = dmm.FUNC_TEMPERATURE')
                if(args):
                    xStr = 'dmm.measure.transducer'
                    if(args[0] == self.Transducer.TC):
                       xStr2 = 'dmm.TRANS_THERMOCOUPLE'
                    elif(args[0] == self.Transducer.RTD4):
                       xStr2 = 'dmm.TRANS_FOURRTD'
                    elif(args[0] == self.Transducer.RTD3):
                       xStr2 = 'dmm.TRANS_THREERTD'
                    elif(args[0] == self.Transducer.THERM):
                       xStr2 = 'dmm.TRANS_THERMISTOR'
                    sndBuffer = '{} = {}'.format(xStr, xStr2)
                    self.send_command(sndBuffer)
                if(len(args) > 1):
                    if(args[0] == self.Transducer.TC):
                        xStr = 'dmm.measure.thermocouple'
                        if(args[1] == self.TCType.K):
                           xType = 'dmm.THERMOCOUPLE_K'
                        elif(args[1] == self.TCType.J):
                           xType = 'dmm.THERMOCOUPLE_J'
                        elif(args[1] == self.TCType.N):
                           xType = 'dmm.THERMOCOUPLE_N' 
                        sndBuffer = '{} = {}'.format(xStr, xType)
                        self.send_command(sndBuffer)
                    elif((args[0] == self.Transducer.RTD4) or (args[1] == self.Transducer.RTD3)):
                        if(args[0] == self.Transducer.RTD4):
                            xStr = 'dmm.measure.fourrtd'
                        if(args[0] == self.Transducer.RTD3):
                            xStr = 'dmm.measure.threertd'

                        if(args[1] == self.RTDType.PT100):
                           rtdType = 'dmm.RTD_PT100'
                        elif(args[1] == self.RTDType.PT385):
                           rtdType = 'dmm.RTD_PT385'
                        elif(args[1] == self.RTDType.PT3916):
                           rtdType = 'dmm.RTD_PT3916'
                        elif(args[1] == self.RTDType.D100):
                           rtdType = 'dmm.RTD_D100'
                        elif(args[1] == self.RTDType.F100):
                           rtdType = 'dmm.RTD_F100'
                        elif(args[1] == self.RTDType.USER):
                           rtdType = 'dmm.RTD_USER'
                           
                        sndBuffer = '{} = {}'.format(xStr, rtdType)
                        self.send_command(sndBuffer)
                    elif(args[0] == self.Transducer.THERM):
                        xStr = 'dmm.measure.thermistor'
                        if(args[1] == self.ThermType.TH2252):
                           thrmType = 'dmm.THERM_2252'
                        elif(args[1] == self.ThermType.TH5K):
                           thrmType = 'dmm.THERM_5000'
                        elif(args[1] == self.ThermType.TH10K):
                           thrmType = 'dmm.THERM_10000'
                        sndBuffer = '{} = {}'.format(xStr, thrmType)
                        self.send_command(sndBuffer)
            else:
                setStr = 'channel.setdmm(\'{}\', '.format(args[0])
                self.send_command('{}dmm.ATTR_MEAS_FUNCTION, dmm.FUNC_TEMPERATURE)'.format(setStr))
                if(len(args) > 1):
                    if(args[1] == self.Transducer.TC):
                       xStr = 'dmm.TRANS_THERMOCOUPLE'
                       xStr2 = 'dmm.ATTR_MEAS_THERMOCOUPLE'
                    elif(args[1] == self.Transducer.RTD4):
                       xStr = 'dmm.TRANS_FOURRTD'
                       xStr2 = 'dmm.ATTR_MEAS_FOUR_RTD'
                    elif(args[1] == self.Transducer.RTD3):
                       xStr = 'dmm.TRANS_THREERTD'
                       xStr2 = 'dmm.ATTR_MEAS_THREE_RTD'
                    elif(args[1] == self.Transducer.THERM):
                       xStr = 'dmm.TRANS_THERMISTOR'
                       xStr2 = 'dmm.ATTR_MEAS_THERMISTOR'
                    sndBuffer = '{}dmm.ATTR_MEAS_TRANSDUCER, {})'.format(setStr, xStr)
                    self.send_command(sndBuffer)
                if(len(args) > 2):
                    if(args[1] == self.Transducer.TC):
                        if(args[2] == self.TCType.K):
                           xType = 'dmm.THERMOCOUPLE_K'
                        elif(args[2] == self.TCType.J):
                           xType = 'dmm.THERMOCOUPLE_J'
                        elif(args[2] == self.TCType.N):
                           xType = 'dmm.THERMOCOUPLE_N' 
                        #print('{}dmm.ATTR_MEAS_THERMOCOUPLE, {})'.format(setStr, xType))
                        sndBuffer = '{}dmm.ATTR_MEAS_THERMOCOUPLE, {})'.format(setStr, xType)
                        self.send_command(sndBuffer)
                    elif((args[1] == self.Transducer.RTD4) or (args[1] == self.Transducer.RTD3)):
                        if(args[2] == self.RTDType.PT100):
                           rtdType = 'dmm.RTD_PT100'
                        elif(args[2] == self.RTDType.PT385):
                           rtdType = 'dmm.RTD_PT385'
                        elif(args[2] == self.RTDType.PT3916):
                           rtdType = 'dmm.RTD_PT3916'
                        elif(args[2] == self.RTDType.D100):
                           rtdType = 'dmm.RTD_F100'
                        elif(args[2] == self.RTDType.F100):
                           rtdType = 'dmm.RTD_D100'
                        elif(args[2] == self.RTDType.USER):
                           rtdType = 'dmm.RTD_USER'
                        sndBuffer = '{}{}, {})'.format(setStr, xStr2, rtdType)
                        self.send_command(sndBuffer)
                    if(args[1] == self.Transducer.THERM):
                        if(args[2] == self.ThermType.TH2252):
                           thrmType = 'dmm.THERM_2252'
                        elif(args[2] == self.ThermType.TH5K):
                           thrmType = 'dmm.THERM_5000'
                        elif(args[2] == self.ThermType.TH10K):
                           thrmType = 'dmm.THERM_10000'
                        sndBuffer = '{}{}, {})'.format(setStr, xStr2, thrmType)
                        self.send_command(sndBuffer)
        return
    
    def set_scan_BasicAttributes(self, *args): # TODO Rework this
        self.send_command('scan.create(\'{}\')'.format(args[0]))
        
        # Set the scan count
        if(len(args) > 1):
            self.send_command('scan.scancount = {}'.format(args[1]))
        
        # Set the time between scans
        if(len(args) > 2):
            self.send_command('scan.scaninterval = {}'.format(args[2]))
        return
    
    def GetScan_Data(self, dataCount, startIndex, endIndex): # TODO Rework this
        #charCnt = 24 * dataCount
        accumCnt = int(self.query_command('print(defbuffer1.n)')[0:-1])
        while(accumCnt < endIndex):
            accumCnt = int(self.query_command('print(defbuffer1.n)')[0:-1])
        rcvBuffer = self.query_command('printbuffer({}, {}, defbuffer1)'.format(startIndex, endIndex))[0:-1]
        return rcvBuffer
    
    class Transducer(Enum): # TODO Rework this
        TC = 0
        RTD4 = 1
        RTD3 = 2
        THERM = 3
    
    class TCType(Enum): # TODO Rework this
        K = 0
        J = 1
        N = 2
    
    class RTDType(Enum): # TODO Rework this
        PT100 = 0
        PT385 = 1
        PT3916 = 2
        D100 = 3
        F100 = 4
        USER = 5
    
    class ThermType(Enum): # TODO Rework this
        TH2252 = 0
        TH5K = 1
        TH10K = 2

def play_megalovania(DAQ):
    DAQ.beep(duration=130/1000, frequency=294)
    DAQ.beep(duration=261/1000, frequency=587)
    DAQ.beep(duration=391/1000, frequency=440)
    DAQ.beep(duration=261/1000, frequency=415)
    DAQ.beep(duration=261/1000, frequency=392)
    DAQ.beep(duration=261/1000, frequency=349)
    DAQ.beep(duration=130/1000, frequency=294)
    DAQ.beep(duration=130/1000, frequency=349)
    DAQ.beep(duration=130/1000, frequency=392)

def main() -> None:
    pass

if __name__ == '__main__':
    if os.path.exists('latest.log'): open('latest.log', 'w').close() # Clear latest.log if it exists
    
    # Set up logger
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
    
    try:
        main()
    except Exception as e:
        logger.fatal(f'The script could no longer continue due to {repr(e)}.')
        exit(1)