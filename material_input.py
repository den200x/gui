def get_test_param():
    de = 1.40 #dielectric constant
    w0_U = 34.00 #per sec^2
    wp_U = 65.4
    γU = 0.4800 #per sec     
    wp_D = 184.0
    w0_D = 0.0
    γD = 0.1460
    
    de = 1.2 #dielectric constant
    w0_U = 22.00 #per sec^2
    wp_U = 30
    γU = 0.3 #per sec     
#    DRUDE PARAMETERS
    w0_D = 0.1
    wp_D = 100.0
    γD = 0.05
    return convert_drude_units(de, w0_U, wp_U, γU, w0_D, wp_D, γD)

def get_drude_param(material):
    if material == "AG":
        #UV PARAMETERS
        de = 1.40 #dielectric constant
        w0_U = 34.00 #per sec^2
        wp_U = 65.4
        γU = 0.4800 #per sec     
        #DRUDE PARAMETERS
        w0_D = 0
        wp_D = 184.0
        γD = 0.1460

    elif material == 'SIO2':
        #UV PARAMETERS
        de = 2.16 #dielectric constant
        w0_U = 45.0
        wp_U = 1.2
        γU = 0.2310
        #DRUDE PARAMETERS
        w0_D = 0
        wp_D = 0
        γD = 0 #per sec, 1/Tau
       
    elif material == "TIO2":
        #UV PARAMETERS
        de = 3.86 #dielectric constant
        w0_U = 38.6
        wp_U = 37.3
        γU = 0.0250
        #DRUDE PARAMETERS
        w0_D = 0
        wp_D = 0.379
        γD = 0

    elif material == "NB2O5":
        #UV PARAMETERS
        de = 2.77 #dielectric constant
        w0_U = 51.1
        wp_U = 101
        γU = 0.0840
        #DRUDE PARAMETERS
        w0_D = 0
        wp_D = 0
        γD = 0 #per sec, 1/Tau
        
    elif material == "TIO2-TIPP":
        #UV PARAMETERS
        de = 2.28 #dielectric constant
        w0_U = 41.10
        wp_U = 44.5
        γU = 4.5 * 10**-8 
        
        #DRUDE PARAMETERS
        w0_D = 0
        wp_D = 0.464
        γD = 0 #per sec, 1/Tau
    elif material == "COPPER":
        #UV PARAMETERS
        de = 3.0 #dielectric constant
        w0_U = 13.5
        wp_U = 12.0
        γU = 0.414
        #DRUDE PARAMETERS
        w0_D = 0
        wp_D = 154
        γD = 0.214
        
    elif material == "ITO":
        #UV PARAMETERS
        de = 3.5 #dielectric constant
        w0_U = 36.0
        wp_U = 22.0
        γU = .64
        
        #DRUDE PARAMETERS
        w0_D = 0
        wp_D = 3.56
        γD = 0.2
    elif material == "TA2O5":
        #UV PARAMETERS
        de = 3.18 #dielectric constant
        w0_U = 45.7
        wp_U = 29.5
        γU = .055
        
        #DRUDE PARAMETERS
        w0_D = 10**-9 
        wp_D = .04
        γD = 0.482
    elif material == "HB3-3MIL":
        #UV PARAMETERS
        de = 2.72 #dielectric constant
        w0_U = 25.1
        wp_U = 0.028
        γU = 0.00573
        
        #DRUDE PARAMETERS
        w0_D = 92.8
        wp_D = 0.00523
        γD = 24.0
    else:
        raise ValueError('Drude parameters of ' + material + ' unknown.')
        
    return convert_drude_units(de, w0_U, wp_U,γU, w0_D, wp_D,γD)

def convert_drude_units(de, w0_U, wp_U,γU, w0_D, wp_D,γD):
     #conversion of original meyerware input to rad / s
    w0_U = (w0_U * 10**30)**0.5 #per sec^2
    wp_U = (wp_U * 10**30)**0.5 #per sec^2
    γU = γU * 10**15 #per sec
    w0_D = (w0_D * 10**30)**0.5 #per sec^2
    wp_D = (wp_D * 10**30)**0.5 #per sec^2
    γD = γD * 10**15 #per sec, 1/Tau 
    return [de, w0_U, wp_U,γU, w0_D, wp_D,γD]

def convert_to_inputunits(de, w0_U, wp_U,γU, w0_D, wp_D,γD):
     #conversion ofrad / s to original meyerware input 
    w0_U = w0_U**2 / 10**30 #per sec^2
    wp_U = wp_U**2 / 10**30 #per sec^2
    γU = γU / 10**15 #per sec
    wp_D = wp_D**2 / 10**30#per sec^2
    w0_D = w0_D**2 / 10**30 #per sec^2
    γD = γD / 10**15 #per sec, 1/Tau 
    return [de, w0_U, wp_U,γU, w0_D, wp_D,γD]

def get_drude_param_range():
    de_min = 1.0 #dielectric constant
    de_max = 10. #dielectric constant
    w0_U_min = 20. #per sec^2
    w0_U_max = 100. #per sec^2
    wp_U_min = 0.0
    wp_U_max = 200.
    γU_min = 0.0 #per sec   
    γU_max = 30.0 
#    DRUDE PARAMETERS
    w0_D_min = 0.0
    w0_D_max = 100
    wp_D_min = 0.0
    wp_D_max = 300.
    γD_min = 0.0
    γD_max = 1.0
    pmin = convert_drude_units(de_min, w0_U_min, wp_U_min,γU_min, w0_D_min, wp_D_min,γD_min)
    pmax = convert_drude_units(de_max, w0_U_max, wp_U_max,γU_max, w0_D_max, wp_D_max,γD_max)
    return (pmin,pmax)