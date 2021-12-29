class frequency_range():
    def __init__(self,frequency1,frequency2):
        self.frequency1 = float(frequency1)
        if(frequency2 != "infinity"):
            self.frequency2 = float(frequency2)
        else:
            self.frequency2 = frequency2
        self.frequency = None
        self.pattern = None

    def __within_frequency__(self,frequency):
        if self.frequency2 == "infinity":
            return frequency >= self.frequency1
        else:
            return frequency >= self.frequency1 and frequency <= self.frequency2

    def __add_periodicity__(self,frequency,pattern):
        self.frequency = float(frequency)
        self.pattern = pattern

    def __update_frequency_range__(self):
        if self.pattern != None :
            frequency_difference = self.frequency2 - self.frequency1
            if self.pattern == "add":
                self.frequency1 = self.frequency1 + self.frequency
            self.frequency2 = self.frequency1 + frequency_difference

    def __comparison__(self,frequency_range):
        if self.frequency2 != "infinity":
            if frequency_range.frequency1 >self.frequency2:
                return False
            elif frequency_range.frequency1 <= self.frequency2:
                return True
        else:
            return True