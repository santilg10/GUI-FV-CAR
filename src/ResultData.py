from KeyDefines import *
from abc import ABC, abstractmethod 

RESULT_DATA_STR = "result_data"

class ResultData():
    def __init__(self) -> None:
        self.parametric_var = ""
        self.azimut = 0
        self.connection = ""
        self.status = "UNKNOWN"
        self.error = ""

    def readParametricVar(file_data):
        if file_data is not None:
            return file_data[RESULT_DATA_STR]["var_parametrica"]
        else:
            return None

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
    
    @abstractmethod
    def FromFileToData(self, new_data):
        pass
    @abstractmethod
    def parametricValues(self):
        pass
    
    def getAzimut(self):
        return self.azimut
    def getConnection(self):
        return self.connection
    
    @abstractmethod
    def firstAzimut(self):
        pass
    @abstractmethod
    def firstConnection(self):
        pass

    @abstractmethod
    def addRecursoSolar(self, valor, parametric):
        pass

    @abstractmethod
    def addCurvaIV(self, valor, parametric):
        pass

    @abstractmethod
    def addGenElec(self, valor, parametric):
        pass

    def addAzimut(self, az):
        self.azimut = az

    def addConnection(self, conn):
        self.connection = conn

class ResultDataAz(ResultData):
    def __init__(self) -> None:
        super().__init__()
        self.azimut = {}
        self.parametric_var = ParametricVarTypes.AZIMUT_TYPE.value

    def FromFileToData(self, file_data):
        for id, value in file_data[RESULT_DATA_STR].items():
            if id == "status":
                self.status = value
            if id == "azimut":
                self.azimut = value
            if id == "connection":
                self.connection = value
            if id == "var_parametrica":
                self.parametric_var = value

        return self
    
    def addAzimut(self, az):
        if az not in self.azimut:
            self.azimut[az] = {RECURSO_SOLAR_TEXT : ""}

    def parametricValues(self):
        return list(self.azimut.keys())
    
    def getAzimut(self):
        return self.parametricValues()
    
    def firstAzimut(self):
        if len(self.getAzimut()) > 0:
            return self.getAzimut()[0]
        else:
            return 0
    
    def firstConnection(self):
        return self.connection
    
    def addRecursoSolar(self, valor, parametric):
        if parametric in self.azimut:
            self.azimut[parametric][RECURSO_SOLAR_TEXT] = valor
        else:
            dict_aux = {RECURSO_SOLAR_TEXT : valor}
            self.azimut[parametric] = dict_aux

    def addCurvaIV(self, valor, parametric):
        if parametric in self.azimut:
            self.azimut[parametric][CURVAS_IV_TEXT] = valor
        else:
            dict_aux = {RECURSO_SOLAR_TEXT : valor}
            self.azimut[parametric] = dict_aux

    def addGenElec(self, valor, parametric):
        if parametric in self.azimut:
            self.azimut[parametric][GEN_ELECTRICA_TEXT] = valor
        else:
            dict_aux = {RECURSO_SOLAR_TEXT : valor}
            self.azimut[parametric] = dict_aux            

class ResultDataConnection(ResultData):
    def __init__(self) -> None:
        super().__init__()
        self.connection = {}
        self.parametric_var = ParametricVarTypes.CONNECTION_TYPE.value

    def FromFileToData(self, file_data):
        for id, value in file_data[RESULT_DATA_STR].items():
            if id == "status":
                self.status = value
            if id == "azimut":
                self.azimut = value
            if id == "connection":
                self.connection = value
            if id == "var_parametrica":
                self.parametric_var = value

        return self
    
    def addConnection(self, conn):
        if conn not in self.conn:
            self.azimut[conn] = {RECURSO_SOLAR_TEXT : ""}

    def parametricValues(self):
        return list(self.connection.keys())
    
    def getConnection(self):
        return self.parametricValues()
    
    def firstAzimut(self):
        return self.azimut

    def firstConnection(self):
        if len(self.getConnection()) > 0:
            return self.getConnection()[0]
        else:
            return 0
        
    def addRecursoSolar(self, valor, parametric):
        if parametric in self.connection:
            self.connection[parametric][RECURSO_SOLAR_TEXT] = valor
        else:
            dict_aux = {RECURSO_SOLAR_TEXT : valor}
            self.connection[parametric] = dict_aux

    def addCurvaIV(self, valor, parametric):
        if parametric in self.connection:
            self.connection[parametric][CURVAS_IV_TEXT] = valor
        else:
            dict_aux = {RECURSO_SOLAR_TEXT : valor}
            self.connection[parametric] = dict_aux

    def addGenElec(self, valor, parametric):
        if parametric in self.connection:
            self.connection[parametric][GEN_ELECTRICA_TEXT] = valor
        else:
            dict_aux = {RECURSO_SOLAR_TEXT : valor}
            self.connection[parametric] = dict_aux


class ResultDataNoParametric(ResultData):
    def __init__(self) -> None:
        super().__init__()
        self.parametric_var = ParametricVarTypes.NO_PARAMETRIC_TYPE.value

        self.recurso_solar = ""
        self.curva_iv = ""
        self.gen_elec = ""

        self.images_dict = {}

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
        for id, value in new_data[RESULT_DATA_STR].items():
            print(f"\t{id} : {value}")
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
    
    def parametricValues(self):
        return self.images_dict
    
    def firstAzimut(self):
        return self.azimut
    
    def firstConnection(self):
        return self.connection

    def addRecursoSolar(self, valor, parametric):
        self.recurso_solar = valor

    def addCurvaIV(self, valor, parametric):
        self.curva_iv = valor

    def addGenElec(self, valor, parametric):
        self.gen_elec = valor

class ResultDataCreator():
    def __init__(self) -> None:
        pass

    def createDataFromFile(self, file_data) -> ResultData:
        parametric_var = ResultData.readParametricVar(file_data)
        print(f"ResultDataCreator::createDataFromFile creating: {parametric_var}")
        if parametric_var == ParametricVarTypes.AZIMUT_TYPE.value:
            return ResultDataAz().FromFileToData(file_data)
        elif parametric_var == ParametricVarTypes.CONNECTION_TYPE.value:
            return ResultDataConnection().FromFileToData(file_data)
        elif parametric_var == ParametricVarTypes.NO_PARAMETRIC_TYPE.value:
            return ResultDataNoParametric().FromFileToData(file_data)
        
    def createDataFromParametricVar(self, parametric_var) -> ResultData:
        if parametric_var == ParametricVarTypes.AZIMUT_TYPE.value:
            return ResultDataAz()
        elif parametric_var == ParametricVarTypes.CONNECTION_TYPE.value:
            return ResultDataConnection()
        elif parametric_var == ParametricVarTypes.NO_PARAMETRIC_TYPE.value:
            return ResultDataNoParametric()
