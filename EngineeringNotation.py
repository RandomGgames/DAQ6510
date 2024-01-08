import math

__version__ = '1.0.2'

class EngineeringNotation():
    si_prefixes = {
        -60: 'My', # *10^-60
        -57: 'Mr', # *10^-57
        -54: 'My', # *10^-54
        -51: 'Mz', # *10^-51
        -48: 'Ma', # *10^-48
        -45: 'Mf', # *10^-45
        -42: 'Mp', # *10^-42
        -39: 'Mn', # *10^-39
        -36: 'Mμ', # *10^-36
        -33: 'Mm', # *10^-33
        -30: 'y', # *10^-30
        -27: 'r', # *10^-27
        -24: 'y', # *10^-24
        -21: 'z', # *10^-21
        -18: 'a', # *10^-18
        -15: 'f', # *10^-15
        -12: 'p', # *10^-12
        -9: 'n', # *10^-9
        -6: 'μ', # *10^-6
        -3: 'm', # *10^-3
        0: None, # *10^0
        3: 'K', # *10^3
        6: 'M', # *10^6
        9: 'G', # *10^9
        12: 'T', # *10^12
        15: 'P', # *10^15
        18: 'E', # *10^18
        21: 'Z', # *10^21
        24: 'Y', # *10^24
        27: 'R', # *10^27
        30: 'Q', # *10^30
        33: 'Mk', # *10^33
        36: 'MM', # *10^36
        39: 'MG', # *10^39
        42: 'MT', # *10^42
        45: 'MP', # *10^45
        48: 'ME', # *10^48
        51: 'MZ', # *10^51
        54: 'MY', # *10^54
        57: 'MR', # *10^57
        60: 'MQ', # *10^60
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