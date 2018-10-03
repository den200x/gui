def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False

def is_number(s):
    '''Function checks if string is number. Returns bool.'''
    try:
        float(s)
        return True
    except ValueError:
        return False

def getThicknessFromString(value):
    '''Function converts string including metric unit into value in 'nm'. Returns value in 'nm'.'''
    value = value.replace(" ", "")
    if len(value) > 1:
        if value[-2:] == 'nm' and is_number(value[:-2]):
            t = float(value[:-2])
        elif value[-2:] == 'µm' and is_number(value[:-2]):
            t = float(value[:-2]) * 1000
        elif value[-2:] == 'mm' and is_number(value[:-2]):
            t = float(value[:-2]) * 1000000
        elif 'l' in value:
            #Filters all digits from string
            lst = list(filter(str.isdigit, value))
            number = abs(int(''.join(lst)))      
            t = str(number) + 'l'
        else:
            if is_number(value):
                t = float(value)
            else:
                t = 0
    else:
        if is_number(value):
            t = float(value)

    if is_number(t) and t < 0:
        t = -t
    return t

def getThicknessAndUnit(x):
    '''Function converts value in nm to sensible metric unit. Returns string with value and unit.'''
    if str(x)[-1] == 'l':
        thickness = x[:-1]
        if thickness == 1:
            thickness_unit = 'layer'
        else:
            thickness_unit = 'layers'
    else:
    #if unit_system == 'metric':
        thickness = x
        thickness_unit = 'nm'
        if x > 1000: 
            thickness = x/1000
            thickness_unit = 'µm'
        if x > 100000:
            thickness = x/1000000
            thickness_unit = 'mm'
    text = "{:g} {}".format(float(thickness), thickness_unit)
    return text

# def sub_tup(tup):
#     '''
#     Subtract 2nd tuple value from 1st tuple value. Used for determining height of plot.
#     '''
#     return np.abs(tup[1]-tup[0])