import PySimpleGUI as sg
from KeyDefines import *
from layouts.layoutFechaYLugar import layoutFechaYLugar
from layouts.layoutConfigCell import layoutConfigCell
from layouts.layoutGeometria import layoutGeometria
from layouts.layoutDatosRadiacion import layoutDatosRadiacion

def vistaConfigStaticSim(resolutionValues, buttonMenuHourList, buttonMenuMinuteLis, listaAzimuts, frameSize):
    frame_fecha_lugar =         sg.Frame("Fecha y lugar", layoutFechaYLugar(resolutionValues, buttonMenuHourList, buttonMenuMinuteLis))
    frame_configuracion_cel =   sg.Frame("Configuración célula", layoutConfigCell(resolutionValues, LISTA_TECNOLOGIAS), expand_x=True, expand_y=True)
    frame_geometria =           sg.Frame("Geometría", layoutGeometria(resolutionValues, listaAzimuts), expand_x=True, expand_y=True)
    frame_radiacion =           sg.Frame("Datos radiación", layout=layoutDatosRadiacion(), expand_x=True, expand_y=True)
    generar_config_layout =     [sg.Push(), sg.Button("Generar config", size=(20,2), key=GENERAR_CONFIG), sg.Push()]
    static_sim_data_layout =    [[frame_fecha_lugar, frame_configuracion_cel, frame_geometria],
                                 [frame_radiacion],
                                 generar_config_layout]
    frame_static_sim_config =   sg.Frame("", layout=static_sim_data_layout)
    frameSize.append(frame_static_sim_config.Size)
    return frame_static_sim_config