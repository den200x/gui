def convertStackTRAtoGeneralTRA(wvl_list, stack):
    '''Interpolate transmission and reflection curve for provided stack wavelengths to match with general wavelengths'''
    from scipy.interpolate import interp1d
    wvl_Stack = stack.wvl
    T_Stack = stack.excelT
    R_Stack = stack.excelR
    A_Stack = stack.excelA
    
    f_T = interp1d(wvl_Stack, T_Stack, kind='cubic', fill_value = 'extrapolate')
    f_R = interp1d(wvl_Stack, R_Stack, kind='cubic', fill_value = 'extrapolate')
    f_A = interp1d(wvl_Stack, A_Stack, kind='cubic', fill_value = 'extrapolate')
   
    T = []
    R = []
    A = []
    for wvl in wvl_list:
        T.append(f_T(wvl).item())
        R.append(f_R(wvl).item())
        A.append(f_A(wvl).item())
    return (T, R, A)
                        
def getWaveList(stack, standard_wave_list):
    '''Function returns list general wave_list based upon available lists of wavelengths.'''
    import numpy as np
    min_wave = min(standard_wave_list)
    temp_min = 0
    #max_wave = np.inf
    max_wave = max(standard_wave_list)
    temp_max = 0
    if not len(stack.wvl) == 0:
        temp_min = min(stack.wvl)
        temp_max = max(stack.wvl)
        min_wave = temp_min if temp_min > min_wave else min_wave
        max_wave = temp_max if temp_max < max_wave else max_wave
    if not len(stack.fit_wvl) == 0:
        temp_min = min(stack.fit_wvl)
        temp_max = max(stack.fit_wvl)
        min_wave = temp_min if temp_min > min_wave else min_wave
        max_wave = temp_max if temp_max < max_wave else max_wave
    for mat in stack.material:
        if not mat.model == 'drude':
            temp_min = min(mat.wvl)
            temp_max = max(mat.wvl)
            min_wave = temp_min if temp_min > min_wave else min_wave
            max_wave = temp_max if temp_max < max_wave else max_wave
        else:
            temp_min = min(standard_wave_list)
            temp_max = max(standard_wave_list)
            min_wave = temp_min if temp_min > min_wave else min_wave
            max_wave = temp_max if temp_max < max_wave else max_wave
    min_list = np.subtract(standard_wave_list, min_wave) >= 0
    min_idx = next(idx for idx,value in enumerate(min_list) if value)
    max_list = np.subtract(standard_wave_list, max_wave) <= 0
    max_idx = next(idx for idx,value in reversed(list(enumerate(max_list))) if value)
    return standard_wave_list[min_idx:max_idx+1]


def writeToExcelFile(material, wvl, data):
    import xlsxwriter
    workbook = xlsxwriter.Workbook('fit_results.xlsx')
    worksheet = workbook.add_worksheet()
   
    for row, array in enumerate(data):
        col = 0
        worksheet.write(row, col, material)
        col = 1
        worksheet.write(row, col, wvl[row])
        col = 2
        worksheet.write_row(row, col, array)
    workbook.close()
                   
# def getMaterialInfoInStack(material_db, stack, DO_FIT):
#     '''Function checks if materials in stacks are present and returns list with material info of stack'''
#     layer_info = []
#     #Collect existing N and K material info
#     layer_info.append([])
#     for mat in stack.layers:
#         #Skip if there is a new material of which the layer has to be fitted
#         #if not mat in material_db:
#         if not contains(material_db, lambda x: x.name == mat):
#             if (not DO_FIT) and (stack.layers == mat):
#                 raise ValueError('Material '+ mat + ' in stack is not found in Material database.')
#             else:
#                 layer_info[stack_idx].append([]) #create empty array for material to be fitted)
#         else:
#             found_material = [x for x in material_db if x.name == mat]
#             if len(found_material) > 1:
#                 raise ValueError('Duplicate names for materials in DB. This is not allowed.')
#             layer_info[stack_idx].append(*found_material)
    # return layer_info

def addMaterialInfoToStack(material_db, stack, DO_FIT):
    '''Function checks if materials in stack are present and returns updated Stack object with material info of stack'''
    from PyQt5 import QtWidgets
    from Stack import Stack, Material
    import copy
    from helperFunctions import contains
    
    #Collect existing N and K material info
    for layer_id,mat in enumerate(stack.layers):
        #Skip if there is a new material of which the layer has to be fitted
        #if not mat in material_db:
        if not contains(material_db, lambda x: x.name == mat):
            if (not DO_FIT) and (stack.layers[layer_id] == mat):
                #raise ValueError('Material '+ mat + ' in stack is not found in Material database.')
                title = 'Material not found!'
                error_text = "{} not found in DB.".format(mat)
                error = True
                stack = Stack()
                return (stack, error, error_text, title)
            else:
                stack.material.append(None) #create empty array for material to be fitted)
        else:
            found_material = [x for x in material_db if x.name == mat]
            if len(found_material) > 1:
                title = 'Duplicate material names!'
                error_text = "Duplicate names for material {} in DB. This is not allowed.".format(mat)
                error = True
                stack = Stack()
                return (stack, error, error_text, title)
            found_material = copy.deepcopy(found_material)
            stack.material.append(*found_material)
            stack.material[layer_id].actual_thickness = stack.thickness[layer_id]

    title = ''
    error_text = ''
    error = False
    return (stack, error, error_text, title)

def getMaxDeltaBetweenCurves(x1, x2, y1, y2, increment):
    '''Returns the wavelength and the delta between two sets using the upper minimum and lower maximum of the set ranges'''
    import numpy as np
    from scipy.interpolate import interp1d
    min_wave = x1[0] if x1[0] > x2[0] else x2[0]
    max_wave = x1[len(x1)-1] if x1[len(x1)-1] < x2[len(x2)-1] else x2[len(x2)-1]
    wave_range = np.arange(min_wave, max_wave+increment, increment)
    y1_func = interp1d(x1, y1, kind ='cubic')
    y2_func = interp1d(x2, y2, kind ='cubic')
    max_delta_wave = wave_range[np.argmax(np.absolute(y1_func(wave_range) - y2_func(wave_range)))]
    delta = np.absolute(y1_func(max_delta_wave) - y2_func(max_delta_wave))
    return (max_delta_wave,delta)

def running_median_insort(seq, window_size):
    """Contributed by Peter Otten"""
    from collections import deque
    from bisect import insort, bisect_left
    from itertools import islice
    seq = iter(seq)
    d = deque()
    s = []
    result = []
    for item in islice(seq, window_size):
        d.append(item)
        insort(s, item)
        result.append(s[len(d)//2])
    m = window_size // 2
    for item in seq:
        old = d.popleft()
        d.append(item)
        del s[bisect_left(s, old)]
        insort(s, item)
        result.append(s[m])
    return result

def calculateTRA(stack, plottype, fitting_layer, incident_angle, incoherence_factor, ActualThicknessCurve, REVERSE_STACK):
    '''Function calculates TRA based upon NK or drude parameters. Returns tuple with TRA.'''
    y_T = []
    y_R = []
    y_A = [] 
    TMM_TRA_results = []

    for idx, wvl in enumerate(stack.fit_wvl):
        result = getTRAfromNKandHeight(wvl, idx, stack, plottype, fitting_layer, incident_angle, incoherence_factor, ActualThicknessCurve, REVERSE_STACK)
        #result = getTRAfromNKandHeight2(wvl, idx, stack, fitting_layer, incident_angle, incoherence_factor, ActualThicknessCurve, REVERSE_STACK)
        TMM_TRA_results.append(result)
    
    for dic in TMM_TRA_results:
        #appended value are numpy.float
        y_T.append(dic["T"])
        y_R.append(dic["R"])
        y_A.append(1 - dic["T"]- dic["R"])

    return (y_T, y_R, y_A)

def getTRAfromNKandHeight(wvl, idx, stack, plottype, fitting_layer, incident_angle, incoherence_factor, ActualThicknessCurve, REVERSE_STACK, DO_FIT = False, Nfit= 0, Hfit = 0, ESTIMATE_HEIGHT = False):
    '''Function calculates TRA from N, K and height. Also used for the function to perform with with N, K and optionnaly height. Returns TMM object'''
    import numpy as np
    import tmm
    pol = "s"
    n_list = []
    d_list = []
    c_list = []

    #create stack
    #air
    n_list.append(1)
    d_list.append(np.inf)
    c_list.append('i')
    th_0 = incident_angle * np.pi / 180

    layer_range = range(len(stack.layers))
    for idx in layer_range:
        if stack.material[idx].fitStatus or plottype == 'design':
            height = stack.thickness[idx]
            #Height in If-statement represent amount of bi-layers in case of LbL
            if str(height)[-1] == 'l':
                Hx =  float(height[:-1]) * stack.material[idx].standard_thickness
            else:
                if ActualThicknessCurve:
                    Hx = stack.material[idx].actual_thickness  
                else:
                    Hx = stack.thickness[idx]
            if DO_FIT and idx == fitting_layer:
                Nc = Nfit
                if ESTIMATE_HEIGHT:
                    Hx = Hfit
            else:
                Nx = stack.material[idx].get_NKspline_value('N',wvl)
                Kx = stack.material[idx].get_NKspline_value('K',wvl)
                Nc = Nx - 1j*Kx
            if Hx > incoherence_factor * wvl:
                c_list.append('i')
            else:
                c_list.append('c')
            n_list.append(Nc)
            d_list.append(Hx)
        
    #air
    n_list.append(1)
    d_list.append(np.inf)
    c_list.append('i')
    
    #calculate stack at given wavelength
    if REVERSE_STACK:
        result = tmm.inc_tmm_fast_reverse(pol, n_list, d_list, c_list, th_0, wvl)
    else:
        result = tmm.inc_tmm_fast(pol, n_list, d_list, c_list, th_0, wvl)
    return result

#OPTIMIZE THIS!
def getTRAfromNKandHeight2(stack, fitting_layer, incident_angle, incoherence_factor, ActualThicknessCurve, REVERSE_STACK, DO_FIT = False, Nfit= 0, Hfit = 0, ESTIMATE_HEIGHT = False):
    '''Function calculates TRA from N, K and height. Also used for the function to perform with with N, K and optionnaly height. Returns TMM object'''
    import numpy as np
    import tmm
    pol = "s"
    n_list = []
    d_list = []
    c_list = []

    #create stack
    #air
    n_list.append(1)
    d_list.append(np.inf)
    c_list.append('i')
    th_0 = incident_angle * np.pi / 180

    for idx in range(len(stack.layers)):
        height = stack.thickness[idx]
        #Height in If-statement represent amount of bi-layers in case of LbL
        if str(height)[-1] == 'l':
            Hx =  float(height[:-1]) * stack.material[idx].standard_thickness
        else:
            if ActualThicknessCurve:
                Hx = stack.material[idx].actual_thickness  
            else:
                Hx = stack.thickness[idx]
        if DO_FIT and idx == fitting_layer:
            Nc = Nfit
            if ESTIMATE_HEIGHT:
                Hx = Hfit
        else:
            Nx = stack.material[idx].get_NKspline_value('N',wvl)
            Kx = stack.material[idx].get_NKspline_value('K',wvl)
            Nc = Nx - 1j*Kx
        if Hx > incoherence_factor * wvl:
            c_list.append('i')
        else:
            c_list.append('c')
        n_list.append(Nc)
        d_list.append(Hx)
        
    #air
    n_list.append(1)
    d_list.append(np.inf)
    c_list.append('i')
    
    #calculate stack at given wavelength
    if REVERSE_STACK:
        result = tmm.inc_tmm_fast_reverse(pol, n_list, d_list, c_list, th_0, wvl)
    else:
        result = tmm.inc_tmm_fast(pol, n_list, d_list, c_list, th_0, wvl)
    return result

def calculateRMS(measuredT, measuredR, fittedT, fittedR):
    '''Function calculates RMS error of T and R of fitted and measured curves. Error is multiplied by 100. Returns RMS.'''
    import numpy as np
    measuredT = np.asarray(measuredT)
    measuredR = np.asarray(measuredR)
    fittedT = np.asarray(fittedT)
    fittedR = np.asarray(fittedR)
    sum_squares = ((measuredT - fittedT)*100)**2 + ((measuredR - fittedR)*100)**2
    return np.sqrt(np.mean(sum_squares)/2)

def calculateColorValues(splineT, splineR, settings):
    '''Function calculates color values of the Transmission and Refelection side of the stack. 
    Input Arguments are tranmission and reflection spline functions.
    Returns array of values/tuples of different standards.'''
    import colour
    import numpy as np
    wvl = np.linspace(380,780,81)
    dic_T = {}
    dic_R = {}
    dic_test = {}
    for idx, value in enumerate(wvl):
        dic_T[value] = splineT(value).item()
        dic_R[value] = splineR(value).item()

    #Removes warnings from conversions.
    colour.filter_warnings()
    cmfs = colour.STANDARD_OBSERVERS_CMFS[settings.color_cmfs] #1931 etc
    illuminant = colour.ILLUMINANTS_RELATIVE_SPDS[settings.color_illuminant] #D65, A, C

    T_spd = colour.SpectralPowerDistribution('', dic_T)
    T_XYZ = colour.spectral_to_XYZ(T_spd, cmfs, illuminant)
    T_xy =  colour.XYZ_to_xy(T_XYZ/100)
    T_ab =  colour.XYZ_to_Lab(T_XYZ/100, illuminant=colour.ILLUMINANTS[settings.color_cmfs][settings.color_illuminant])
    T_rgb = colour.XYZ_to_sRGB(T_XYZ/100, illuminant=colour.ILLUMINANTS[settings.color_cmfs][settings.color_illuminant])

    R_spd = colour.SpectralPowerDistribution('', dic_R)
    R_XYZ = colour.spectral_to_XYZ(R_spd, cmfs, illuminant)
    R_xy =  colour.XYZ_to_xy(R_XYZ/100)
    R_ab =  colour.XYZ_to_Lab(R_XYZ/100, illuminant=colour.ILLUMINANTS[settings.color_cmfs][settings.color_illuminant])
    R_rgb = colour.XYZ_to_sRGB(R_XYZ/100, illuminant=colour.ILLUMINANTS[settings.color_cmfs][settings.color_illuminant])

    return (T_XYZ, T_xy, T_ab, T_rgb, R_XYZ, R_xy, R_ab, R_rgb)



        
                            