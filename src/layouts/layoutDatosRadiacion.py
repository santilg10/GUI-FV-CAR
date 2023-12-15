import PySimpleGUI as sg
from KeyDefines import *

def layoutDatosRadiacion():
    #CLEAR_SKY
    clear_sky_layout =      [[sg.Radio("Clear sky", group_id=RADIATION_TYPE_GROUP, default=True, enable_events=True, key=CLEAR_SKY)]]
    col_clear_sky = sg.Col(layout=clear_sky_layout)

    #TMY
    tmy_layout =            [[sg.Radio("Tmy", group_id=RADIATION_TYPE_GROUP, enable_events=True, key=TMY)],
                            [sg.Listbox(values=LISTA_TMY, size=(MIN_WIDTH, LISTBOX_SIZE), no_scrollbar=True, disabled=True, key=TMY_INPUT)]]
    col_tmy = sg.Col(layout=tmy_layout)

    #DATA METEO
    data_meteo_layout =     [[sg.Radio("Data meteo", group_id=RADIATION_TYPE_GROUP, enable_events=True, key=DATA_METEO)],
                            [sg.In(size=(25, 1), enable_events=True, disabled=True, key=DATA_METEO_INPUT), 
                            sg.FolderBrowse(disabled=True, key=DATA_METEO_BROWSER)]]
    col_data_meteo = sg.Col(layout=data_meteo_layout)

    layout_radiacion =  [[sg.vtop(col_clear_sky),
                        sg.VSeparator(), 
                        col_tmy,
                        sg.VSeparator(),
                        sg.vtop(col_data_meteo)]]
    
    return layout_radiacion