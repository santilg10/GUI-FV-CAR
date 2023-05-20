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

    def infoFile(self, connection, azimut, graph_type):
        return self.session_path + f"{connection}/azimuth {azimut}/{self.getPickleFileFromType(graph_type)}"
    
    #de momento solo tiene varios días:
    # data/connections/hmSbxPx/azimuth 0/dataframe.pickle
    def getPickleFileFromType(self, graph_type):
        ret = ""
        if graph_type == RECURSO_SOLAR_TEXT:
            ret = "irr_map.pickle"
        elif graph_type == CURVAS_IV_TEXT:
            ret = "iv_module.pickle"
        elif graph_type == GEN_ELECTRICA_TEXT:
            # ret = "power_pv_df.pickle"
            ret = "dataframe.pickle"
        return ret

    def plot(self, momento, data_map, graph_type):
        fig, ax = plt.subplots()
        if graph_type == RECURSO_SOLAR_TEXT:
            ax.imshow(data_map[momento]['irr']['c_interp_curv'])
        elif graph_type == CURVAS_IV_TEXT:
            ax.plot(data_map[momento]['iv_s']['voltage'], data_map[momento]['iv_s']['current'])
        elif graph_type == GEN_ELECTRICA_TEXT:
            # print(data_map['Pmpp'])
            data_map['Pmpp'].plot.bar(ax=ax, title=momento)
            ax.grid(visible=True, which='major', axis='both')
        return fig


    #TODO: comprobar qué errores puede haber aquí
    def readFile(self, info_file, graph_type):
        with open(info_file, 'rb') as handle:
            data = pickle.load(handle)
        # data = self.addDay(data, '2018-06-12', '2018-06-14', graph_type)
        return data

    def generateImage(self, connection, azimut, graph_type, list_moments):
        print(connection, azimut, graph_type, list_moments)
        info_file = self.infoFile(connection, azimut, graph_type)
        data = self.readFile(info_file, graph_type)
        return self.plot(list_moments, data, graph_type)
        
    def getMoments(self, connection, azimut, graph_type):
        info_file = self.infoFile(connection, azimut, graph_type)
        print("\ngetMoments from:\n"+info_file)
        data = self.readFile(info_file, graph_type)
        if graph_type == GEN_ELECTRICA_TEXT:
            data_copy = data.copy()
            index_timestamp_list = data_copy.index.tolist()
            index_list = []
            for index in index_timestamp_list:
                index_list.append(str(index))
            return index_list
        return list(data.keys())
    
    def addDay(self, data_map, day_orig, day_dest, graph_type):
        moments_list = list(data_map.keys())
        
        if graph_type == GEN_ELECTRICA_TEXT:
            df_new_day = data_map.copy()
            new_day = df_new_day.index[-1].date() + timedelta(days=1)
            df_new_day.index = df_new_day.index.map(lambda t: datetime.combine(new_day, t.time(), tzinfo=t.tzinfo))
            df_new_day['day'] = new_day
            data_map = data_map.append(df_new_day)
            with open('power_pv_df.pickle', 'wb') as f:
                pickle.dump(data_map, f)

        else:
            for day in moments_list:
                values = data_map[day]
                day = day.replace(day_orig, day_dest)
                data_map[day] = values
        return data_map
