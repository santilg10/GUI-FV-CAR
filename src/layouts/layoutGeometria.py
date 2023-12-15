import PySimpleGUI as sg
from KeyDefines import *

def layoutGeometria(resolutionValues, listaAzimuts):
    x_layout =              [sg.T("Dimensión horizontal", size=GEOM_MIN_SIZE),
                            sg.Spin(values=resolutionValues, size=MIN_SIZE, key=DIM_X_INPUT)]

    y_layout =              [sg.T("Dimensión vertical", size=GEOM_MIN_SIZE),
                            sg.Spin(values=resolutionValues, size=MIN_SIZE, key=DIM_Y_INPUT)]

    curvatura_layout =      [sg.T("Radio de Curvatura", size=GEOM_MIN_SIZE),
                            sg.Spin(values=resolutionValues, size=MIN_SIZE, key=CURVATURA_INPUT)]

    orientacion_layout =    [sg.T("Orientación", size=GEOM_MIN_SIZE),
                            sg.Spin(values=resolutionValues, size=MIN_SIZE, key=ORIENTACION_INPUT),
                            sg.T("º")]
    
    azimut_layout =         [sg.T("Azimut", size=GEOM_MIN_SIZE),
                            sg.Spin(values=listaAzimuts, size=MIN_SIZE, key=AZIMUT_INPUT)]

    layout_geometria =  [x_layout,
                        y_layout,
                        curvatura_layout,
                        orientacion_layout,
                        azimut_layout]
    return layout_geometria