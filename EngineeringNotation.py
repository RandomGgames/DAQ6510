import math

__version__ = '1.0.1'

class EngineeringNotation():
    si_prefixes = {
        -60: 'My',
        -57: 'Mr',
        -54: 'My',
        -51: 'Mz',
        -48: 'Ma',
        -45: 'Mf',
        -42: 'Mp',
        -39: 'Mn',
        -36: 'Mμ',
        -33: 'Mm',
        -30: 'y',
        -27: 'r',
        -24: 'y',
        -21: 'z',
        -18: 'a',
        -15: 'f',
        -12: 'p',
        -9: 'n',
        -6: 'μ',
        -3: 'm',
        0: None,
        3: 'K',
        6: 'M',
        9: 'G',
        12: 'T',
        15: 'P',
        18: 'E',
        21: 'Z',
        24: 'Y',
        27: 'R',
        30: 'Q',
        33: 'Mk',
        36: 'MM',
        39: 'MG',
        42: 'MT',
        45: 'MP',
        48: 'ME',
        51: 'MZ',
        54: 'MY',
        57: 'MR',
        60: 'MQ',
    }
    
    def __init__(self, number, digits_to_round_to: int = 3):
        self.value = round(number, 7)
        self.engineering_exponent = self._get_engineering_exponent()
        self.mantissa = round(self.value / 10 ** self.engineering_exponent, digits_to_round_to)
        self.prefix = EngineeringNotation.si_prefixes.get(self.engineering_exponent)
    
    def _get_engineering_exponent(self):
        if self.value == 0:
            return 0
        exponent = int(math.log10(abs(self.value)))
        while exponent % 3 != 0:
            exponent -= 1
        return exponent
    
    def get_si_form(self, unit: str = ''):
        return f'{self.mantissa} {self.prefix}{unit}' if self.prefix is not None else f'{self.get_engieering_form()} {unit}'
    
    def get_engieering_form(self, unit: str = ''):
        return f'{self.mantissa}E{self.engineering_exponent} {unit}'
