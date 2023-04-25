from KeyDefines import *
from enum import Enum

RESULT_DATA_STR = "result_data"

class ResultData():
    def __init__(self, parametric_var=""):
        self.connection = {}
        self.azimut = {}
        self.parametric_var = parametric_var
        self.status = "UNKNOWN"
        self.error = ""
        self.recurso_solar = ""
        self.curva_iv = ""
        self.gen_elec = ""
        self.images_dict = {}

    def addRecursoSolar(self, valor, az, conn):
        pass

    def addCurvaIV(self, valor, az, conn):
        pass

    def addGenElec(self, valor, az, conn):
        pass
    
    def setStatus(self, status):
        self.status = status

    def setError(self, error):
        self.error = error

    def FromDataToFile(self):
        """
        returns a dictionary with data encapsuled in a identificative string
        """
        data = {"var_parametrica":self.parametric_var,
                "status" : self.status,
                "azimut" : self.azimut,
                "connection" : self.connection}
        if self.error and self.status == "ERROR":
            data["error"] = self.error

        file_dict = {RESULT_DATA_STR : data}
        return file_dict
    
    def FromFileToData(self, new_data):
        """""
        receives a dictionary and sets data from it
        """""
        for id, value in new_data[RESULT_DATA_STR].items():
            if id == "status":
                self.status = value
            if id == "azimut":
                self.azimut = value
            if id == "connection":
                self.connection = value
            if id == "var_parametrica":
                self.parametric_var = value
        
        if self.parametric_var == "no_parametrica":
            return ResultDataNoParametric.FromFileToData(self, new_data)
        else:
            return self


class ResultDataAz(ResultData):
    def __init__(self, parametric_var="azimut", connection=""):
        super().__init__(parametric_var)
        self.azimut = {}
        self.connection = connection

    def addRecursoSolar(self, valor, az, conn):
        if az in self.azimut:
            self.azimut[az][RECURSO_SOLAR_TEXT] = valor
        else:
            dict_aux = {RECURSO_SOLAR_TEXT : valor}
            self.azimut[az] = dict_aux

    def addCurvaIV(self, valor, az, conn):
        if az in self.azimut:
            self.azimut[az][CURVAS_IV_TEXT] = valor
        else:
            dict_aux = {CURVAS_IV_TEXT : valor}
            self.azimut[az] = dict_aux

    def addGenElec(self, valor, az, conn):
        if az in self.azimut:
            self.azimut[az][GEN_ELECTRICA_TEXT] = valor
        else:
            dict_aux = {GEN_ELECTRICA_TEXT : valor}
            self.azimut[az] = dict_aux


class ResultDataConn(ResultData):
    def __init__(self, parametric_var="connection", azimut=""):
        super().__init__(parametric_var)
        self.connection = {}
        self.azimut = azimut

    def addRecursoSolar(self, valor, az, conn):
        if conn in self.connection:
            self.connection[conn][RECURSO_SOLAR_TEXT] = valor
        else:
            dict_aux = {RECURSO_SOLAR_TEXT : valor}
            self.connection[conn] = dict_aux

    def addCurvaIV(self, valor, az, conn):
        if conn in self.connection:
            self.connection[conn][CURVAS_IV_TEXT] = valor
        else:
            dict_aux = {CURVAS_IV_TEXT : valor}
            self.connection[conn] = dict_aux

    def addGenElec(self, valor, az, conn):
        if conn in self.connection:
            self.connection[conn][GEN_ELECTRICA_TEXT] = valor
        else:
            dict_aux = {GEN_ELECTRICA_TEXT : valor}
            self.connection[conn] = dict_aux            


class ResultDataNoParametric(ResultData):
    def __init__(self, parametric_var="no_parametrica", azimut=0, connection=""):
        super().__init__(parametric_var)
        self.azimut = azimut
        self.connection = connection

    def addRecursoSolar(self, valor, az, conn):
        self.recurso_solar = valor

    def addCurvaIV(self, valor, az, conn):
        self.curva_iv = valor

    def addGenElec(self, valor, az, conn):
        self.gen_elec = valor

    def setImagesDict(self):
        images = { RECURSO_SOLAR_TEXT : self.recurso_solar,
            CURVAS_IV_TEXT : self.curva_iv,
            GEN_ELECTRICA_TEXT : self.gen_elec
        }
        parametric_var = self.parametric_var
        parametric_map = { 0 : images}
        self.images_dict = { "var_parametrica": self.parametric_var,
                 "status" : self.status,
                 "azimut" : self.azimut,
                 "connection" : self.connection,
                 parametric_var : parametric_map
        }

    def FromDataToFile(self):
        """
        returns a dictionary with data encapsuled in a identificative string
        """
        self.setImagesDict()
        data = self.images_dict
        if self.error and self.status == "ERROR":
            data["error"] = self.error

        file_dict = {RESULT_DATA_STR : data}
        return file_dict
    
    def FromFileToData(self, new_data):
        """""
        receives a dictionary and sets data from it
        """""
        print("ResultDataNoParametric::FromFileToData")
        # super().FromFileToData(new_data)
        for id, value in new_data[RESULT_DATA_STR].items():
            print(id, value)
            if id == "status":
                self.status = value
            if id == "azimut":
                self.azimut = value
            if id == "connection":
                self.connection = value
            if id == "var_parametrica":
                self.parametric_var = value
            if id == self.parametric_var:
                self.images_dict = value
        return self