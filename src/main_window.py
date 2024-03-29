import os
import shutil
import subprocess
import threading
import datetime
import io
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasAgg
import PySimpleGUI as sg
import ValueChecker as vc
import DataStaticSim as dss
import ResultData as rd
import ConnectionDataReader as cdr
from EstadosVistas import EstadosVistas
from YAMLAdapter import YAMLReader, YAMLWriter
from KeyDefines import *

from vistas.vistaConfiguracion import vistaConfigStaticSim
from vistas.vistaSesiones import vistaSesiones
from vistas.vistaResultados import windowResults

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

param_var_size = (20, 1)

#   LISTAS AUXILIARES
lista_azimuts = []
for i in range(91):
    if (i % 5) == 0:
        lista_azimuts.append(i)

dict_parametric_vars = {"no_parametrica" : [],
                        "azimut" : lista_azimuts,
                        "connection" : LISTA_CONEXIONES}
parametric_keys = []
for key in dict_parametric_vars:
    parametric_keys.append(key)

global dict_results
dict_results = {}

latitud_value = 0
longitud_value = 0

fecha_inicio_timestamp = ""
fecha_fin_timestamp = ""

frameSize = []

#############################################
#   VISTA SIMULACIONES
#############################################

def SimulationsLayout():
    simulations_layout =    [[sg.B("Simulación Estática", size=MIN_BUTTON_SIZE, key=STATIC_SIM_SELECTED)],
                            [sg.B("Simulación Dinámica", size=MIN_BUTTON_SIZE, disabled=True)]]
    return simulations_layout

def VistaSimulaciones():
    global main_window
    main_window = sg.Window("FV CAR MODEL", layout=SimulationsLayout(), element_padding=(200,50), finalize=True)


#############################################
#   VISTA SIMULACIÓN ESTÁTICA
#############################################

def ResultWindow():
    global result_data
    list_moments = result_data_reader.getMoments(result_data.firstConnection(), result_data.firstAzimut(), RECURSO_SOLAR_TEXT)

    return windowResults(result_data, list_moments, frameSize)

#################
#
#   VISTA FINAL
#
#################

def StaticSimLayout():
    back_col =              [[sg.B("Back", key=BACK)]]

    tab_sesion_layout =     [[vistaSesiones(parametric_keys, lista_azimuts)]]
    tab_data_layout =       [[vistaConfigStaticSim(resolution_values, button_menu_hour_list, button_menu_minute_list, lista_azimuts, frameSize)]]
    tab_group_layout =      [[sg.Tab("Sesión", tab_sesion_layout, key=TAB_SESION),
                             sg.Tab("Configuración", tab_data_layout, key=TAB_CONFIG),
                             ]]
    
    static_sim_layout =     [[sg.TabGroup(tab_group_layout, enable_events=True, key=TAB_GRUPO)],
                             [sg.Column(back_col),]]
    
    return static_sim_layout


def VistaSimEstatica():
    global main_window
    main_window = sg.Window("FV CAR MODEL", layout=StaticSimLayout(), finalize=True, 
                       grab_anywhere_using_control=True, resizable=True)
    
    #añadir eventos
    main_window[RESOLUCION_INPUT].bind('<Key>', "")
    main_window[LONGITUD_INPUT].bind('<Button-3>', RIGHT_CLICK)
    main_window[LATITUD_INPUT].bind('<Button-3>', RIGHT_CLICK)
    main_window[NUM_CEL_X_INPUT].bind('<Key>', "")
    main_window[NUM_CEL_Y_INPUT].bind('<Key>', "")
    main_window[DIM_X_INPUT].bind('<Key>', "")
    main_window[DIM_Y_INPUT].bind('<Key>', "")
    main_window[CURVATURA_INPUT].bind('<Key>', "")
    main_window[ORIENTACION_INPUT].bind('<Key>', "")
    main_window[AZIMUT_INPUT].bind('<Key>', "")

#################
#
#   EVENTOS
#
#################

def mainloop():
    global tipo_datos_radiacion
    global datastaticsim
    global result_window
    tipo_datos_radiacion = "clear sky"

    while True:
        window, event, values = sg.read_all_windows()
        print(event)

        if event == sg.WIN_CLOSED:
            window.close()
            if window == result_window:
                result_window = None
            elif window == main_window:
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
                main_window[CONFIG_FILE_TEXT].update(file_to_save)
                main_window[SIMULAR_INPUT].update(disabled=False)

                sg.popup_ok(f"Archivo de configuración \"{file_to_save}\" generado correctamente")

        elif event == CARGAR_SESION_INPUT:
            cargarSesionPrevia(values[CARGAR_SESION_INPUT])

        elif event == FECHA_INICIO_INPUT:
            main_window[FECHA_INICIO].update(formatCalendarDate(sg.popup_get_date(close_when_chosen=True)))

        elif event == FECHA_FIN_INPUT:
            main_window[FECHA_FIN].update(formatCalendarDate(sg.popup_get_date(close_when_chosen=True)))

        elif event == NUM_CEL_Y_INPUT:
            result_int = acceptInput(str(values[NUM_CEL_Y_INPUT]))
            main_window[NUM_CEL_Y_INPUT].update(result_int)

        elif event == NUM_CEL_X_INPUT:
            result_int = acceptInput(str(values[NUM_CEL_X_INPUT]))
            main_window[NUM_CEL_X_INPUT].update(result_int)

        elif event == RESOLUCION_INPUT:
            result_int = acceptInput(str(values[RESOLUCION_INPUT]))
            main_window[RESOLUCION_INPUT].update(result_int)

        elif event == DIM_X_INPUT:
            result_int = acceptInput(str(values[DIM_X_INPUT]))
            main_window[DIM_X_INPUT].update(result_int)

        elif event == DIM_Y_INPUT:
            result_int = acceptInput(str(values[DIM_Y_INPUT]))
            main_window[DIM_Y_INPUT].update(result_int)

        elif event == CURVATURA_INPUT:
            result_int = acceptInput(str(values[CURVATURA_INPUT]))
            main_window[CURVATURA_INPUT].update(result_int)

        elif event == ORIENTACION_INPUT:
            result_int = acceptInput(str(values[ORIENTACION_INPUT]))
            main_window[ORIENTACION_INPUT].update(result_int)

        elif event == AZIMUT_INPUT:
            result_int = acceptInput(str(values[AZIMUT_INPUT]))
            main_window[AZIMUT_INPUT].update(result_int)

        elif event == DIM_X_INPUT:
            result_int = acceptInput(str(values[DIM_X_INPUT]))
            main_window[DIM_X_INPUT].update(result_int)

        elif event == ENABLE_PARAMETRIC_INPUT:
            enabled = values[ENABLE_PARAMETRIC_INPUT]
            main_window[PARAMETRIC_VAR_INPUT].update(disabled=not enabled)
            main_window[VALUES_PARAMETRIC_INPUT].update(disabled=not enabled)


        elif event == PARAMETRIC_VAR_INPUT:
            if values[PARAMETRIC_VAR_INPUT] in dict_parametric_vars:
                main_window[VALUES_PARAMETRIC_INPUT].update(dict_parametric_vars[values[PARAMETRIC_VAR_INPUT]])

        #INPUTs Fecha y Lugar
        elif event == (LATITUD_INPUT + RIGHT_CLICK):
            global latitud_value
            main_window[LATITUD_INPUT].update(str(latitud_value))
            value = sg.popup_get_text('Enter slider value', keep_on_top=True, no_titlebar=True, grab_anywhere=True, size=(10,2))
            if (vc.ValueChecker().isStringFloat(value)):
                main_window[LATITUD_INPUT].update(str(value))
                latitud_value = value
            elif value is not None:
                sg.popup_error("Número introducido no válido")

        elif event == (LONGITUD_INPUT + RIGHT_CLICK):
            global longitud_value
            main_window[LONGITUD_INPUT].update(str(longitud_value))
            value = sg.popup_get_text('Enter slider value', keep_on_top=True, no_titlebar=True, grab_anywhere=True, size=(10,2))
            if (vc.ValueChecker().isStringFloat(value)):
                main_window[LONGITUD_INPUT].update(str(value))
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
            if result_window != None:
                result_window.close()
                result_window = None
            break
        
        elif event == SIMULAR_INPUT:
            save_data = checkSession(values)
            if save_data:
                lanzarSimulacion(main_window[CONFIG_FILE_TEXT].get(), values[NOMBRE_INPUT], values[DESCRIPCION_INPUT])

        elif event == GENERAR_GRAFICA_INPUT:
            image_connection, image_azimut = getImagesValues(values)
            image = result_data_reader.generateImage(image_connection, image_azimut, values[RESULTADO_INPUT], values[MOMENTO_INPUT][0])
            draw_image(window[RESULT_IMAGE], image)
        
        elif event == RESULTADO_INPUT:
            image_connection, image_azimut = getImagesValues(values)
            if values[RESOLUCION_HORARIA]:
                updateMomentsFrame(RESOLUCION_HORARIA, values[RESULTADO_INPUT], image_connection, image_azimut)
            elif values[RESOLUCION_DIARIA]:
                updateMomentsFrame(RESOLUCION_DIARIA, values[RESULTADO_INPUT], image_connection, image_azimut)
            elif values[RESOLUCION_MENSUAL]:
                updateMomentsFrame(RESOLUCION_MENSUAL, values[RESULTADO_INPUT], image_connection, image_azimut)

        elif event == RESOLUCION_HORARIA or event == RESOLUCION_DIARIA or event == RESOLUCION_MENSUAL:
            image_connection, image_azimut = getImagesValues(values)
            updateMomentsFrame(event, values[RESULTADO_INPUT], image_connection, image_azimut)

    changeState(trigger)

def draw_image(element, figure):
    """
    Draws the previously created "figure" in the supplied Image Element
    :param element: an Image Element
    :param figure: a Matplotlib figure
    :return: The figure canvas
    """

    plt.close('all')        # erases previously drawn plots
    canv = FigureCanvasAgg(figure)
    buf = io.BytesIO()
    canv.print_figure(buf, format='png')
    if buf is None:
        return None
    buf.seek(0)
    element.update(data=buf.read())
    return canv

def cargarConfig(config_name):
    new_data = reader.readData(config_name)
    load_ok = datastaticsim.FromFileToData(new_data)
    if load_ok:
        setStaticSimViewValuesFromFile(datastaticsim.GetValues())
        main_window[CONFIG_FILE_TEXT].update(config_name)
        main_window[SIMULAR_INPUT].update(disabled=False)
    else:
        sg.popup_error("ERROR al cargar el archivo de configuración")

def cargarSesionPrevia(sesion_previa):
    name = os.path.basename(sesion_previa)
    print(name)
    main_window[NOMBRE_INPUT].update(name)
    config_name = sesion_previa + "/config_static_sim_data.yaml"
    if os.path.isfile(config_name):
        cargarConfig(config_name)

        description_file = sesion_previa + "/descripcion.txt"
        if os.path.isfile(description_file):
            leerDescripcion(description_file)

        result_file = sesion_previa + "/result/" + RESULT_FILE
        if os.path.isfile(result_file):
            new_data = reader.readData(result_file)
            global result_data
            result_data = rd.ResultDataCreator().createDataFromFile(new_data)
            if result_data is not None:
                choice = popUpSesionYaGenerada()
                if choice == VER_RESULTADOS_OPTION:
                    mostrarResultados()
                elif choice == RELANZAR_SIM_OPTION:
                    lanzarSimulacion(main_window[CONFIG_FILE_TEXT].get(), main_window[NOMBRE_INPUT].get(), main_window[DESCRIPCION_INPUT].get())
                else:
                    sg.popup_error(f"ERROR: Opción de simulación {choice} inválida")
            else:
                sg.popup_error(f"ERROR: archivo de resultados de la simulación vacío")
    else:
        sg.popup_error(f"ERROR: No existe el fichero {config_name}. Cargarlo manualmente")



def formatCalendarDate(date):
    #format="%Y-%m-%d"
    ret = ""
    month = date[0]
    day = date[1]
    year = date[2]
    ret = f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
    return ret

def popUpSesionYaGenerada():
    layout_choice = [[sg.T('Sesión ya generada')],
                     [sg.B(VER_RESULTADOS_OPTION, size=MIN_BUTTON_SIZE), sg.B(RELANZAR_SIM_OPTION, size=MIN_BUTTON_SIZE)]]
    choice = sg.Window('Sesión ya generada', layout=layout_choice, disable_close=True, keep_on_top=True).read(close=True)
    print(choice[0])
    return choice[0]


def generarCarpetaSesion(nombre, file_to_save):
    new_dir_name = SESSIONS_PATH + f"{nombre}/"
    new_file_name = new_dir_name + CONFIG_FILE_NAME

    if not os.path.isdir(SESSIONS_PATH):
        os.mkdir(SESSIONS_PATH)
        
    if not os.path.isdir(new_dir_name):
        os.mkdir(new_dir_name)
        shutil.copy(file_to_save, new_dir_name)

    return new_dir_name

def callSubprocess(*args):
    print(args)
    print("------------- INICIO DE LA SIMULACIÓN -------------")
    subprocess.run([ANACONDA_EXECUTE, *args])
    print("--------------- FIN DE LA SIMULACIÓN ---------------")
    global subprocess_completed
    subprocess_completed = True
    print("subprocess_completed: ", subprocess_completed)
    return

def animateGIF(gif, close=False):
    if close:
        gif = None
    prev_theme = sg.theme()
    sg.theme("DarkGrey")
    sg.PopupAnimated(image_source=gif, message="Cargando...", time_between_frames=100)
    sg.theme(prev_theme)

def loadingScreen(args):
    load_img = IMAGES_PATH + "loading.gif"
    load_win = sg.Window(title="Simulación en curso", layout=[[sg.T("Cargando")]], ttk_theme="DarkGrey")

    global subprocess_completed
    subprocess_completed = False
    subprocess_thread = threading.Thread(target=callSubprocess, args=args)
    subprocess_thread.start()
    
    while not subprocess_completed:
        event, values = load_win.Read(timeout=100)

        if event == sg.WIN_CLOSED:
            trigger = sg.WIN_CLOSED
            break
        else:
            animateGIF(load_img)
    
    subprocess_thread.join()
    load_win.close()
    animateGIF(load_img, close=True)

def lanzarSimulacion(config_file, session_name, description):   #Config_file, session_name, description
    file_to_save = config_file
    new_dir_name = generarCarpetaSesion(session_name, file_to_save)
    args = [MODEL_SCRIPT, file_to_save, new_dir_name]
    loadingScreen(args)
    guardarDescripcion(description, new_dir_name + "descripcion.txt")

    result_file = new_dir_name + "result/" + RESULT_FILE
    if os.path.isfile(result_file):
        global result_data
        result_data = rd.ResultDataCreator().createDataFromFile(reader.readData(result_file))

        if result_data.status == "OK":
            mostrarResultados()
        else:
            sg.popup_error("Fallo en la simulación: archivo vacío")
    else:
        sg.popup_error("Fallo en la simulación: no se generó el archivo de resultados")

def guardarDescripcion(descripcion, description_file):
    f = open(description_file, "w")
    f.write(descripcion)
    f.close()

def leerDescripcion(description_file):
    f = open(description_file, "r")
    descripcion = f.read()
    print(descripcion)
    main_window[DESCRIPCION_INPUT].update(descripcion)
    f.close()

def mostrarResultados():
    print("\nMOSTRAR RESULTADOS\n")
    global dict_results

    global result_window
    #cerrar ventana result_window y volver a crearla
    if result_window == None:
        result_window = ResultWindow()


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
    main_window[RESOLUCION_INPUT].update(data["resolucion"])

    datetimeStart = datetime.datetime.fromisoformat(data["fecha_inicio"])
    datetimeEnd = datetime.datetime.fromisoformat(data["fecha_fin"])

    main_window[FECHA_INICIO].update(datetimeStart.date().isoformat())
    main_window[FECHA_FIN].update(datetimeEnd.date().isoformat())

    main_window[HORA_INICIO_INPUT].update(value=datetimeStart.hour)
    main_window[MINUTO_INICIO_INPUT].update(value=datetimeStart.minute)
    main_window[HORA_FINAL_INPUT].update(value=datetimeEnd.hour)
    main_window[MINUTO_FINAL_INPUT].update(value=datetimeEnd.minute)

    main_window[LUGAR_INPUT].update(data["lugar"])
    main_window[LATITUD_INPUT].update(data["latitud"])
    main_window[LONGITUD_INPUT].update(data["longitud"])
    main_window[DIM_X_INPUT].update(data["x"])
    main_window[DIM_Y_INPUT].update(data["y"])
    main_window[CURVATURA_INPUT].update(data["curvatura"])
    main_window[ORIENTACION_INPUT].update(data["orientacion"])
    main_window[AZIMUT_INPUT].update(data["azimut"])
    tec_index = vc.ValueChecker().findValueInList(LISTA_TECNOLOGIAS, data["tecnologia"])
    main_window[TECNOLOGIA_INPUT].update(set_to_index=tec_index)
    main_window[NUM_CEL_X_INPUT].update(data["num_cels_x"])
    main_window[NUM_CEL_Y_INPUT].update(data["num_cels_y"])
    con_index = vc.ValueChecker().findValueInList(LISTA_CONEXIONES, data["conexion"])
    main_window[CONEXION_INPUT].update(set_to_index=con_index)
    tipo_datos_radiacion = data["tipo_datos_radiacion"]
    updateTipoDatosRadiacion(tipo_datos_radiacion=tipo_datos_radiacion)

    var_parametrica = data["var_parametrica"]
    if var_parametrica in dict_parametric_vars or var_parametrica == "no_parametrica" :
        par_index = vc.ValueChecker().findValueInList(parametric_keys, var_parametrica)
        main_window[PARAMETRIC_VAR_INPUT].update(set_to_index=par_index)
        main_window[VALUES_PARAMETRIC_INPUT].update(dict_parametric_vars[var_parametrica])
        if len(data["valores_parametrica"]) != 0:
            main_window[VALUES_PARAMETRIC_INPUT].set_value(data["valores_parametrica"])
            main_window[ENABLE_PARAMETRIC_INPUT].update(True)
            main_window.write_event_value(ENABLE_PARAMETRIC_INPUT, True)
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
        azimut=data[AZIMUT_INPUT],
        tecnologia=data[TECNOLOGIA_INPUT][0],
        num_cels_x=data[NUM_CEL_X_INPUT],
        num_cels_y=data[NUM_CEL_Y_INPUT],
        conexion=data[CONEXION_INPUT][0],
        tipo_datos_radiacion=tipo_datos_radiacion,
        datos_radiacion="",
        var_parametrica=(data[PARAMETRIC_VAR_INPUT] 
                         if data[ENABLE_PARAMETRIC_INPUT] 
                         else "no_parametrica"),
        valores_parametricos=data[VALUES_PARAMETRIC_INPUT])

    writer.writeData(file_to_save, datastaticsim.FromDataToFile())

#Máquina Estados

def changeState(trigger):
    print("changeState: " + str(trigger))
    global main_window
    global state

    if state == EstadosVistas.Init:
        if trigger == INIT_SIMULATION:
            state = EstadosVistas.VistaSimulaciones
            VistaSimulaciones()

    if state == EstadosVistas.VistaSimulaciones:
        if trigger == STATIC_SIM_SELECTED:
            state = EstadosVistas.VistaSimEstatica
            main_window.close()
            VistaSimEstatica()

        # if trigger == DYNAMIC_SIM_SELECTED:
        #     main_window.close()
        #     VistaSimDinamica()

    if state == EstadosVistas.VistaSimEstatica:
        if trigger == BACK:
            state = EstadosVistas.VistaSimulaciones
            main_window.close()
            VistaSimulaciones()

    if trigger != sg.WIN_CLOSED:
        mainloop()
        return True

    return False

def updateTipoDatosRadiacion(tipo_datos_radiacion):
    if tipo_datos_radiacion == "clear sky":
        main_window[CLEAR_SKY].reset_group()
        main_window[CLEAR_SKY].update(value=True)
        main_window[TMY_INPUT].update(disabled=True)
        main_window[DATA_METEO_INPUT].update(disabled=True)
        main_window[DATA_METEO_BROWSER].update(disabled=True)

    elif tipo_datos_radiacion == "tmy":
        main_window[TMY].reset_group()
        main_window[TMY].update(value=True)
        main_window[TMY_INPUT].update(disabled=False)
        main_window[DATA_METEO_INPUT].update(disabled=True)
        main_window[DATA_METEO_BROWSER].update(disabled=True)

    elif tipo_datos_radiacion == "data meteo":
        main_window[DATA_METEO].reset_group()
        main_window[DATA_METEO].update(value=True)
        main_window[TMY_INPUT].update(disabled=True)
        main_window[DATA_METEO_INPUT].update(disabled=False)
        main_window[DATA_METEO_BROWSER].update(disabled=False)

def getImagesValues(values):
    global result_window
    if result_window.metadata == ParametricVarTypes.AZIMUT_TYPE.value:
        image_azimut = values[VALOR_PARAMETRICA]
        image_connection = result_window[VALOR_NO_PARAMETRICA].DisplayText
    elif result_window.metadata == ParametricVarTypes.CONNECTION_TYPE.value:
        image_connection = values[VALOR_PARAMETRICA]
        image_azimut = result_window[VALOR_NO_PARAMETRICA].DisplayText
    elif result_window.metadata == ParametricVarTypes.NO_PARAMETRIC_TYPE.value:
        image_azimut = result_window[VALOR_PARAMETRICA].DisplayText
        image_connection = result_window[VALOR_NO_PARAMETRICA].DisplayText
    else:
        sg.popup_error(f"ERROR: variable paramétrica \"{result_window.metadata}\" no identificada")
    
    return image_connection, image_azimut



#Si graph_type == GEN_ELECTRICA -> RESOLUCION_HORARIA bloqueada + actualizar valor seleccionado RESULT_RESOLUTION_GROUP
#else -> desbloquear RESOLUCION_HORARIA
#después ya solo queda generar gráficas con los valores seleccionados al darle al botón Ver Gráfica

def updateMomentsFrame(resolucion:str, graph_type:str, image_connection:str, image_azimut:int):
    list_moments = []
    if resolucion == RESOLUCION_HORARIA:
        list_moments = result_data_reader.getMoments(image_connection, image_azimut, graph_type)
    elif resolucion == RESOLUCION_DIARIA:
        list_moments = result_data_reader.getDays(image_connection, image_azimut, graph_type)
    elif resolucion == RESOLUCION_MENSUAL:
        list_moments = result_data_reader.getMonths(image_connection, image_azimut, graph_type)
        print(list_moments)
    else:
        print(f"{resolucion} inválida")

    if len(list_moments) <= 0:
        sg.popup_error("ERROR actualizando momentos: revisar logs aplicación")

    result_window[MOMENTO_INPUT].update(list_moments, set_to_index=0)


def checkAllValues(values):
    ret = True
    
    global fecha_inicio_timestamp
    fecha_inicio_timestamp = generateDateIsoformat(main_window[FECHA_INICIO].get(), values[HORA_INICIO_INPUT], values[MINUTO_INICIO_INPUT])
    if fecha_inicio_timestamp is None:
        sg.popup_error("Fecha y hora de inicio introducidas no válida")
        ret = False
    
    global fecha_fin_timestamp
    fecha_fin_timestamp = generateDateIsoformat(main_window[FECHA_FIN].get(), values[HORA_FINAL_INPUT], values[MINUTO_FINAL_INPUT])
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
    global result_data
    result_data = rd.ResultData()
    writer = YAMLWriter()
    reader = YAMLReader()
    result_data_reader = cdr.ConnectionDataReader()
    state = EstadosVistas.Init
    global result_window
    result_window = None
    print(result_window)
    changeState(INIT_SIMULATION)

#TODO:
#   - crear updateFrameMoments en función del getMoments (llamar cuando se cambia MOMENTO_INPUT)
#       |
#        -> Los momentos no van a ir en un frame porque no se puede actualizar de forma dinámica un layout
#        -> La solución es hacer un Radio Element como simulación horaria/diaria/mensual y en función de eso actualizar la listbox de MOMENTO_INPUT
#   - por lo general la imagen que se genera depende del momento específico, pero para el caso de generación eléctrica pueden generarse gráficas de varios tipos
#   - generateImage tiene que aceptar una lista de momentos
#   - generateImage peta cuando le pasamos un momento cuyo valor está vacío
#   - hay que seguir investigando cómo generar gráficas para varios días