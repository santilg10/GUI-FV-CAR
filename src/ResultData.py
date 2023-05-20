from KeyDefines import *
from abc import ABC, abstractmethod 

RESULT_DATA_STR = "result_data"

class ResultData():
    def __init__(self) -> None:
        self.parametric_var = ""
        self.azimut = 0
        self.connection = ""

    def readParametricVar(file_data):
        return file_data[RESULT_DATA_STR]["var_parametrica"]

    @abstractmethod
    def FromDataToFile(self):
        pass    
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

class ResultDataAz(ResultData):
    def __init__(self) -> None:
        self.parametric_var = ParametricVarTypes.AZIMUT_TYPE.value

    def FromDataToFile(self):
        pass    
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

class ResultDataConnection(ResultData):
    def __init__(self) -> None:
        self.parametric_var = ParametricVarTypes.CONNECTION_TYPE.value

    def FromDataToFile(self):
        pass    
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
        

class ResultDataNoParametric(ResultData):
    def __init__(self) -> None:
        self.parametric_var = ParametricVarTypes.NO_PARAMETRIC_TYPE.value
        self.images_dict = {}


    def FromDataToFile(self):
        pass

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

class ResultDataCreator():
    def __init__(self) -> None:
        pass

    def createDataFromFile(self, file_data) -> ResultData:
        parametric_var = ResultData.readParametricVar(file_data)
        print(f"ResultDataCreator::craeteDataFromFile creating: {parametric_var}")
        if parametric_var == ParametricVarTypes.AZIMUT_TYPE.value:
            return ResultDataAz().FromFileToData(file_data)
        elif parametric_var == ParametricVarTypes.CONNECTION_TYPE.value:
            return ResultDataConnection().FromFileToData(file_data)
        elif parametric_var == ParametricVarTypes.NO_PARAMETRIC_TYPE.value:
            return ResultDataNoParametric().FromFileToData(file_data)