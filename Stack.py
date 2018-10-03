from collections import defaultdict
from PyQt5 import QtGui, QtWidgets
from helperFunctions import is_number

class Stack:
    def __init__(self):
        self.id = 0
        self.name = ''
        self.layers = []
        self.thickness = []
        self.run = ''
        self.source = ''
        self.date = ''
        self.wvl =[]
        #TRA from DB
        self.excel_wvl =[]
        self.excelT =[]
        self.excelR =[]
        self.excelA =[]
        #TRA from measurement device
        self.measure_wvl =[]
        self.measureT =[]
        self.measureR =[]
        self.measureA =[]
        #TRA from fit
        self.fit_wvl = []
        self.fitT =[]
        self.fitR =[]
        self.fitA =[]
        self.RMSerror = ''
        self.comment =''
        self.material = []
        self.type = ''

        self.online = False
        self.measuredTime = '-'

        #MOVE TO SETTINGS CLASS
        self.fitting_layer = -1
        self.incident_angle = 2
        self.incoherence_factor = 6.2
        self.REVERSE_STACK = True
        

    def layer_count(self):
        return len(self.layers)
        
    def getTRA_DB(self):
        return (self.excelT, self.excelR, self.excelA)

    def getTRA_Measured(self):
        return (self.measureT, self.measureR, self.measureA)

    def getTRA_Fitted(self):
        return (self.fitT, self.fitR, self.fitA)
    
    def save_stack(self):
        pass
    
    def print_info(self):
        print("*******Stack info********")
        print("Name: {}, id: {}".format(self.name,self.id))
        print("Light -> {}".format('-'.join(self.layers)))
        print('\n')
        print("Thickness: ")
        for i in range(len(self.layers)):
            t = str(self.thickness[i])
            if t[-1] == 'l':
                t = t[:-1] + ' bi-layers'
            else:
                t += ' nm'
            print("{}: {}".format(self.layers[i], t))
        print('\n')
        print("Run: {}".format(self.run))
        print("Source: {}".format(self.source))
        print("Date: {}".format(self.date))
        print("Comment: {}".format(self.comment))
        print("*************************")

    def setTRAsplines(self, w_list = None, type = 'original', kind = 'cubic'):
        '''Function returns spline of T, R or A. Optional wave list argument determines if own or general wave list is used. Optional kind
        determines degree of spline.'''
        from scipy.interpolate import interp1d
        if type == 'original':
            if not len(self.excelT) == 0:
                self.spline_excelT = interp1d(self.excel_wvl, self.excelT, kind = kind, fill_value= 'extrapolate')
                self.spline_excelR = interp1d(self.excel_wvl, self.excelR, kind = kind, fill_value= 'extrapolate')
                self.spline_excelA = interp1d(self.excel_wvl, self.excelA, kind = kind, fill_value= 'extrapolate')
        elif type == 'measured':
            self.spline_measureT = interp1d(self.measure_wvl, self.measureT, kind = kind, fill_value= 'extrapolate')
            self.spline_measureR = interp1d(self.measure_wvl, self.measureR, kind = kind, fill_value= 'extrapolate')
            self.spline_measureA = interp1d(self.measure_wvl, self.measureA, kind = kind, fill_value= 'extrapolate')
        elif type == 'fitted':
            if not len(self.fitT) == 0:
                self.spline_fitT = interp1d(self.fit_wvl, self.fitT, kind = kind, fill_value= 'extrapolate')
                self.spline_fitR = interp1d(self.fit_wvl, self.fitR, kind = kind, fill_value= 'extrapolate')
                self.spline_fitA = interp1d(self.fit_wvl, self.fitA, kind = kind, fill_value= 'extrapolate')
        elif type == 'design':
            if not len(self.designT) == 0:
                self.spline_designT = interp1d(self.fit_wvl, self.designT, kind = kind, fill_value= 'extrapolate')
                self.spline_designR = interp1d(self.fit_wvl, self.designR, kind = kind, fill_value= 'extrapolate')
                self.spline_designA = interp1d(self.fit_wvl, self.designA, kind = kind, fill_value= 'extrapolate')
    
    def addMaterialToStack(self, material):
        '''Function adds material to stack'''
        modifyName = True if self.name == '-'.join(self.layers) else False
        self.layers.append(material.name)
        if modifyName:
            self.name = '-'.join(self.layers)

        if is_number(material.standard_thickness):
            self.thickness.append(material.standard_thickness)
            material.actual_thickness = material.standard_thickness
        else:
            self.thickness.append(0)
        #self.material.fitStatus = False
        self.material.append(material)

        #TRA from DB
        #self.T =[]
        #self.R =[]
        #self.A =[]

        #TRA from design
        self.designT =[]
        self.designR =[]
        self.designA =[]

        #Splines TRA from design
        self.spline_designT = None
        self.spline_designR = None
        self.spline_designA = None

        
    def removeMaterialFromStack(self, idx):
        '''Function removes one material from stack.'''
        modifyName = True if self.name == '-'.join(self.layers) else False
        del self.layers[idx]
        del self.material[idx]
        del self.thickness[idx]
        if modifyName:
            self.name = '-'.join(self.layers)
        #TRA from DB
        #self.T =[]
        #self.R =[]
        #self.A =[]
        
        #TRA from fit
        self.designT =[]
        self.designR =[]
        self.designA =[]
        
        #Splines TRA from fit
        self.spline_designT = None
        self.spline_designR = None
        self.spline_designA = None

        
    @classmethod
    def get_stacks(cls, inputfile):
        '''Function imports stack data from excel file and returns list with Stack objects.'''
        import pandas as pd
        import numpy as np

        #1. Data entry
        try:
            data_raw = pd.read_excel(inputfile, sheet_name='Table stacks')
            data_raw.loc[data_raw.shape[0]] = np.nan
            empty_rows = data_raw.index[data_raw.isnull().all(axis = 1)]
        except FileNotFoundError:
            data_raw = None
            empty_rows = []
        
        #Group all data. Data is split where 1 or more rows are empty.
        data_grouped = []
        previous_row = 0
        for i in range(len(empty_rows)):
            if not (empty_rows[i] - 1 == previous_row):
                if i == 0:
                    data_grouped.append(data_raw[:empty_rows[i]])
                else:
                    data_grouped.append(data_raw[empty_rows[i-1]+1:empty_rows[i]].reset_index())
            previous_row = empty_rows[i]
        
        stacks = []
        for i in range(len(data_grouped)):
            item = Stack()
            sub_df = data_grouped[i][['wvl', 'T','R']].sort_values(by='wvl', ascending=True)
            item.name = data_grouped[i]['name'][0]
            item.id = int(data_grouped[i]['id'][0])
            item.layers = list(data_grouped[i]['layers'].dropna())
            item.thickness = list(data_grouped[i]['thickness'].dropna())
            item.run = data_grouped[i]['run'][0]
            item.source = data_grouped[i]['source'][0]
            item.date = data_grouped[i]['date'][0]
            item.excel_wvl = list(sub_df['wvl'].dropna())
            
            if len(item.excel_wvl) != len(set(item.excel_wvl)):
                raise ValueError('Error: list of wavelength of stack {} is corrupt.'.format(item.name))
            
            item.excelT = np.array(sub_df['T'].dropna())
            item.excelR = np.array(sub_df['R'].dropna())
            item.excelA = 1 - np.array(item.excelT) - np.array(item.excelR)
            item.comment = ' '.join(list(data_grouped[i]['comment'].dropna()))
            
            stacks.append(item)
    
        return stacks

    def saveStack(self):
        '''Function saves Stack to Excel file'''
        import pandas as pd
        import numpy as np

        #1. Find last row
        inputfile = "Materials.xlsx"
        
        data_raw = pd.read_excel(inputfile, sheet_name='Table stacks')
        data_raw.loc[data_raw.shape[0]] = np.nan
        empty_rows = data_raw.index[data_raw.isnull().all(axis = 1)]

        wvl = self.fit_wvl
        list_name = [''] * len(wvl)
        if len(self.layers) == 0:
                raise ValueError('Stack is empty. Stack not saved.')
        list_name[0] = self.name
        list_id = [''] * len(wvl)
        list_id[0] = 0

        list_layers = [''] * len(wvl)
        for idx, value in enumerate(self.layers):
            list_layers[idx] = value

        list_thickness = [''] * len(wvl)
        for idx, value in enumerate(self.thickness):
            list_thickness[idx] = value
        
        list_run = [''] * len(wvl)
        list_source = [''] * len(wvl)
        list_date = [''] * len(wvl)
        list_comment = [''] * len(wvl)
    
        data = pd.DataFrame(
            {'01_name': list_name,
            '02_id': list_id,
            '03_layers': list_layers,
            '04_thickness': list_thickness,
            '05_run': list_run,
            '06_source': list_source,
            '07_date': list_date,
            '08_wvl': self.fit_wvl,
            '09_T': self.excelT,
            '10_R': self.excelR,
            '11_comment': list_comment
            })

        #3. Data entry
        from openpyxl import load_workbook

        book = load_workbook(inputfile)
        writer = pd.ExcelWriter(inputfile, engine='openpyxl') 
        writer.book = book
        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

        data.to_excel(writer, "Table stacks", startrow = empty_rows[-1] + 2, header = False, index = False)
        writer.save()
        
    def isEmpty(self):
        return True if len(self.layers) == 0 else False

    def removeMeasuredTRA(self):
        '''Function removes invalidated TRA measurements.'''
        self.measureT = []
        self.measureR = []
        self.measureA = []
    
    def removeOriginalTRA(self):
        '''Function removes invalidated TRA values that were supplied from database.'''
        self.excelT = []
        self.excelR = []
        self.excelA = []


class Material:
    def __init__(self,idx, name):
        self.idx = idx
        self.name = name
        self.material = ''
        self.run = ''
        self.source = ''
        self.date = ''
        self.version = ''
        self.standard_thickness = 0
        self.actual_thickness = 0
        self.wvl =[]
        self.n ={}
        self.k ={}
        self.de = 0
        self.w0_U = 0
        self.wp_U = 0
        self.gamma_U = 0
        self.w0_D = 0
        self.wp_D = 0
        self.gamma_D = 0

        self.de_org = 0
        self.w0_U_org = 0
        self.wp_U_org = 0
        self.gamma_U_org = 0
        self.w0_D_org = 0
        self.wp_D_org = 0
        self.gamma_D_org = 0

        self.comment =''
        self.model = ''
        self.splineN = None
        self.splineK = None
        self.splineNKcomplex = None
        self.color = 'white'
        self.fitStatus = False
        self.editMode = False
        self.incident_angle = 0

        self.fit_param = {'thickness': False, 'de': False, 'w0_U': False,'wp_U': False,'gamma_U': False,'w0_D': False,'wp_D': False,'gamma_D': False}

    
    def print_info(self):
        print("*******Material info********")
        print("Name: {}, id: {}".format(self.name, self.idx))
        print("Assumed thickness: {} nm".format(Stack.thickness))
        print("Run: {}".format(self.run))
        print("Source: {}".format(self.source))
        print("Date: {}".format(self.date))
        print("Version: {}".format(self.version))
        print("Comment: {}".format(self.comment))
        print("*************************")


    def save_material(self):
        pass

    def getDrudeParams(self):
        from material_input import convert_drude_units
        return convert_drude_units(self.de, self.w0_U, self.wp_U, self.gamma_U, self.w0_D, self.wp_D, self.gamma_D)
    
    def getDrudeParamsForPrint(self):
        return self.de, self.w0_U, self.wp_U, self.gamma_U, self.w0_D, self.wp_D, self.gamma_D
    
    def check_DB_valid(self):
        '''check if data makes sense...include check for no double names'''

    @classmethod
    def get_materials(cls, standard_wvl_list, inputfile):
        '''Function imports all material data from excel file and returns list with Material objects.'''
        #Get all NK data
        materials = cls.get_nk_data(cls, inputfile)
        #Get all drude data
        materials += cls.get_drude_data(cls, inputfile, standard_wvl_list)
        
        sorted_materials = sorted(materials, key=lambda x: x.name, reverse=False)
    
        return sorted_materials
    
    def get_NKspline_value(self, NK, wave):
        '''Function returns spline of T, R or A. Optional wave list argument determines if own or general wave list is used.'''
        if self.splineN == None:
            self.create_NKspline()
        if NK == 'N':
            value = self.splineN(wave)
        elif NK == 'K':
            value = self.splineK(wave)
        return value

    def get_NKspline(self, NK):
        '''Function returns spline of N or K.'''
        if self.splineN == None:
            self.create_NKspline()
        if NK == 'N':
            spline = self.splineN()
        elif NK == 'K':
            spline = self.splineK()
        return spline

    def create_NKspline(self):
        from scipy.interpolate import interp1d
        #from numpy import interp
        from FunctionsDrude import NandK_function#, N_function, K_function
        if self.model == 'nk':
            self.splineN = interp1d(self.wvl, self.n, kind ='linear')
            self.splineK = interp1d(self.wvl, self.k, kind ='linear')
        elif self.model == 'drude':
            #slow method
            #n = N_function(self.wvl, self.getDrudeParams())
            #k = K_function(self.wvl, self.getDrudeParams())
            #fast method
            n, k = NandK_function(self.wvl, self.getDrudeParams())
            self.splineN = interp1d(self.wvl, n, kind ='linear')
            self.splineK = interp1d(self.wvl, k, kind ='linear')
            c = n - 1j*k
            self.splineNKcomplex = interp1d(self.wvl, c, kind ='linear')

    def get_nk_data(cls, inputfile):
        import pandas as pd
        import numpy as np

        try:
            data_raw = pd.read_excel(inputfile, sheet_name='Table nk materials')
            data_raw.loc[data_raw.shape[0]] = np.nan
            empty_rows = data_raw.index[data_raw.isnull().all(axis = 1)]
        except FileNotFoundError:
            data_raw = None
            empty_rows = []
        
        #Group all data. Data is split where 1 or more rows are empty.
        data_grouped = []
        previous_row = 0
        for i in range(len(empty_rows)):
            if not (empty_rows[i] - 1 == previous_row):
                if i == 0:
                    data_grouped.append(data_raw[:empty_rows[i]])
                else:
                    data_grouped.append(data_raw[empty_rows[i-1]+1:empty_rows[i]].reset_index())
            previous_row = empty_rows[i]
        
        mat = []
        for i in range(len(data_grouped)):
            sub_df = data_grouped[i][['wvl', 'n','k']].sort_values(by='wvl', ascending=True)
            idx = data_grouped[i]['id'][0]
            name = data_grouped[i]['name'][0]
            item = Material(idx, name)
            item.material = data_grouped[i]['material'][0]
            item.standard_thickness = data_grouped[i]['thickness'][0]
            item.run = data_grouped[i]['run'][0]
            item.source = data_grouped[i]['source'][0]
            item.date = data_grouped[i]['date'][0]
            item.model = data_grouped[i]['model'][0]
            item.type = data_grouped[i]['type'][0]
            item.wvl = list(sub_df['wvl'].dropna())

            if np.isnan(item.date):
                item.date = '-'

            #Procedure check if there are any duplicate wavelengths in the data.
            if len(item.wvl) != len(set(item.wvl)):
                raise ValueError('Error: list of wavelength of material {} is corrupt.'.format(item.name))
            item.n = list(sub_df['n'].dropna())
            item.k = list(sub_df['k'].dropna())
            item.comment = ' '.join(list(data_grouped[i]['comment'].dropna()))
            item.color = cls.setMaterialColor(cls, data_grouped[i]['color'][0])
            item.actual_thickness = item.standard_thickness
            mat.append(item)
        return mat

    def get_drude_data(cls, inputfile, standard_wvl_list):
        import pandas as pd
        import numpy as np
        
        try:
            data_raw = pd.read_excel(inputfile, sheet_name='Table drude materials')
        except FileNotFoundError:
            data_raw = pd.DataFrame()
        #Delete empty rows from dataset
        mat = []
        for i in range(data_raw.shape[0]):
            idx = data_raw['id'][i]
            name = data_raw['name'][i]
            item = Material(idx, name)
            item.material = data_raw['material'][i]
            item.standard_thickness = data_raw['thickness'][i]
            item.run = data_raw['run'][i]
            item.source = data_raw['source'][i]
            item.date = data_raw['date'][i]
            item.wvl = standard_wvl_list
            item.de = data_raw['de'][i]
            item.w0_U = data_raw['w0_U'][i]
            item.wp_U = data_raw['wp_U'][i]
            item.gamma_U = data_raw['gamma_U'][i]
            item.w0_D = data_raw['w0_D'][i]
            item.wp_D = data_raw['wp_D'][i]
            item.gamma_D = data_raw['gamma_D'][i]

            #copy values to originals for restoring.
            item.de_org = item.de
            item.w0_U_org = item.w0_U
            item.wp_U_org = item.wp_U
            item.gamma_U_org = item.gamma_U
            item.w0_D_org = item.w0_D
            item.wp_D_org = item.wp_D
            item.gamma_D_org = item.gamma_D

            item.comment = data_raw['comment'][i]
            item.model = data_raw['model'][i].lower()
            item.type = data_raw['type'][i].lower()
            item.color = cls.setMaterialColor(cls, data_raw['color'][i])

            if item.type == 'substrate':
                item.actual_thickness = item.standard_thickness
            
            #if item.type == 'substrate':
            item.fitStatus = False #means that substrate is directly included in fit.

            mat.append(item)
        return mat

    def setMaterialColor(cls, colorString):
        if QtGui.QColor.isValid(QtGui.QColor(colorString)):
            R,G,B,f = QtGui.QColor(colorString).getRgb()
            color = QtGui.QColor(R,G,B,127)
        else:
            color = QtGui.QColor("white")
        return color

    def restoreOriginalDrudes(self):
        self.de = self.de_org
        self.w0_U = self.w0_U_org
        self.wp_U = self.wp_U_org
        self.gamma_U = self.gamma_U_org
        self.w0_D = self.w0_D_org
        self.wp_D = self.wp_D_org
        self.gamma_D = self.gamma_D_org