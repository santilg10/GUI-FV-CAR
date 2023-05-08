from pathlib import Path
import pickle
from matplotlib import pyplot as plt
import pandas as pd
import sys
import os
import DataStaticSim as dss
from YAMLAdapter import YAMLReader, YAMLWriter
from ResultData import ResultData, ResultDataAz, ResultDataConn, ResultDataNoParametric
from KeyDefines import *

connection = "SbSx"
azimut = 0
azimuths = []
connections = []
list_ret = []

#COMPROBAR PARÁMETROS RECIBIDOS
if len(sys.argv) == 3:
    dataStaticSimFile = sys.argv[1]
    session_dir_name = sys.argv[2]
    reader = YAMLReader()
    new_data = reader.readData(dataStaticSimFile)
    datastaticsim = dss.DataStaticSim()
    datastaticsim.FromFileToData(new_data)

    parametric_var = datastaticsim.GetValue("var_parametrica")
    result_data = ResultData(parametric_var)
    if parametric_var == "azimut":
        azimuths = datastaticsim.GetValue("valores_parametrica")
        connections.append(datastaticsim.GetValue("conexion"))
        result_data = ResultDataAz(connection=datastaticsim.GetValue("conexion"))


    elif parametric_var == "connection":
        connections = datastaticsim.GetValue("valores_parametrica")
        azimuths.append(datastaticsim.GetValue("azimut"))
        result_data = ResultDataConn(azimut=datastaticsim.GetValue("azimut"))

    elif parametric_var == "no_parametrica":
        connections.append(datastaticsim.GetValue("conexion"))
        azimuths.append(datastaticsim.GetValue("azimut"))
        result_data = ResultDataNoParametric()

    print(azimuths, connections)


def plot_irr_momento(momento, irr_map):
    fig, ax = plt.subplots()
    ax.imshow(irr_map[momento]['irr']['c_interp_curv'])
    filename = images_path + f'irr_momento_{connection_iter}_{azimuth_iter}.png'
    plt.savefig(filename)
    list_ret.append(filename)
    result_data.addRecursoSolar(valor=filename, az=azimuth_iter, conn=connection_iter)
    
def plot_iv_momento(momento, iv_module):
    fig, ax = plt.subplots()
    ax.plot(iv_module[momento]['iv_s']['voltage'], iv_module[momento]['iv_s']['current'])
    filename = images_path + f'iv_momento_{connection_iter}_{azimuth_iter}.png'
    plt.savefig(filename)
    list_ret.append(filename)
    result_data.addCurvaIV(valor=filename, az=azimuth_iter, conn=connection_iter)
    
def plot_power_dia(dia, power):
    fig, ax = plt.subplots()
    power_pv['Pmpp'].plot.bar(ax=ax, title=dia)
    filename = images_path + f'power_dia_{connection_iter}_{azimuth_iter}.png'
    plt.savefig(filename)
    list_ret.append(filename)
    result_data.addGenElec(valor=filename, az=azimuth_iter, conn=connection_iter)

def generateResultFile(ret, error):
    if ret is True:
        result_data.setStatus("OK")

    else:
        result_data.setStatus("ERROR")
        result_data.setError(error)

    writer = YAMLWriter()
    data = result_data.FromDataToFile()
    result_file = result_path + RESULT_FILE
    writer.writeData(result_file, data)

def generateDirStruct(path):
    global result_path
    global images_path
    result_path = path + "result/"
    images_path = result_path + "images/"

    if not os.path.isdir(result_path):
        os.mkdir(result_path)
        print("Creado dir: " + result_path)
    if not os.path.isdir(images_path):
        os.mkdir(images_path)
        print("Creado dir: " + images_path)




PATH1 = Path('connections')
simulador = False
if simulador:
    connections_path = session_dir_name + "connections/"
else:
    connections_path = CONNECTIONS_DEFAULT_PATH

generateDirStruct(session_dir_name)
ret = False
error = ""
for azimuth_iter in azimuths:

    for connection_iter in connections:
        # path2 = PATH1 / connection / f'azimuth {azimuth_iter}'
        print(connection_iter, azimuth_iter)
        path2 = connections_path + f'{connection_iter}/azimuth {azimuth_iter}'
        if os.path.isdir(path2):
            with open(path2 + "/irr_map.pickle", 'rb') as handle:
                irradiance_map = pickle.load(handle)
                
            with open(path2 + "/iv_module.pickle", 'rb') as fichero:
                iv_curve = pickle.load(fichero)
        
            power_pv = pd.read_pickle(path2 + "/power_pv_df.pickle")
            plot_irr_momento(momento='2018-06-12 12:00:00+02:00', irr_map=irradiance_map)
            plot_iv_momento(momento='2018-06-12 12:00:00+02:00', iv_module=iv_curve)
            plot_power_dia(dia='2018-06-12', power=power_pv)
            ret = True
        
        else:
            ret = False
            error = "No such file or directory: " + str(path2)
            break
generateResultFile(ret, error)
print(list_ret)


