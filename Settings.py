import json

class Settings():
    def __init__(self):
        self.loadSettings()

    def default(self):
        #General
        self.display_absorbCurve = True
        self.display_designCurvesInFit = True
        self.defaultFile = 'Materials.xlsx'
        self.incident_angle = 2
        self.incoherence_factor = 6.2
        self.standard_wave_list = [360.0, 380.0, 400.0, 420.0, 440.0, 460.0, 480.0, 500.0, 520.0, 540.0, 560.0,
                                    580.0, 600.0, 620.0, 640.0, 660.0, 680.0, 700.0, 720.0, 740.0, 760.0, 780.0,
                                    800.0, 850.0, 900.0, 1000.0, 1100.0, 1300.0, 1550.0, 1800.0, 2000.0, 2200.0]
        self.domain_min_wvl =[]
        self.domain_max_wvl =[]
        self.standard_wave_list_mod = [360.0, 380.0, 400.0, 420.0, 440.0, 460.0, 480.0, 500.0, 520.0, 540.0, 560.0,
                                    580.0, 600.0, 620.0, 640.0, 660.0, 680.0, 700.0, 720.0, 740.0, 760.0, 780.0,
                                    800.0, 850.0, 900.0, 1000.0, 1100.0, 1300.0, 1550.0, 1800.0, 2000.0, 2200.0]

        #Color
        self.color_cmfs = 'CIE 1931 2 Degree Standard Observer'
        self.color_cmfs_list = ['CIE 1931 2 Degree Standard Observer', 
                                'CIE 1964 10 Degree Standard Observer', 
                                'CIE 2012 2 Degree Standard Observer',
                                'CIE 2012 10 Degree Standard Observer']

        self.color_illuminant = 'D65' #ILLUMINANTS_RELATIVE_SPDS: D65, A, C
        self.color_illuminant_list = ['D65', 'A', 'B', 'C', 'D50', 'D55', 'D60', 'D75','E', 'F1', 'F2', 
                                        'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']

        #Fit
        self.Opt_maxIteration = 500
        self.Opt_maxIncluded = False
        self.Opt_minheight = 0
        self.Opt_maxheight = 300
        self.Opt_minde = 1.01
        self.Opt_maxde = 12
        self.Opt_minw0_U = 0
        self.Opt_minwp_U = 0
        self.Opt_mingamma_U = 0
        self.Opt_minw0_D = 0
        self.Opt_minwp_D = 0
        self.Opt_mingamma_D = 0
        self.Opt_maxw0_U = 55
        self.Opt_maxwp_U = 160
        self.Opt_maxgamma_U = 12
        self.Opt_maxw0_D = 105
        self.Opt_maxwp_D = 200
        self.Opt_maxgamma_D = 28
        self.fitMethod = 'default'
        
        #CURRENTLY IN STACK
        self.fitting_layer = -1
        self.refresh_time = 1

        self.SQL_driver = "SQL Server Native Client 11.0"
        self.SQL_server = "localhost\ZEISSSQL"
        self.SQL_DB = "ThinProcess"

        self.device_list = ['Device 1', 'Device 2']
        self.device_select = 0

        self.saveSettings()
        
    
    def saveSettings(self):
        with open('settings.json', 'w') as outfile:
            json.dump(self.__dict__, outfile)
    
    def loadSettings(self):
        try:
            with open('settings.json', 'r') as f:
                test = json.load(f)
                self.__dict__ = test
        except FileNotFoundError:
            self.default()
