import PySimpleGUI as sg
from KeyDefines import *
from layouts.layoutDatosParametricos import frameDatosParametricos


def vistaSesiones(parametricKeys, listaAzimuts):
    nombre_layout       = [sg.T("Nombre", size=TEXT_SIZE), sg.Input(key=NOMBRE_INPUT, size=TEXT_SIZE)]
    descripcion_layout  = [sg.vtop(sg.T("Descripción", size=TEXT_SIZE)), sg.Multiline(key=DESCRIPCION_INPUT, size=(50, 5))]
    config_file_layout  = [sg.T("Archivo configuración", size=TEXT_SIZE), 
                           sg.Input(key=CARGAR_CONFIG_INPUT, enable_events=True, visible=False),
                           sg.FileBrowse("Cargar config", target=CARGAR_CONFIG_INPUT, key=CONFIG_FILE_BROWSER, file_types=(("YAML files", "*.yaml"),)),
                           sg.Text("", auto_size_text=True, key=CONFIG_FILE_TEXT)]
    
    load_session_layout = [sg.Input(key=CARGAR_SESION_INPUT, enable_events=True, visible=False), #solo para actualizar automáticamente
                           sg.Push(), 
                           sg.FolderBrowse(button_text="Cargar sesión previa", target=CARGAR_SESION_INPUT, size=SESSION_BUTTON_SIZE),
                           sg.Push()]
    simular_layout      = [sg.Push(), sg.Button("SIMULAR", size=SESSION_BUTTON_SIZE, key=SIMULAR_INPUT, disabled=True), sg.Push()]

    session_data_layout = [nombre_layout,
                           descripcion_layout,
                           config_file_layout,
                           [frameDatosParametricos(parametricKeys, listaAzimuts)],
                           [sg.VPush()],
                           load_session_layout,
                           [sg.VPush()],
                           simular_layout,
                           [sg.VPush()],]
    
    frame_session_data = sg.Frame("", session_data_layout, expand_x=True, expand_y=True)
    return frame_session_data