import PySimpleGUI as sg
import re
from DataStaticSim import *
from EstadosVistas import EstadosVistas
from YAMLAdapter import YAMLReader, YAMLWriter
from KeyDefines import *
from ValueChecker import *
import datetime

#################
#   DEFINES
#################
resolution_values = []
for i in range(10000):
    resolution_values.append(i)

button_menu_hour_start_str = "00"
button_menu_minute_start_str = "00"
button_menu_hour_end_str = "00"
button_menu_minute_end_str = "00"
button_menu_hour_list = []
button_menu_minute_list = []
for i in range(24):
    button_menu_hour_list.append(f'{i:02d}')

for i in range(60):
    button_menu_minute_list.append(f'{i:02d}')

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

listbox_size = 5

lista_tecnologias = ("DSC", "CIS", "CdTe", "a-Si", "TF-Si")
lista_conexiones = ("Paralelo", "Serie", "Combinada")

lista_tmy = ("DB1", "DB2", "DB3")

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

def splitHour(hour):
    ret = "00"
    patron = re.compile(":")
    splitlist = patron.split(hour)
    if splitlist != None:
        ret = splitlist

    print(ret)
    return ret

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
#   VISTA DATOS STATIC SIM
#
#################

def FrameStaticSimData():
    frame_fecha_lugar =         sg.Frame("Fecha y lugar", FechaYLugarLayout())
    # frame_fecha_lugar =         sg.Frame("", FechaYLugarLayout(), background_color="DarkOliveGreen3")
    frame_geometria =           sg.Frame("Geometría", GeometriaLayout(), expand_x=True, expand_y=True)
    frame_configuracion_cel =   sg.Frame("Configuración célula", ConfigCelLayout(), expand_x=True, expand_y=True)
    frame_radiacion =           sg.Frame("Datos radiación", layout=RadiacionLayout())
    static_sim_data_layout =    [[frame_fecha_lugar, frame_configuracion_cel, frame_geometria],
                                [frame_radiacion]]
    frame_static_sim_data =     sg.Frame("", layout=static_sim_data_layout)
    return frame_static_sim_data


#################
#
#   VISTA FINAL
#
#################

def StaticSimLayout():
    back_col =              [[sg.B("Back", key=BACK)]]

    tipo_res_col =          [[sg.T("Tipo Simulación", size=geom_min_size)],
                            [sg.Checkbox("Recurso solar", key=RECURSO_SOLAR_INPUT)],
                            [sg.Checkbox("Curvas IV", key=CURVAS_IV_INPUT)],
                            [sg.Checkbox("Generación Eléctrica", key=GEN_ELECTRICA_INPUT)]]

    acciones_sim_col =      [[sg.B("Guardar", size=min_size, key=GUARDAR_INPUT)],
                            [sg.B("Cargar datos", size=min_size, key=CARGAR_DATOS_INPUT)],
                            [sg.B("Simular", size=min_size, key=SIMULAR_INPUT)]]

    static_sim_layout =     [[FrameStaticSimData()],
                            [sg.Column(back_col),
                            sg.Push(),
                            sg.Column(tipo_res_col),
                            sg.Push(),
                            sg.Column(acciones_sim_col)]]
    return static_sim_layout


def random(event):
    print("random")
    print(event.char)
    return event.char

def VistaSimEstatica():
    global window
    # window = sg.Window("FV CAR MODEL", layout=StaticSimLayout(), finalize=True, background_color="DarkSlateGray3")
    window = sg.Window("FV CAR MODEL", layout=StaticSimLayout(), finalize=True)
    
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

        #INPUTs Fecha y Lugar
        elif event == (LATITUD_INPUT + RIGHT_CLICK):
            global latitud_value
            window[LATITUD_INPUT].update(str(latitud_value))
            value = sg.popup_get_text('Enter slider value', keep_on_top=True, no_titlebar=True, size=(10,2))
            if (ValueChecker().isStringFloat(value)):
                window[LATITUD_INPUT].update(str(value))
                latitud_value = value
            elif value is not None:
                sg.popup_error("Número introducido no válido")

        elif event == (LONGITUD_INPUT + RIGHT_CLICK):
            global longitud_value
            window[LONGITUD_INPUT].update(str(longitud_value))
            # value=  popupInValue('', 'Enter slider value')
            value = sg.popup_get_text('Enter slider value', keep_on_top=True, no_titlebar=True, size=(10,2))
            if (ValueChecker().isStringFloat(value)):
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
        
        elif event == GUARDAR_INPUT:
            save_data = checkAllValues(values)
            if save_data:
                datastaticsim = DataStaticSim(resolucion=values[RESOLUCION_INPUT],
                    fecha_inicio=fecha_inicio_timestamp,
                    fecha_fin=fecha_fin_timestamp,
                    lugar=values[LUGAR_INPUT],
                    latitud=values[LATITUD_INPUT],
                    longitud=values[LONGITUD_INPUT],
                    x=values[DIM_X_INPUT],
                    y=values[DIM_Y_INPUT],
                    curvatura=values[CURVATURA_INPUT],
                    orientacion=values[ORIENTACION_INPUT],
                    tecnologia=values[TECNOLOGIA_INPUT][0],
                    num_cels_x=values[NUM_CEL_X_INPUT],
                    num_cels_y=values[NUM_CEL_Y_INPUT],
                    conexion=values[CONEXION_INPUT][0],
                    tipo_datos_radiacion=tipo_datos_radiacion,
                    datos_radiacion="")
                writer.writeData("D:\GUI FV CAR\model1\src\static_sim_data.yaml", datastaticsim.FromDataToFile())
        
        elif event == CARGAR_DATOS_INPUT:
            #esto debería abrir un browser
            #D:\GUI FV CAR\model1\src
            new_data = reader.readData("D:\GUI FV CAR\model1\src\\test.yaml")
            datastaticsim.FromFileToData(new_data)
            setStaticSimViewValuesFromFile(datastaticsim.GetValues())

    changeState(trigger)

def generateDateIsoformat(fecha, hora, min):
    """""
    fecha: viene ya en formato YYYY-MM-DD
    hora: viene en formato HH
    min: viene en formato MM
    return: date en formato YYYY-MM-DDTHH:mm:ss
    """""
    checker = ValueChecker()
    dateStr = f"{fecha}T{hora}:{min}:00"
    print(dateStr)
    if checker.isStringDateIsoformat(dateStr):
        date = datetime.datetime.fromisoformat(dateStr)
        return date.isoformat()
    else:
        return None

def setStaticSimViewValuesFromFile(data):
    print(data)

    window[RESOLUCION_INPUT].update(data["resolucion"])
    window[FECHA_INICIO].update(data["fecha_inicio"])
    window[FECHA_FIN].update(data["fecha_fin"])

    hora_y_min_start = splitHour(data["hora_inicio"])
    window[HORA_INICIO_INPUT].update(value=hora_y_min_start[0])
    window[MINUTO_INICIO_INPUT].update(value=hora_y_min_start[1])

    hora_y_min_end = splitHour(data["hora_fin"])
    window[HORA_FINAL_INPUT].update(value=hora_y_min_end[0])
    window[MINUTO_FINAL_INPUT].update(value=hora_y_min_end[1])

    window[LUGAR_INPUT].update(data["lugar"])
    window[LATITUD_INPUT].update(data["latitud"])
    window[LONGITUD_INPUT].update(data["longitud"])
    window[DIM_X_INPUT].update(data["x"])
    window[DIM_Y_INPUT].update(data["y"])
    window[CURVATURA_INPUT].update(data["curvatura"])
    window[ORIENTACION_INPUT].update(data["orientacion"])
    tec_index = ValueChecker().findValueInList(lista_tecnologias, data["tecnologia"])
    window[TECNOLOGIA_INPUT].update(set_to_index=tec_index)
    window[NUM_CEL_X_INPUT].update(data["num_cels_x"])
    window[NUM_CEL_Y_INPUT].update(data["num_cels_y"])
    con_index = ValueChecker().findValueInList(lista_conexiones, data["conexion"])
    window[CONEXION_INPUT].update(set_to_index=con_index)
    global tipo_datos_radiacion
    tipo_datos_radiacion = data["tipo_datos_radiacion"]
    updateTipoDatosRadiacion(tipo_datos_radiacion=tipo_datos_radiacion)


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
    
    checker = ValueChecker()
    if checker.isStringUInt(str(values[RESOLUCION_INPUT])) == False:
        sg.popup_error("Error en los datos introducidos: " + RESOLUCION_INPUT + ": solo acepta números enteros")
        ret = False

    if checker.isStringUInt(str(values[NUM_CEL_X_INPUT])) == False:
        sg.popup_error("Error en los datos introducidos: " + NUM_CEL_X_INPUT + ": solo acepta números enteros")
        ret = False

    if checker.isStringUInt(str(values[NUM_CEL_Y_INPUT])) == False:
        sg.popup_error("Error en los datos introducidos: " + NUM_CEL_Y_INPUT + ": solo acepta números enteros")
        ret = False

    if checker.isStringUInt(str(values[DIM_X_INPUT])) == False:
        sg.popup_error("Error en los datos introducidos: " + DIM_X_INPUT + ": solo acepta números enteros")
        ret = False
    if checker.isStringUInt(str(values[DIM_Y_INPUT])) == False:
        sg.popup_error("Error en los datos introducidos: " + DIM_Y_INPUT + ": solo acepta números enteros")
        ret = False
    
    return ret

def acceptInput(value):
    result = ""
    i = 0
    for i in range(len(value)):
        if (ValueChecker().isStringInt(value[i])):
            result = result + value[i]
    if (result == ""):
        result = "0"
    result_int = int(result)
    return result_int

if __name__ == "__main__":
    print("MAIN")
    datastaticsim = DataStaticSim()
    writer = YAMLWriter()
    reader = YAMLReader()
    state = EstadosVistas.Init
    changeState(INIT_SIMULATION)

    #todo: comprobar que todos los valores son válidos
    #todo: pestaña error si los valores introducidos no son válidos
    #todo: mejorar visibilidad pop up
    #todo: set data_radiacion