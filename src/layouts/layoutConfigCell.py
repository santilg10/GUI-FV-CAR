import PySimpleGUI as sg
from KeyDefines import *


def layoutConfigCell(resolutionValues, listaTeconologias):
    tecnologia_layout =     [sg.vtop(sg.T("Tecnología célula", size=GEOM_MIN_SIZE)),
                            sg.Listbox(values=listaTeconologias, default_values=listaTeconologias[0], size=(MIN_WIDTH, LISTBOX_SIZE), 
                                no_scrollbar=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, key=TECNOLOGIA_INPUT)]

    num_cels_x_layout =     [sg.T("Número células en x", size=GEOM_MIN_SIZE),
                            sg.Spin(values=resolutionValues, expand_x=True, key=NUM_CEL_X_INPUT)]

    num_cels_y_layout =     [sg.T("Número células en y", size=GEOM_MIN_SIZE),
                            sg.Spin(values=resolutionValues, expand_x=True, key=NUM_CEL_Y_INPUT)]

    conexion_layout =       [sg.vtop(sg.T("Tipo de conexión", size=GEOM_MIN_SIZE)),
                            sg.Listbox(values=LISTA_CONEXIONES, default_values=LISTA_CONEXIONES[0], size=(MIN_WIDTH, LISTBOX_SIZE), 
                                no_scrollbar=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, key=CONEXION_INPUT)]

    layout_config_cel = [tecnologia_layout,
                        num_cels_x_layout,
                        num_cels_y_layout,
                        conexion_layout]
    return layout_config_cel