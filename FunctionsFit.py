from lmfit import minimize, Minimizer, Parameters, Parameter, report_fit
import numpy as np

def fit(stack, settings):
    '''Function initiates fitting procedure'''
    import time
    start_time = time.time()

    #initial guess
    params = Parameters()
    for layer_idx, mat in enumerate(stack.material):
        for param, value in mat.fit_param.items():
            if value == True and mat.fitStatus:
                param_string = '{}___{}'.format(param, layer_idx)
                if param == 'thickness': 
                    value = mat.actual_thickness
                    minValue = settings.Opt_minheight
                    maxValue = settings.Opt_maxheight
                elif param == 'de': 
                    value = mat.de
                    minValue = settings.Opt_minde
                    maxValue = settings.Opt_maxde
                elif param == 'w0_U': 
                    value = mat.w0_U
                    minValue = settings.Opt_minw0_U
                    maxValue = settings.Opt_maxw0_U
                elif param == 'wp_U': 
                    value = mat.wp_U
                    minValue = settings.Opt_minwp_U
                    maxValue = settings.Opt_maxwp_U
                elif param == 'gamma_U': 
                    value = mat.gamma_U 
                    minValue = settings.Opt_mingamma_U
                    maxValue = settings.Opt_maxgamma_U
                elif param == 'w0_D': 
                    value = mat.w0_D
                    minValue = settings.Opt_minw0_D
                    maxValue = settings.Opt_maxw0_D
                elif param == 'wp_D': 
                    value = mat.wp_D
                    minValue = settings.Opt_minwp_D
                    maxValue = settings.Opt_maxwp_D
                elif param == 'gamma_D': 
                    value = mat.gamma_D
                    minValue = settings.Opt_mingamma_D
                    maxValue = settings.Opt_maxgamma_D

                if settings.Opt_maxIncluded:
                    params.add(param_string, value=value, min=minValue, max = maxValue)
                else:
                    params.add(param_string, value=value, min=minValue)

    #INCLUDE CHECK THAT VALUE IS BELOW MIN OR MAX AND SEND ERROR BOX.
    
    #Create spline of T and R based upon wavelengths used for fit (this is always the the smallest wvl domain list)
    #fit_wvl_shortened = []
    #for idx, wvl in enumerate(stack.fit_wvl):
    #    if (idx % 4) == 0:
    #        fit_wvl_shortened.append(wvl)

    #Is data is from online create spline based upon spline_measureT, else on standard (from Excel) spline_excelT.
    if stack.online:
        stack.setTRAsplines(stack.measure_wvl, type = 'measured', kind = 'cubic')
        T = stack.spline_measureT(stack.fit_wvl)
        R = stack.spline_measureR(stack.fit_wvl)
    else:
        T = stack.spline_excelT(stack.fit_wvl)
        R = stack.spline_excelR(stack.fit_wvl)

    #create single y array
    y = np.array([T, R]).flatten()
    
    #calculate fit 
    x = stack.fit_wvl
    result = minimize(optimizeDrudeParameters(stack), params, args=(x, y))
    #Minimize methods are: leastsq (default), least_squares, differential_evolution, brute, nelder,
    #lbfgsb, powell, cg (conjugate-gradient), newton, cobyla, tnc (truncate newton),
    #trust-ncg (trust Newton-Conjugate-Gradient), dogleg,slsqp (sequntial linear squares programming)

    #Store new drude parameters
    dic = result.params.valuesdict()
    changed_layers = []
    for param, value in dic.items():
        drude, layer_idx = param.split('___')
        layer_idx = int(layer_idx)
        value = float(value)
        changed_layers.append(layer_idx)
        if drude == 'thickness':  stack.material[layer_idx].actual_thickness = value
        elif drude == 'de': stack.material[layer_idx].de = value
        elif drude == 'w0_U': stack.material[layer_idx].w0_U = value
        elif drude == 'wp_U': stack.material[layer_idx].wp_U = value
        elif drude == 'gamma_U': stack.material[layer_idx].gamma_U = value
        elif drude == 'w0_D': stack.material[layer_idx].w0_D = value
        elif drude == 'wp_D': stack.material[layer_idx].wp_D = value
        elif drude == 'gamma_D': stack.material[layer_idx].gamma_D = value

    #Update results for the plotting.  
    for layer_idx in changed_layers:
        stack.material[layer_idx].create_NKspline()

    end_time = time.time()
    print("Time: ", end_time - start_time)
    #print('Result iterations: {}'.format(result.nfev))
    #print('Fit was: {}'.format(result.success))
    return stack

def optimizeDrudeParameters(stack):
    '''Function calculatest the TRA of the stack. Output is a flattened array of T and R of the delta
     between the measured and the fitted values.'''
    def function(params, x, y):
        import time
        import numpy as np
        from scipy.interpolate import interp1d
        import tmm
        start_time = time.time()
        dic = params.valuesdict()
        changed_layers = []
        for param, value in dic.items():
            drude, layer_idx = param.split('___')
            layer_idx = int(layer_idx)
            value = float(value)
            changed_layers.append(layer_idx)
            if drude == 'thickness':  stack.material[layer_idx].actual_thickness = value
            elif drude == 'de': stack.material[layer_idx].de = value
            elif drude == 'w0_U': stack.material[layer_idx].w0_U = value
            elif drude == 'wp_U': stack.material[layer_idx].wp_U = value
            elif drude == 'gamma_U': stack.material[layer_idx].gamma_U = value
            elif drude == 'w0_D': stack.material[layer_idx].w0_D = value
            elif drude == 'wp_D': stack.material[layer_idx].wp_D = value
            elif drude == 'gamma_D': stack.material[layer_idx].gamma_D = value

        #Generate new NK spline for changed layers  
        for layer_idx in np.unique(changed_layers):
            stack.material[layer_idx].create_NKspline()

        TMM_TRA_results = []
        y_T = []
        y_R = []
    
        #Build stack for calculation
        pol = "s"
        n_func_list = []
        c_func_list = []
        d_list = []

        #create stack
        #air
        n_func_list.append(1)
        d_list.append(np.inf)
        c_func_list.append('i')
        th_0 = stack.incident_angle * np.pi / 180
        
        #layers
        for idx in range(len(stack.material)):
            #Only add layer is fitStatus is on.
            if stack.material[idx].fitStatus:
                if str(stack.thickness[idx])[-1] == 'l':
                    Hx = float(stack.thickness[idx][:-1]) * layers_in_stack.material[idx].standard_thickness
                else:
                    Hx = stack.material[idx].actual_thickness
                d_list.append(Hx)
                n_func_list.append(stack.material[idx].splineNKcomplex)
                c_func_list.append(Hx > stack.incoherence_factor * np.array(stack.fit_wvl))
        
        #air
        n_func_list.append(1)
        d_list.append(np.inf)
        c_func_list.append('i')

        mid_time = time.time()

        for idx, wvl in enumerate(x):
            n_list = []
            c_list = []
            for n in n_func_list:
                if type(n) == interp1d:
                    n_list.append(n(wvl).item())
                else:
                    n_list.append(n)
            for c in c_func_list:
                if type(c) == np.ndarray:
                    if c[idx].item():
                        c_list.append('i')
                    else:
                        c_list.append('c')
                else:
                    c_list.append(c)
            
            if stack.REVERSE_STACK:
                result = tmm.inc_tmm_fast_reverse(pol, n_list, d_list, c_list, th_0, wvl)
            else:
                result = tmm.inc_tmm_fast(pol, n_list, d_list, c_list, th_0, wvl)
            y_T.append(result["T"])
            y_R.append(result["R"])
        end_time = time.time()
        print("Time TMM duration: ", time.time() - mid_time)
        print("Time TMM done: ", end_time - start_time)

        y_fit = np.concatenate((y_T, y_R), axis=0)
        return y - y_fit
    return function