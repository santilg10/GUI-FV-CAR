import PySimpleGUI as sg
from KeyDefines import *


def layoutDatosParametricos(enabled, parametricKeys, listaAzimuts):
    enable_parametric =     [sg.Checkbox("Simulación paramétrica", key=ENABLE_PARAMETRIC_INPUT, enable_events=True)]
    parametric_var_layout = [sg.vtop(sg.Text("Variable parametrizable", size=PARAM_VAR_SIZE)), 
                             sg.Combo(values=parametricKeys, default_value=parametricKeys[0], disabled=(not enabled),
                                      size=(MIN_WIDTH, LISTBOX_SIZE),readonly=True, key=PARAMETRIC_VAR_INPUT, enable_events=True)]
    valores_layout =        [sg.vtop(sg.Text("Valores", size=PARAM_VAR_SIZE)),
                             sg.Listbox(values=listaAzimuts, size=(MIN_WIDTH, LISTBOX_SIZE), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, 
                                        enable_events=True, key=VALUES_PARAMETRIC_INPUT, disabled=(not enabled))]

    layout_parametric =     [enable_parametric,
                             parametric_var_layout,
                             valores_layout]

    return layout_parametric

def frameDatosParametricos(parametricKeys, listaAzimuts):
    frame_parametrica = sg.Frame("Datos paramétricos", layout=layoutDatosParametricos(False, parametricKeys, listaAzimuts), expand_x=True, expand_y=True)
    return frame_parametrica