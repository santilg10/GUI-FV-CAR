import sys
import pickle
import pandas as pd
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from KeyDefines import *


DAY_IN_SECS = 86400
class ConnectionDataReader():
    def __init__(self, session_path=CONNECTIONS_DEFAULT_PATH) -> None:
        self.session_path = session_path
        self.datetime_format = '%Y-%m-%d'

    def infoFile(self, connection, azimut, graph_type) -> str:
        return self.session_path + f"{connection}/azimuth {azimut}/{self.getPickleFileFromType(graph_type)}"
    
    def getPickleFileFromType(self, graph_type) -> str:
        ret = ""
        if graph_type == RECURSO_SOLAR_TEXT:
            ret = "irr_map.pickle"
        elif graph_type == CURVAS_IV_TEXT:
            ret = "iv_module.pickle"
        elif graph_type == GEN_ELECTRICA_TEXT:
            ret = "power_pv_df.pickle"
            # ret = "dataframe.pickle"
        return ret

    def plot(self, momento, data_map, graph_type):
        fig, ax = plt.subplots()
        if graph_type == RECURSO_SOLAR_TEXT:
            ax.imshow(data_map[momento]['irr']['c_interp_curv'])
        elif graph_type == CURVAS_IV_TEXT:
            ax.plot(data_map[momento]['iv_s']['voltage'], data_map[momento]['iv_s']['current'])
        elif graph_type == GEN_ELECTRICA_TEXT:
            # data_map['Pmpp'].plot.bar(ax=ax, title=momento)
            # ax.grid(visible=True, which='major', axis='both')

            print("ConnectionDataReader::plot")
            print(momento)
            print(data_map['Pmpp'])
            new_data_map = self.createDataMapFromMoment(data_map, [momento], RESOLUCION_DIARIA)
            new_data_map['Pmpp'].plot.bar(ax=ax, title=momento)
            ax.grid(visible=True, which='major', axis='both')
        return fig


    #TODO: comprobar qué errores puede haber aquí
    def readFile(self, info_file):
        with open(info_file, 'rb') as handle:
            data = pickle.load(handle)
        # data = self.addDay(data, '2018-06-12', '2018-06-14', graph_type)
        return data

    def generateImage(self, connection, azimut, graph_type, list_moments):
        print("ConnectionDataReader::generateImage:")
        print(connection, azimut, graph_type, list_moments)
        info_file = self.infoFile(connection, azimut, graph_type)
        data = self.readFile(info_file)
        return self.plot(list_moments, data, graph_type)
        
    def addDay(self, data_map, day_orig, day_dest, graph_type):
        moments_list = list(data_map.keys())
        
        if graph_type == GEN_ELECTRICA_TEXT:
            df_new_day = data_map.copy()
            print(df_new_day)
            
            for i in range(1, 51):
                new_day_i = df_new_day.index[-1].date() + timedelta(days=i)
                df_new_day_i = df_new_day.copy()
                df_new_day_i.index = df_new_day_i.index.map(lambda t: t + timedelta(days=i))
                df_new_day_i['day'] = new_day_i.strftime(self.datetime_format)
                data_map = data_map.append(df_new_day_i)

            with open('dataframe.pickle', 'wb') as f:
                pickle.dump(data_map, f)

        else:
            for day in moments_list:
                values = data_map[day]
                day = day.replace(day_orig, day_dest)
                data_map[day] = values
        return data_map
    
    
    def getMoments(self, connection, azimut, graph_type):
        info_file = self.infoFile(connection, azimut, graph_type)
        data = self.readFile(info_file)
        if graph_type == GEN_ELECTRICA_TEXT:
            data_copy = data.copy()
            index_timestamp_list = data_copy.index.tolist()
            index_list = []
            for index in index_timestamp_list:
                index_list.append(str(index))
            return index_list
        return list(data.keys())
    
    def getDays(self, connection:str, azimut:int, graph_type:str):
        days = []
        if graph_type == GEN_ELECTRICA_TEXT:
            info_file = self.infoFile(connection, azimut, graph_type)
            data = self.readFile(info_file)
            # data = self.addDay(data, '2018-06-12', '2018-06-14', graph_type)
            for day in data['day'].to_list():
                if day not in days:
                    days.append(day)
        else:
            print(f"ConnectionDataReader::getDays for {graph_type} NOT IMPLEMENTED")
        return days
    
    def getMonths(self, connection:str, azimut:int, graph_type:str):
        months = []
        days = self.getDays(connection, azimut, graph_type)
        for day in days:
            date = datetime.strptime(day, self.datetime_format)
            print(date)
            print(date.date())
            month = date.date().month
            print(month)
            if month not in months:
                months.append(month)
        return months
    
    def createDataMapFromMoment(self, data_map, fechas_seleccionadas, resolucion):
        print("ConnectionDataReader::createDataMapFromMoment")
        print(data_map, fechas_seleccionadas, resolucion)
        ret = data_map
        if resolucion == RESOLUCION_HORARIA:
            ret = data_map[data_map['day'].isin(fechas_seleccionadas)].copy()
        else:
            print(f"ConnectionDataReader::createDataMapFromMoment {resolucion} no tratada")
        print(ret)
        return ret
