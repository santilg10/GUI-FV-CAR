import PySimpleGUI as sg
from KeyDefines import *

def layoutFechaYLugar(resolutionValues, buttonMenuHourList, buttonMenuMinuteList):
    resolucion_layout =     [sg.Text("Resolución", size=MIN_SIZE), sg.Spin(values=resolutionValues, size=MIN_SIZE, key=RESOLUCION_INPUT)] #en minutos
    fecha_inicio_layout =   [sg.Text("Fecha inicio", size=MIN_SIZE),
                            sg.Push(),
                            sg.Text("YYYY-DD-MM", key=FECHA_INICIO), 
                            sg.Push(),
                            sg.CalendarButton(button_text="change date", target=FECHA_INICIO, format="%Y-%m-%d", key=FECHA_INICIO_INPUT, close_when_date_chosen=True)]
    fecha_final_layout =    [sg.Text("Fecha fin", size=MIN_SIZE),
                            sg.Push(),
                            sg.Text("YYYY-DD-MM", key=FECHA_FIN),
                            sg.Push(),
                            sg.CalendarButton(button_text="change date", target=FECHA_FIN, format="%Y-%m-%d", key=FECHA_FIN_INPUT)]

    hora_inicio_layout =    [sg.Text("Hora inicio", size=MIN_SIZE), 
                            sg.Combo(values=buttonMenuHourList, default_value=buttonMenuHourList[0], readonly=True, key=HORA_INICIO_INPUT),
                            sg.Text(":"),
                            sg.Combo(values=buttonMenuMinuteList, default_value=buttonMenuMinuteList[0], readonly=True, key=MINUTO_INICIO_INPUT),
                            sg.Push(),]
    hora_final_layout =     [sg.Text("Hora fin", size=MIN_SIZE),
                            sg.Combo(values=buttonMenuHourList, default_value=buttonMenuHourList[0], readonly=True, key=HORA_FINAL_INPUT),
                            sg.Text(":"),
                            sg.Combo(values=buttonMenuMinuteList, default_value=buttonMenuMinuteList[0], readonly=True, key=MINUTO_FINAL_INPUT),
                            sg.Push(),]
    lugar_layout =          [sg.Text("Lugar", size=MIN_SIZE),
                            sg.Input(key=LUGAR_INPUT, size=(20,2))]

    tool_msg = "Click dcho para introducir valor por teclado"
    latitud_layout =        [sg.Text("Latitud", size=MIN_SIZE),
                            sg.Slider(range=[-90,90], default_value=0, resolution=0.1, tooltip=tool_msg, orientation='h', key=LATITUD_INPUT)]

    longitud_layout =       [sg.Text("Longitud", size=MIN_SIZE),
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