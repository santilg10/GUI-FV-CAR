import PySimpleGUI as sg
import FrameResultParametric as paramFrames
import ResultData as rd
from KeyDefines import *

def windowResults(resultData : rd.ResultData, listMoments, frameSize):
    result_data_frame = paramFrames.FrameResultParametric(resultData, listMoments).metodoFabricacion(resultData.parametric_var)
    result_data_frame.setSize(frameSize[0])

    column_data_layout =    [[result_data_frame.drawFrame()]]
    column_img_layout =     [[sg.Image(key=RESULT_IMAGE)]]
    result_layout =         [[sg.Column(column_data_layout), sg.Column(column_img_layout)]]

    return sg.Window("Resultados", layout=result_layout, finalize=True, resizable=True, metadata=result_data_frame.var_parametrica)
