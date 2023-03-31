import os
import shutil
import subprocess
import datetime
import PySimpleGUI as sg
import ValueChecker as vc
import DataStaticSim as dss
import ResultData as rd
from EstadosVistas import EstadosVistas
from YAMLAdapter import YAMLReader, YAMLWriter
from KeyDefines import *

#################
#   DEFINES
#################
resolution_values = []
button_menu_hour_list = []
button_menu_minute_list = []

for i in range(10000):
    resolution_values.append(i)

for i in range(24):
    button_menu_hour_list.append(i)

for i in range(60):
    button_menu_minute_list.append(i)

#   SIZES
min_width = 10
min_height = 1
min_size = (min_width, min_height)

min_button_width = 30
min_button_height = 2
min_button_size = (min_button_width, min_button_height)

geom_min_width = 16
geom_min_height = 1
geom_min_size = (geom_min_width, geom_min_height)

param_var_size = (20, 1)

listbox_size = 5

#   LISTAS AUXILIARES
lista_tecnologias = ("DSC", "CIS", "CdTe", "a-Si", "TF-Si")
lista_conexiones = ("hmSbxPx", "hmSbxPy", 
                    "hmSxPbx", "hmSxPby", 
                    "hmSxPx", "hmSxPy", 
                    "hmSyPbx", "hmSyPby", 
                    "hmSyPx", "hmSyPy", 
                    "SbSx", "SSbx", "SSby")
lista_tmy = ("DB1", "DB2", "DB3")
lista_azimuts = []
for i in range(91):
    if (i % 5) == 0:
        lista_azimuts.append(i)

dict_parametric_vars = {"azimut" : lista_azimuts,
                        "connection" : lista_conexiones}
parametric_keys = []
for key in dict_parametric_vars:
    parametric_keys.append(key)

global dict_results
dict_results = {}

latitud_value = 0
longitud_value = 0

fecha_inicio_timestamp = ""
fecha_fin_timestamp = ""

def popupInValue(title, text):
    window = sg.Window(title, layout=[[sg.T(text)], 
        [sg.In(size=min_size, key=POPUP_INPUT, expand_x=True)], 
        [sg.Push(), sg.OK(), sg.Push()]], background_color="DarkSlateGray3")
    event, values = window.read()
    window.close()
    return None if event != 'OK' else values[POPUP_INPUT]

#############################################
#   VISTA SIMULACIONES
#############################################

def SimulationsLayout():
    simulations_layout =    [[sg.B("Simulación Estática", size=min_button_size, key=STATIC_SIM_SELECTED)],
                            [sg.B("Simulación Dinámica", size=min_button_size, disabled=True)]]
    return simulations_layout

def VistaSimulaciones():
    global window
    window = sg.Window("FV CAR MODEL", layout=SimulationsLayout(), element_padding=(200,50))


#############################################
#   VISTA SIMULACIÓN ESTÁTICA
#############################################

#################
#
#   FECHA Y LUGAR
#
#################

def FechaYLugarLayout():
    resolucion_layout =     [sg.Text("Resolución", size=min_size), sg.Spin(values=resolution_values, size=min_size, key=RESOLUCION_INPUT)] #en minutos
    fecha_inicio_layout =   [sg.Text("Fecha inicio", size=min_size),
                            sg.Push(),
                            sg.Text("YYYY-DD-MM", key=FECHA_INICIO), 
                            sg.Push(),
                            sg.CalendarButton(button_text="change date", target=FECHA_INICIO, format="%Y-%m-%d", key=FECHA_INICIO_INPUT)]
    fecha_final_layout =    [sg.Text("Fecha fin", size=min_size),
                            sg.Push(),
                            sg.Text("YYYY-DD-MM", key=FECHA_FIN),
                            sg.Push(),
                            sg.CalendarButton(button_text="change date", target=FECHA_FIN, format="%Y-%m-%d", key=FECHA_FIN_INPUT)]

    hora_inicio_layout =    [sg.Text("Hora inicio", size=min_size), 
                            sg.Combo(values=button_menu_hour_list, default_value=button_menu_hour_list[0], readonly=True, key=HORA_INICIO_INPUT),
                            sg.Text(":"),
                            sg.Combo(values=button_menu_minute_list, default_value=button_menu_minute_list[0], readonly=True, key=MINUTO_INICIO_INPUT),
                            sg.Push(),]
    hora_final_layout =     [sg.Text("Hora fin", size=min_size),
                            sg.Combo(values=button_menu_hour_list, default_value=button_menu_hour_list[0], readonly=True, key=HORA_FINAL_INPUT),
                            sg.Text(":"),
                            sg.Combo(values=button_menu_minute_list, default_value=button_menu_minute_list[0], readonly=True, key=MINUTO_FINAL_INPUT),
                            sg.Push(),]
    lugar_layout =          [sg.Text("Lugar", size=min_size),
                            sg.Input(key=LUGAR_INPUT, size=(20,2))]

    tool_msg = "Click dcho para introducir valor por teclado"
    latitud_layout =        [sg.Text("Latitud", size=min_size),
                            sg.Slider(range=[-90,90], default_value=0, resolution=0.1, tooltip=tool_msg, orientation='h', key=LATITUD_INPUT)]

    longitud_layout =       [sg.Text("Longitud", size=min_size),
                            sg.Slider(range=[-180,180], default_value=0, resolution=0.1, tooltip=tool_msg, orientation='h', key=LONGITUD_INPUT)]

    layout_fecha_lugar =    [resolucion_layout,
                            fecha_inicio_layout,
                            fecha_final_layout,
                            hora_inicio_layout,
                            hora_final_layout,
                            lugar_layout,
                            latitud_layout,
                            longitud_layout]
    return layout_fecha_lugar


#################
#
#   GEOMETRÍA
#
#################

def GeometriaLayout():
    x_layout =              [sg.T("Dimensión horizontal", size=geom_min_size),
                            sg.Spin(values=resolution_values, size=min_size, key=DIM_X_INPUT)]

    y_layout =              [sg.T("Dimensión vertical", size=geom_min_size),
                            sg.Spin(values=resolution_values, size=min_size, key=DIM_Y_INPUT)]

    curvatura_layout =      [sg.T("Radio de Curvatura", size=geom_min_size),
                            sg.Spin(values=resolution_values, size=min_size, key=CURVATURA_INPUT)]

    orientacion_layout =    [sg.T("Orientación", size=geom_min_size),
                            sg.Spin(values=resolution_values, size=min_size, key=ORIENTACION_INPUT),
                            sg.T("º")]

    layout_geometria =  [x_layout,
                        y_layout,
                        curvatura_layout,
                        orientacion_layout]
    return layout_geometria


#################
#
#   CONFIGURACIÓN DE LA CÉLULA
#
#################

def ConfigCelLayout():
    tecnologia_layout =     [sg.vtop(sg.T("Tecnología célula", size=geom_min_size)),
                            sg.Listbox(values=lista_tecnologias, default_values=lista_tecnologias[0], size=(min_width, listbox_size), 
                                no_scrollbar=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, key=TECNOLOGIA_INPUT)]

    num_cels_x_layout =     [sg.T("Número células en x", size=geom_min_size),
                            sg.Spin(values=resolution_values, expand_x=True, key=NUM_CEL_X_INPUT)]

    num_cels_y_layout =     [sg.T("Número células en y", size=geom_min_size),
                            sg.Spin(values=resolution_values, expand_x=True, key=NUM_CEL_Y_INPUT)]

    conexion_layout =       [sg.vtop(sg.T("Tipo de conexión", size=geom_min_size)),
                            sg.Listbox(values=lista_conexiones, default_values=lista_conexiones[0], size=(min_width, listbox_size), 
                                no_scrollbar=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, key=CONEXION_INPUT)]

    layout_config_cel = [tecnologia_layout,
                        num_cels_x_layout,
                        num_cels_y_layout,
                        conexion_layout]
    return layout_config_cel


#################
#
#   DATOS RADIACIÓN
#
#################

def RadiacionLayout():
    #CLEAR_SKY
    clear_sky_layout =      [[sg.Radio("Clear sky", group_id=RADIATION_TYPE_GROUP, default=True, enable_events=True, key=CLEAR_SKY)]]
    col_clear_sky = sg.Col(layout=clear_sky_layout)

    #TMY
    tmy_layout =            [[sg.Radio("Tmy", group_id=RADIATION_TYPE_GROUP, enable_events=True, key=TMY)],
                            [sg.Listbox(values=lista_tmy, size=(min_width, listbox_size), no_scrollbar=True, disabled=True, key=TMY_INPUT)]]
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


#################
#
#   DATOS PARAMETRIZACIÓN
#
#################

def ParametricLayout():
    parametric_var_layout = [sg.vtop(sg.Text("Variable parametrizable", size=param_var_size)), 
                             sg.Combo(values=parametric_keys, default_value=parametric_keys[0], 
                                      size=(min_width, listbox_size),readonly=True, key=PARAMETRIC_VAR_INPUT, enable_events=True)]
    valores_layout =        [sg.vtop(sg.Text("Valores", size=param_var_size)),
                             sg.Listbox(values=lista_azimuts, size=(min_width, listbox_size), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, 
                                        enable_events=True, key=VALUES_PARAMETRIC_INPUT)]

    layout_parametric =     [parametric_var_layout,
                            #  lim_inf_layout,
                            #  lim_sup_layout,
                            #  rango_layout,
                             valores_layout]

    return layout_parametric


#################
#
#   VISTA CONFIG STATIC SIM 
#
#################

def FrameStaticSimConfig():
    frame_fecha_lugar =         sg.Frame("Fecha y lugar", FechaYLugarLayout())
    # frame_fecha_lugar =         sg.Frame("", FechaYLugarLayout(), background_color="DarkOliveGreen3")
    frame_geometria =           sg.Frame("Geometría", GeometriaLayout(), expand_x=True, expand_y=True)
    frame_configuracion_cel =   sg.Frame("Configuración célula", ConfigCelLayout(), expand_x=True, expand_y=True)
    frame_radiacion =           sg.Frame("Datos radiación", layout=RadiacionLayout(), expand_x=True, expand_y=True)
    frame_parametrica =         sg.Frame("Datos paramétricos", layout=ParametricLayout(), expand_x=True, expand_y=True)
    generar_config_layout =     [sg.Push(), sg.Button("Generar config", size=(20,2), key=GENERAR_CONFIG), sg.Push()]
    static_sim_data_layout =    [[frame_fecha_lugar, frame_configuracion_cel, frame_geometria],
                                 [frame_radiacion, frame_parametrica],
                                 generar_config_layout]
    frame_static_sim_config =   sg.Frame("", layout=static_sim_data_layout)
    global frame_size
    frame_size = frame_static_sim_config.Size
    return frame_static_sim_config


#################
#
#   VISTA DATOS SESIÓN
#
#################

text_size = (20,2)
button_size = (30, 2)

def FrameSessionData():
    nombre_layout       = [sg.T("Nombre", size=text_size), sg.Input(key=NOMBRE_INPUT, size=text_size)]
    descripcion_layout  = [sg.vtop(sg.T("Descripción", size=text_size)), sg.Multiline(key=DESCRIPCION_INPUT, size=(50, 5))]
    config_file_layout  = [sg.T("Archivo configuración", size=text_size), 
                           sg.Input(key=CARGAR_CONFIG_INPUT, enable_events=True, visible=False),
                           sg.FileBrowse("Cargar config", target=CARGAR_CONFIG_INPUT, key=CONFIG_FILE_BROWSER, file_types=(("YAML files", "*.yaml"),)),
                           sg.Text("", auto_size_text=True, key=CONFIG_FILE_TEXT)]
    
    # todo: botón cargar sesión previa 
    load_session_layout = [sg.Input(key=CARGAR_SESION_INPUT, enable_events=True, visible=False), #solo para actualizar automáticamente
                           sg.Push(), 
                           sg.FolderBrowse(button_text="Cargar sesión previa", target=CARGAR_SESION_INPUT, size=button_size),
                           sg.Push()]
    simular_layout      = [sg.Push(), sg.Button("SIMULAR", size=button_size, key=SIMULAR_INPUT, disabled=True), sg.Push()]

    session_data_layout = [nombre_layout,
                           descripcion_layout,
                           config_file_layout,
                           [sg.VPush()],
                           load_session_layout,
                           [sg.VPush()],
                           simular_layout,
                           [sg.VPush()],]
    
    frame_session_data = sg.Frame("", session_data_layout, expand_x=True, expand_y=True)
    return frame_session_data


#################
#
#   VISTA RESULTADOS
#
#################

def FrameResults():
    test_image = IMAGES_PATH + "test_image.png"
    list_results = [RECURSO_SOLAR_TEXT, CURVAS_IV_TEXT, GEN_ELECTRICA_TEXT]
    result_layout = [[sg.Text("Variable paramétrica", size=param_var_size),
                      sg.Text("", auto_size_text=True, key=PARAM_VAR_TEXT),
                      sg.Combo(values=button_menu_hour_list, default_value=button_menu_hour_list[0], readonly=True, enable_events=True, key=VALOR_PARAMETRICA, size=param_var_size)],
                    [sg.Combo(values=list_results, default_value=list_results[0], size=param_var_size, readonly=True, enable_events=True, key=RESULTADO_INPUT),
                     sg.Image(test_image, key=RESULT_IMAGE)]]
    frame_results = sg.Frame("Resultados", result_layout, size=frame_size, key=FRAME_RESULTADOS)
    return frame_results

#################
#
#   VISTA FINAL
#
#################

def StaticSimLayout():
    back_col =              [[sg.B("Back", key=BACK)]]

    tab_sesion_layout =     [[FrameSessionData()]]
    tab_data_layout =       [[FrameStaticSimConfig()]]
    tab_results_layout =    [[FrameResults()]]
    tab_group_layout =      [[sg.Tab("Sesión", tab_sesion_layout, key=TAB_SESION),
                             sg.Tab("Configuración", tab_data_layout, key=TAB_CONFIG),
                             sg.Tab("Results", tab_results_layout, key=TAB_RESULTADOS, visible=False)]]
    
    static_sim_layout =     [[sg.TabGroup(tab_group_layout, enable_events=True, key=TAB_GRUPO)],
                             [sg.Column(back_col),]]
    
    return static_sim_layout


def VistaSimEstatica():
    global window
    window = sg.Window("FV CAR MODEL", layout=StaticSimLayout(), finalize=True, 
                       grab_anywhere_using_control=True, resizable=True)
    
    #añadir eventos
    window[RESOLUCION_INPUT].bind('<Key>', "")
    window[LONGITUD_INPUT].bind('<Button-3>', RIGHT_CLICK)
    window[LATITUD_INPUT].bind('<Button-3>', RIGHT_CLICK)
    window[NUM_CEL_X_INPUT].bind('<Key>', "")
    window[NUM_CEL_Y_INPUT].bind('<Key>', "")
    window[DIM_X_INPUT].bind('<Key>', "")
    window[DIM_Y_INPUT].bind('<Key>', "")
    window[CURVATURA_INPUT].bind('<Key>', "")
    window[ORIENTACION_INPUT].bind('<Key>', "")

#################
#
#   EVENTOS
#
#################

def mainloop():
    global tipo_datos_radiacion
    tipo_datos_radiacion = "clear sky"
    global datastaticsim
    while True:
        event, values = window.read()
        print(event)

        if event == sg.WIN_CLOSED:
            trigger = sg.WIN_CLOSED
            break

        elif event == STATIC_SIM_SELECTED:
            trigger = STATIC_SIM_SELECTED
            break

        elif event == CARGAR_CONFIG_INPUT:
            cargarConfig(values[CARGAR_CONFIG_INPUT])

        elif event == GENERAR_CONFIG:
            save_data = checkAllValues(values)
            if save_data:
                file_to_save = CONFIG_FILE_NAME
                saveStaticSimViewValuesToFile(values, file_to_save)
                window[CONFIG_FILE_TEXT].update(file_to_save)
                window[SIMULAR_INPUT].update(disabled=False)

        elif event == CARGAR_SESION_INPUT:
            cargarSesionPrevia(values[CARGAR_SESION_INPUT])

        elif event == NUM_CEL_Y_INPUT:
            result_int = acceptInput(str(values[NUM_CEL_Y_INPUT]))
            window[NUM_CEL_Y_INPUT].update(result_int)

        elif event == NUM_CEL_X_INPUT:
            result_int = acceptInput(str(values[NUM_CEL_X_INPUT]))
            window[NUM_CEL_X_INPUT].update(result_int)

        elif event == RESOLUCION_INPUT:
            result_int = acceptInput(str(values[RESOLUCION_INPUT]))
            window[RESOLUCION_INPUT].update(result_int)

        elif event == DIM_X_INPUT:
            result_int = acceptInput(str(values[DIM_X_INPUT]))
            window[DIM_X_INPUT].update(result_int)

        elif event == DIM_Y_INPUT:
            result_int = acceptInput(str(values[DIM_Y_INPUT]))
            window[DIM_Y_INPUT].update(result_int)

        elif event == ORIENTACION_INPUT:
            result_int = acceptInput(str(values[ORIENTACION_INPUT]))
            window[ORIENTACION_INPUT].update(result_int)

        elif event == DIM_X_INPUT:
            result_int = acceptInput(str(values[DIM_X_INPUT]))
            window[DIM_X_INPUT].update(result_int)

        elif event == PARAMETRIC_VAR_INPUT:
            if values[PARAMETRIC_VAR_INPUT] in dict_parametric_vars:
                window[VALUES_PARAMETRIC_INPUT].update(dict_parametric_vars[values[PARAMETRIC_VAR_INPUT]])

        #INPUTs Fecha y Lugar
        elif event == (LATITUD_INPUT + RIGHT_CLICK):
            global latitud_value
            window[LATITUD_INPUT].update(str(latitud_value))
            value = sg.popup_get_text('Enter slider value', keep_on_top=True, no_titlebar=True, grab_anywhere=True, size=(10,2))
            if (vc.ValueChecker().isStringFloat(value)):
                window[LATITUD_INPUT].update(str(value))
                latitud_value = value
            elif value is not None:
                sg.popup_error("Número introducido no válido")

        elif event == (LONGITUD_INPUT + RIGHT_CLICK):
            global longitud_value
            window[LONGITUD_INPUT].update(str(longitud_value))
            # value=  popupInValue('', 'Enter slider value')
            value = sg.popup_get_text('Enter slider value', keep_on_top=True, no_titlebar=True, grab_anywhere=True, size=(10,2))
            if (vc.ValueChecker().isStringFloat(value)):
                window[LONGITUD_INPUT].update(str(value))
                longitud_value = value
            elif value is not None:
                sg.popup_error("Número introducido no válido")


        #INPUTs Tipo Datos Radiación
        elif event == CLEAR_SKY:
            tipo_datos_radiacion = "clear sky"
            updateTipoDatosRadiacion(tipo_datos_radiacion)

        elif event == TMY:
            tipo_datos_radiacion = "tmy"
            updateTipoDatosRadiacion(tipo_datos_radiacion)

        elif event == DATA_METEO:
            tipo_datos_radiacion = "data meteo"
            updateTipoDatosRadiacion(tipo_datos_radiacion)
        

        #INPUTs Botones auxiliares
        elif event == BACK: 
            trigger = BACK
            break
        
        elif event == SIMULAR_INPUT:
            save_data = checkSession(values)
            if save_data:
                lanzarSimulacion(values)
                if result_data.status == "OK":
                    mostrarResultados()
                else:
                    sg.popup_error("Fallo en la simulación: archivo vacío")

        #INPUTs Vista Resultados
        elif event == RESULTADO_INPUT:
            updateResultTab(values[VALOR_PARAMETRICA], values[RESULTADO_INPUT])

        elif event == VALOR_PARAMETRICA:
            updateResultTab(values[VALOR_PARAMETRICA], values[RESULTADO_INPUT])


    changeState(trigger)


def cargarConfig(config_name):
    new_data = reader.readData(config_name)
    datastaticsim.FromFileToData(new_data)
    setStaticSimViewValuesFromFile(datastaticsim.GetValues())
    window[CONFIG_FILE_TEXT].update(config_name)
    window[SIMULAR_INPUT].update(disabled=False)

def cargarSesionPrevia(sesion_previa):
    name = os.path.basename(sesion_previa)
    print(name)
    window[NOMBRE_INPUT].update(name)
    config_name = sesion_previa + "/config_static_sim_data.yaml"
    if os.path.isfile(config_name):
        cargarConfig(config_name)
    else:
        sg.popup_error(f"ERROR: No existe el fichero {config_name}. Cargarlo manualmente")

    result_file = sesion_previa + "/result/" + RESULT_FILE
    if os.path.isfile(result_file):
        new_data = reader.readData(result_file)
        result_data.FromFileToData(new_data)
        mostrarResultados()
    


def generarCarpetaSesion(nombre, file_to_save):
    new_dir_name = SESSIONS_PATH + f"{nombre}/"
    new_file_name = new_dir_name + CONFIG_FILE_NAME

    if not os.path.isdir(SESSIONS_PATH):
        os.mkdir(SESSIONS_PATH)
        
    if not os.path.isdir(new_dir_name):
        os.mkdir(new_dir_name)
        shutil.copy(file_to_save, new_dir_name)

    return new_dir_name

def lanzarSimulacion(values):
    file_to_save = window[CONFIG_FILE_TEXT].get()

    new_dir_name = generarCarpetaSesion(values[NOMBRE_INPUT], file_to_save)
    args = [file_to_save, new_dir_name]
    subprocess.run([ANACONDA_EXECUTE, MODEL_SCRIPT] + args)
    
    result_file = new_dir_name + "result/" + RESULT_FILE
    if os.path.isfile(result_file):
        new_data = reader.readData(result_file)
        result_data.FromFileToData(new_data)

    else:
        sg.popup_error("Fallo en la simulación: no se generó el archivo de resultados")

def mostrarResultados():
    parametric_var = result_data.parametric_var
    global dict_results
    if parametric_var == "azimut":
        window[PARAM_VAR_TEXT].update(result_data.parametric_var)
        dict_results = result_data.azimut

    elif parametric_var == "connection":
        window[PARAM_VAR_TEXT].update(result_data.parametric_var)
        dict_results = result_data.connection

    else:
        sg.popup_error(f"ERROR: variable paramétrica {parametric_var} no contemplada")
        return

    list_keys = []
    for key, val in dict_results.items():
        list_keys.append(key)

    if len(list_keys) > 0:
        window[VALOR_PARAMETRICA].update(values=list_keys, value=list_keys[0])
        valor_previo = window[RESULTADO_INPUT].get()
        updateResultTab(list_keys[0], valor_previo)

    window[TAB_RESULTADOS].update(visible=True)
    window[TAB_RESULTADOS].select()


def generateDateIsoformat(fecha, hora, min):
    """""
    fecha: viene ya en formato YYYY-MM-DD
    hora: int
    min: int
    return: date en formato 'YYYY-MM-DDTHH:mm:ss'
    """""
    hora_str = str(hora)
    min_str = str(min)
    if hora < 10:
        hora_str = f'{hora:02d}'
    if min < 10:
        min_str = f'{min:02d}'
    
    dateStr = f"{fecha}T{hora_str}:{min_str}:00"
    if vc.ValueChecker().isStringDateIsoformat(dateStr):
        date = datetime.datetime.fromisoformat(dateStr)
        return date.isoformat()
    else:
        return None

def setStaticSimViewValuesFromFile(data):
    # print(data)
    window[RESOLUCION_INPUT].update(data["resolucion"])

    datetimeStart = datetime.datetime.fromisoformat(data["fecha_inicio"])
    datetimeEnd = datetime.datetime.fromisoformat(data["fecha_fin"])

    window[FECHA_INICIO].update(datetimeStart.date().isoformat())
    window[FECHA_FIN].update(datetimeEnd.date().isoformat())

    window[HORA_INICIO_INPUT].update(value=datetimeStart.hour)
    window[MINUTO_INICIO_INPUT].update(value=datetimeStart.minute)
    window[HORA_FINAL_INPUT].update(value=datetimeEnd.hour)
    window[MINUTO_FINAL_INPUT].update(value=datetimeEnd.minute)

    window[LUGAR_INPUT].update(data["lugar"])
    window[LATITUD_INPUT].update(data["latitud"])
    window[LONGITUD_INPUT].update(data["longitud"])
    window[DIM_X_INPUT].update(data["x"])
    window[DIM_Y_INPUT].update(data["y"])
    window[CURVATURA_INPUT].update(data["curvatura"])
    window[ORIENTACION_INPUT].update(data["orientacion"])
    tec_index = vc.ValueChecker().findValueInList(lista_tecnologias, data["tecnologia"])
    window[TECNOLOGIA_INPUT].update(set_to_index=tec_index)
    window[NUM_CEL_X_INPUT].update(data["num_cels_x"])
    window[NUM_CEL_Y_INPUT].update(data["num_cels_y"])
    con_index = vc.ValueChecker().findValueInList(lista_conexiones, data["conexion"])
    window[CONEXION_INPUT].update(set_to_index=con_index)
    tipo_datos_radiacion = data["tipo_datos_radiacion"]
    updateTipoDatosRadiacion(tipo_datos_radiacion=tipo_datos_radiacion)

    var_parametrica = data["var_parametrica"]
    if var_parametrica in dict_parametric_vars:
        par_index = vc.ValueChecker().findValueInList(parametric_keys, var_parametrica)
        window[PARAMETRIC_VAR_INPUT].update(set_to_index=par_index)
        window[VALUES_PARAMETRIC_INPUT].update(dict_parametric_vars[var_parametrica])
        window[VALUES_PARAMETRIC_INPUT].set_value(data["valores_parametrica"])
    else:
        sg.popup_error(f"ERROR al cargar archivo de configuración: variable paramétrica {var_parametrica} no se reconoce")

def saveStaticSimViewValuesToFile(data, file_to_save):
    datastaticsim = dss.DataStaticSim(resolucion=data[RESOLUCION_INPUT],
        fecha_inicio=fecha_inicio_timestamp,
        fecha_fin=fecha_fin_timestamp,
        lugar=data[LUGAR_INPUT],
        latitud=data[LATITUD_INPUT],
        longitud=data[LONGITUD_INPUT],
        x=data[DIM_X_INPUT],
        y=data[DIM_Y_INPUT],
        curvatura=data[CURVATURA_INPUT],
        orientacion=data[ORIENTACION_INPUT],
        tecnologia=data[TECNOLOGIA_INPUT][0],
        num_cels_x=data[NUM_CEL_X_INPUT],
        num_cels_y=data[NUM_CEL_Y_INPUT],
        conexion=data[CONEXION_INPUT][0],
        tipo_datos_radiacion=tipo_datos_radiacion,
        datos_radiacion="",
        var_parametrica=data[PARAMETRIC_VAR_INPUT],
        # lim_sup=data[LIM_SUP_INPUT],
        # lim_inf=data[LIM_INF_INPUT],
        # rango=data[RANGO_INPUT],
        valores_parametricos=data[VALUES_PARAMETRIC_INPUT])

    writer.writeData(file_to_save, datastaticsim.FromDataToFile())

#Máquina Estados

def changeState(trigger):
    global window
    global state

    if state == EstadosVistas.Init:
        if trigger == INIT_SIMULATION:
            state = EstadosVistas.VistaSimulaciones
            VistaSimulaciones()

    if state == EstadosVistas.VistaSimulaciones:
        if trigger == STATIC_SIM_SELECTED:
            state = EstadosVistas.VistaSimEstatica
            window.close()
            VistaSimEstatica()

        # if trigger == DYNAMIC_SIM_SELECTED:
        #     window.close()
        #     VistaSimDinamica()

    if state == EstadosVistas.VistaSimEstatica:
        if trigger == BACK:
            state = EstadosVistas.VistaSimulaciones
            window.close()
            VistaSimulaciones()

    if trigger != sg.WIN_CLOSED:
        mainloop()
        return True

    return False

def updateTipoDatosRadiacion(tipo_datos_radiacion):
    if tipo_datos_radiacion == "clear sky":
        window[CLEAR_SKY].reset_group()
        window[CLEAR_SKY].update(value=True)
        window[TMY_INPUT].update(disabled=True)
        window[DATA_METEO_INPUT].update(disabled=True)
        window[DATA_METEO_BROWSER].update(disabled=True)

    elif tipo_datos_radiacion == "tmy":
        window[TMY].reset_group()
        window[TMY].update(value=True)
        window[TMY_INPUT].update(disabled=False)
        window[DATA_METEO_INPUT].update(disabled=True)
        window[DATA_METEO_BROWSER].update(disabled=True)

    elif tipo_datos_radiacion == "data meteo":
        window[DATA_METEO].reset_group()
        window[DATA_METEO].update(value=True)
        window[TMY_INPUT].update(disabled=True)
        window[DATA_METEO_INPUT].update(disabled=False)
        window[DATA_METEO_BROWSER].update(disabled=False)

def updateResultTab(valor_sel, select_grafica):
    imagen = ""
    if valor_sel in dict_results:
        if select_grafica in dict_results[valor_sel]:
            imagen = dict_results[valor_sel][select_grafica]
    updateResultImage(imagen)

def updateResultImage(image):
    print(image)
    if os.path.isfile(image):
        window[RESULT_IMAGE].update(image)
    else:
        sg.popup_error(f"ERROR: imagen {image} no existe")


def checkAllValues(values):
    ret = True
    
    global fecha_inicio_timestamp
    fecha_inicio_timestamp = generateDateIsoformat(window[FECHA_INICIO].get(), values[HORA_INICIO_INPUT], values[MINUTO_INICIO_INPUT])
    if fecha_inicio_timestamp is None:
        sg.popup_error("Fecha y hora de inicio introducidas no válida")
        ret = False
    
    global fecha_fin_timestamp
    fecha_fin_timestamp = generateDateIsoformat(window[FECHA_FIN].get(), values[HORA_FINAL_INPUT], values[MINUTO_FINAL_INPUT])
    if fecha_fin_timestamp is None:
        ret = False
        sg.popup_error("Fecha y hora de fin introducidas no válida")
    
    return ret

def checkSession(values):
    ret = True
    if not values[NOMBRE_INPUT]:
        ret = False
        sg.popup_error("ERROR: introducir nombre de la sesión")
    if checkAllValues(values) == False:
        ret = False
    
    return ret

def acceptInput(value):
    result = ""
    i = 0
    for i in range(len(value)):
        if (vc.ValueChecker().isStringInt(value[i])):
            result = result + value[i]
    if (result == ""):
        result = "0"
    result_int = int(result)
    return result_int

if __name__ == "__main__":
    print("MAIN")
    datastaticsim = dss.DataStaticSim()
    result_data = rd.ResultData()
    writer = YAMLWriter()
    reader = YAMLReader()
    state = EstadosVistas.Init
    changeState(INIT_SIMULATION)

#todo: set data_radiacion