class manual_modification():

    def __init__(self,starting_frequency, last_frequency, impulsion_modification):
        self.name = "transfer_function"
        self.starting_frequency = starting_frequency
        self.last_frequency = last_frequency
        self.impulsion_modification = impulsion_modification

    def __plug__(self, manual_modification):
        self.starting_frequency = manual_modification.starting_frequency
        self.last_frequency = manual_modification.last_frequency
        self.impulsion_modification = manual_modification.impulsion_modification
        self.phase_modification = manual_modification.phase_modification

    def __modify_starting_frequency__(self, starting_frequency):
        self.starting_frequency = starting_frequency

    def __modify_last_frequency__(self, last_frequency):
        self.last_frequency = last_frequency

    def __modify_impulsion_modification__(self, impulsion_modification):
        self.impulsion_modification = impulsion_modification






