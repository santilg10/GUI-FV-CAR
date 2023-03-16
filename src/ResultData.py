from KeyDefines import *

RESULT_DATA_STR = "result_data"

class ResultData():
    def __init__(self, conexion=""):
        self.conexion = conexion
        self.azimut = {}
        self.status = "UNKNOWN"

    def addRecursoSolar(self, valor, az):
        if az in self.azimut:
            self.azimut[az][RECURSO_SOLAR_TEXT] = valor
        else:
            dict_aux = {RECURSO_SOLAR_TEXT : valor}
            self.azimut[az] = dict_aux
    
    def addCurvaIV(self, valor, az):
        if az in self.azimut:
            self.azimut[az][CURVAS_IV_TEXT] = valor
        else:
            dict_aux = {CURVAS_IV_TEXT : valor}
            self.azimut[az] = dict_aux

    def addGenElec(self, valor, az):
        if az in self.azimut:
            self.azimut[az][GEN_ELECTRICA_TEXT] = valor
        else:
            dict_aux = {GEN_ELECTRICA_TEXT : valor}
            self.azimut[az] = dict_aux
    
    def setStatus(self, status):
        self.status = status

    def FromDataToFile(self):
        """
        returns a dictionary with data encapsuled in a identificative string
        """
        data = {"conexion" : self.conexion,
                "azimut" : self.azimut,
                "status" : self.status}
        file_dict = {RESULT_DATA_STR : data}
        return file_dict
    
    def FromFileToData(self, new_data):
        """""
        receives a dictionary and sets data from it
        """""
        print("ResultData::FromFileToData")
        print(new_data)
        for id, value in new_data[RESULT_DATA_STR].items():
            print(id, value)
            if id == "status":
                self.status = value
            if id == "azimut":
                self.azimut = value
            if id == "conexion":
                self.conexion = value