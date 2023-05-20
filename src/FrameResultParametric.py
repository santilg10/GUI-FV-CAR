import PySimpleGUI as sg
from KeyDefines import *
from PySimpleGUI.PySimpleGUI import DEFAULT_FRAME_RELIEF
import ResultData as rd
from abc import ABC, abstractmethod 

param_var_size = (20, 1)
class FrameResultParametric():
    def __init__(self, result_data, list_moments=[]) -> None:
        """result_data es de tipo ResultData.ResultData"""
        self.var_parametrica = result_data.parametric_var
        self.result_data = result_data
        self.list_moments = list_moments
        self.frame = sg.Frame("", [], visible=False)

    @abstractmethod
    def drawFrame(self):
        print("FrameResultParametric::drawFrame")
        pass

    def setSize(self, size):
        self.size = size

    def metodoFabricacion(self, var_parametrica):
        print(f"FrameResultParametric -> CREATING [\t{self.var_parametrica}\t]")
        if var_parametrica == ParametricVarTypes.AZIMUT_TYPE.value:
            return FrameResultParametricAzimut(self.result_data, self.list_moments)
        elif var_parametrica == ParametricVarTypes.CONNECTION_TYPE.value:
            return FrameResultParametricConnection(self.result_data, self.list_moments)
        else:
            return FrameResultNoParametric(self.result_data, self.list_moments)
        
    def momentsFrame(self):
        print("drawing moments frame")
        moment_layout = [[sg.Radio("Resolución horaria", group_id=RESULT_RESOLUTION_GROUP, default=True, enable_events=True, key=RESOLUCION_HORARIA)],
                         [sg.Radio("Resolución diaria", group_id=RESULT_RESOLUTION_GROUP, default=False, enable_events=True, key=RESOLUCION_DIARIA)],
                         [sg.Radio("Resolución mensual", group_id=RESULT_RESOLUTION_GROUP, default=False, enable_events=True, key=RESOLUCION_MENSUAL)],
                         [sg.Listbox(self.list_moments, default_values=self.list_moments[0], key=MOMENTO_INPUT, no_scrollbar=False,
                                     select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, size=(30,5))]]
        return sg.Frame("", layout=moment_layout)

    def setResultData(self, result_data):
        self.result_data = result_data



#################
#
#   FrameResultParametricAzimut
#
#################

class FrameResultParametricAzimut(FrameResultParametric):
    def __init__(self, result_data, list_moments) -> None:
        super().__init__(result_data, list_moments)
        print("FrameResultParametricAzimut CREATED")

    def drawFrame(self):
        print("FrameResultParametricAzimut::drawFrame")
        layout =[
            [sg.Text(f"{ParametricVarTypes.AZIMUT_TYPE.value}", size=param_var_size),
             sg.Combo(self.result_data.parametricValues(), default_value=self.result_data.firstAzimut(),
                      readonly=True, enable_events=True, key=VALOR_PARAMETRICA, size=param_var_size)
            ],
            [sg.Text(f"{ParametricVarTypes.CONNECTION_TYPE.value}", size=param_var_size), 
             sg.Text(self.result_data.firstConnection(), key=VALOR_NO_PARAMETRICA)
            ],
            [sg.Combo(values=LISTA_RESULTADOS, default_value=LISTA_RESULTADOS[0], size=param_var_size, readonly=True, enable_events=True, key=RESULTADO_INPUT)],
            [self.momentsFrame()],
            [sg.Push(), sg.Button("Ver gráfica", key=GENERAR_GRAFICA_INPUT), sg.Push()]
        ]
        self.frame = sg.Frame("Azimut parametric", layout, size=self.size, key=f"{FRAME_RESULTADOS}{self.var_parametrica}")
        return self.frame



#################
#
#   FrameResultParametricConnection
#
#################

class FrameResultParametricConnection(FrameResultParametric):
    def __init__(self, result_data, list_moments) -> None:
        super().__init__(result_data, list_moments)
        print("FrameResultParametricConnection CREATED")

    def drawFrame(self):
        print("FrameResultParametricConnection::drawFrame")
        print(self.result_data.firstConnection())
        layout =[
            [sg.Text(f"{ParametricVarTypes.CONNECTION_TYPE.value}", size=param_var_size),
             sg.Combo(self.result_data.parametricValues(), default_value=self.result_data.firstConnection(),
                      readonly=True, enable_events=True, key=VALOR_PARAMETRICA, size=param_var_size)
            ],
            [sg.Text(f"{ParametricVarTypes.AZIMUT_TYPE.value}", size=param_var_size), 
             sg.Text(self.result_data.firstAzimut(), key=VALOR_NO_PARAMETRICA)
            ],
            [sg.Combo(values=LISTA_RESULTADOS, default_value=LISTA_RESULTADOS[0], size=param_var_size, readonly=True, enable_events=True, key=RESULTADO_INPUT)],
            [self.momentsFrame()],
            [sg.Push(), sg.Button("Ver gráfica", key=GENERAR_GRAFICA_INPUT), sg.Push()]
        ]
        self.frame = sg.Frame("Connection parametric", layout, size=self.size, key=f"{FRAME_RESULTADOS}{self.var_parametrica}")
        return self.frame



#################
#
#   FrameResultNoParametric
#
#################

class FrameResultNoParametric(FrameResultParametric):
    def __init__(self, result_data, list_moments) -> None:
        super().__init__(result_data,list_moments)
        print("FrameResultNoParametric CREATED")

    def drawFrame(self):
        print("FrameResultNoParametric::drawFrame")
        layout =[
            [sg.Text(f"{ParametricVarTypes.AZIMUT_TYPE.value}", size=param_var_size), 
             sg.Text(self.result_data.firstAzimut(), key=VALOR_PARAMETRICA)
            ],
            [sg.Text(f"{ParametricVarTypes.CONNECTION_TYPE.value}", size=param_var_size),
             sg.Text(self.result_data.firstConnection(), key=VALOR_NO_PARAMETRICA)
            ],
            [sg.Combo(values=LISTA_RESULTADOS, default_value=LISTA_RESULTADOS[0], size=param_var_size, readonly=True, enable_events=True, key=RESULTADO_INPUT)],
            [self.momentsFrame()],
            [sg.Push(), sg.Button("Ver gráfica", key=GENERAR_GRAFICA_INPUT), sg.Push()]
        ]
        self.frame = sg.Frame("No parametric", layout, size=self.size, key=f"{FRAME_RESULTADOS}{self.var_parametrica}")
        return self.frame