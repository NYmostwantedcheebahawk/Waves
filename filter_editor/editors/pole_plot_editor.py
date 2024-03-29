class pole_plot_editor():

    def __init__(self):
        self.type = "filter_editor_bode"

    def plug(self, editor):
        self.data_in = editor.data_in
        self.data_out = editor.data_out
        self.vout = editor.vout
        self.freq = editor.freq
        self.freq_complete = editor.freq_complete

        self.vin = editor.vin
        self.vin_positive = editor.vin_positive
        self.vout_positive = editor.vout_positive

    def plug2(self, data_in, data_out, fc1, fc2, type):
        self.data_in = data_in
        fourier_no_complex = [0] * len(self.data_in[0].fourier_complete)
        for x in range(0, len(self.data_in[0].fourier_complete)):
            fourier_no_complex[x] = self.data_in[0].fourier_complete[x].real
        self.data_out = data_out
        self.vout = data_out[0].fourier_no_complexe
        self.freq = data_out[0].freq
        self.freq_complete = data_out[0].freq_complete

        self.vin = fourier_no_complex
        self.vin_positive = data_in[0].fourier_no_complexe_positive
        self.vout_positive = data_out[0].fourier_no_complexe_positive
        self.fc1 = fc1
        self.fc2 = fc2
        self.type = type

        self.phaseShift = 0;

    def get_data_for_graphic(self):

        self.impulsion_db_positive = [0]*len(self.vin_positive)
        self.impulsion_db = [0]*len(self.vin)
        answer = 0
        for x in range(0,len(self.vin)):
            if(self.vout[x]/self.vin[x] < 0.0000000000001):
                answer = 0.00000000000001
            else:
                answer = self.vout[x] / self.vin[x]

            if(self.freq_complete[x] >= 0):
                self.impulsion_db_positive[x] = 20 * math.log(answer)
                self.impulsion_db[x] = 20 * math.log(answer)
            else:
                self.impulsion_db[x] = 20* math.log(answer)

    def modify_response(self, first, last, attenuation, type):

        if(type == "passe bas"):
            for x in range(len(self.freq_complete)):
                if(self.freq_complete[x] < 0):
                    if(self.freq_complete[x] <= -1* float(first)):
                        self.vout[x] = math.pow(10,(float(attenuation)/20)) *self.vin[x]
                if(self.freq_complete[x] >=0):
                    if(self.freq_complete[x] >= float(first)):
                        self.vout[x] = math.pow(10, (float(attenuation) / 20) )* self.vin[x]

        if(type == "passe haut"):
            for x in range(len(self.freq_complete)):
                if(self.freq_complete[x] < 0):
                    if(self.freq_complete[x] >= -1* float(first)):
                        self.vout[x] = math.pow(10,(float(attenuation)/20)) *self.vin[x]
                if(self.freq_complete[x] >=0):
                    if(self.freq_complete[x] <= float(first)):
                        self.vout[x] = math.pow(10, (float(attenuation) / 20) )* self.vin[x]
        if(type == "passe bande"):
            for x in range(len(self.freq_complete)):
                if (self.freq_complete[x] < 0):
                    if (self.freq_complete[x] > -1 * self.cut_off* 2):
                        self.vout[x] = math.pow(10, (float(attenuation) / 20)) * self.vin[x]
                    elif (self.freq_complete[x]< -1 * self.cut_off2* 2):
                        self.vout[x] = math.pow(10, (float(attenuation) / 20)) * self.vin[x]
                elif (self.freq_complete[x] >= 0):
                    if (self.freq_complete[x] < self.cut_off* 2):
                        self.vout[x] = math.pow(10, (float(attenuation) / 20)) * self.vin[x]
                    elif (self.freq_complete[x] > self.cut_off2* 2):
                        self.vout[x] = math.pow(10, (float(attenuation) / 20)) * self.vin[x]
