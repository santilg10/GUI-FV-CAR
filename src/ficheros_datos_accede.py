# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 18:51:00 2023

@author: Ruben
"""
from pathlib import Path
import pickle
from matplotlib import pyplot as plt
import pandas as pd
import sys
import DataStaticSim as dss
from YAMLAdapter import YAMLReader, YAMLWriter
from ResultData import ResultData
from KeyDefines import IMAGES_PATH, RESULT_FILE

connection = "SbSx"
azimuth = []
list_ret = []

#COMPROBAR PARÁMETROS RECIBIDOS
if len(sys.argv) == 2:
    dataStaticSimFile = sys.argv[1]
    reader = YAMLReader()
    new_data = reader.readData(dataStaticSimFile)
    datastaticsim = dss.DataStaticSim()
    datastaticsim.FromFileToData(new_data)

    connection = datastaticsim.GetValue("conexion")
    result_data = ResultData(connection)
    if datastaticsim.GetValue("var_parametrica") == "azimut":
        # azimuth = datastaticsim.GetValue("azimut")
        lim_inf = datastaticsim.GetValue("lim_inferior")
        lim_sup = datastaticsim.GetValue("lim_superior")
        rango = datastaticsim.GetValue("rango")

        iter = lim_inf
        while iter <= lim_sup:
            azimuth.append(iter)
            iter += rango


def plot_irr_momento(momento, irr_map):
    fig, ax = plt.subplots()
    ax.imshow(irr_map[momento]['irr']['c_interp_curv'])
    filename = IMAGES_PATH + f'irr_momento_{connection}_{azimuth_iter}.png'
    plt.savefig(filename)
    list_ret.append(filename)
    result_data.addRecursoSolar(valor=filename, az=azimuth_iter)
    
def plot_iv_momento(momento, iv_module):
    fig, ax = plt.subplots()
    ax.plot(iv_module[momento]['iv_s']['voltage'], iv_module[momento]['iv_s']['current'])
    filename = IMAGES_PATH + f'iv_momento_{connection}_{azimuth_iter}.png'
    plt.savefig(filename)
    list_ret.append(filename)
    result_data.addCurvaIV(valor=filename, az=azimuth_iter)
    
def plot_power_dia(dia, power):
    fig, ax = plt.subplots()
    power_pv['Pmpp'].plot.bar(ax=ax, title=dia)
    filename = IMAGES_PATH + f'power_dia_{connection}_{azimuth_iter}.png'
    plt.savefig(filename)
    list_ret.append(filename)
    result_data.addGenElec(valor=filename, az=azimuth_iter)

def generateResultFile(ret):
    if ret is True:
        result_data.setStatus("OK")
        writer = YAMLWriter()
        data = result_data.FromDataToFile()
        writer.writeData(RESULT_FILE, data)
    else:
        result_data.setStatus("ERROR")

PATH1 = Path('connections')

ret = False
for azimuth_iter in azimuth:
    path2 = PATH1 / connection / f'azimuth {azimuth_iter}'
    # print(connection, azimuth_iter)
    with open(path2 / 'irr_map.pickle', 'rb') as handle:
        irradiance_map = pickle.load(handle)
        
    with open(path2 / 'iv_module.pickle', 'rb') as fichero:
        iv_curve = pickle.load(fichero)
    
    power_pv = pd.read_pickle(path2 / 'power_pv_df.pickle')
    plot_irr_momento(momento='2018-06-12 12:00:00+02:00', irr_map=irradiance_map)
    plot_iv_momento(momento='2018-06-12 12:00:00+02:00', iv_module=iv_curve)
    plot_power_dia(dia='2018-06-12', power=power_pv)
    ret = True
generateResultFile(ret)


