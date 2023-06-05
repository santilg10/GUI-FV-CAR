STATIC_SIM_DATA_STR = "static_sim_data"

class DataStaticSim():
    """""
    class that contains all the data from Static simulation
    has method to return data in dictionary form to pass to config file writer
    has method to set data from a config file
    """""
    def __init__(self, resolucion=0, fecha_inicio=0, fecha_fin=0, lugar="", latitud=0, longitud=0,
            x=1, y=1, curvatura=0, orientacion=0, azimut=0, tecnologia="", num_cels_x=1, num_cels_y=1, conexion="", tipo_datos_radiacion="",
            datos_radiacion="", var_parametrica="", valores_parametricos=[]):
        print("DataStaticSim")

        self.data = {
            "resolucion" : resolucion,
            "fecha_inicio" : fecha_inicio,
            "fecha_fin" : fecha_fin,
            "lugar" : lugar,
            "latitud" : latitud,
            "longitud" : longitud,
            "x" : x,
            "y" : y,
            "curvatura" : curvatura,
            "orientacion" : orientacion,
            "azimut" : azimut,
            "tecnologia" : tecnologia,
            "num_cels_x" : num_cels_x,
            "num_cels_y" : num_cels_y,
            "conexion" : conexion,
            "tipo_datos_radiacion" : tipo_datos_radiacion,
            "datos_radiacion" : datos_radiacion,
            "var_parametrica" : var_parametrica,
            "valores_parametrica" : valores_parametricos,
        }

    def SetValue(self, data, val):
        self.data[data] = val

    def GetValue(self, data):
        return self.data[data]

    def GetValues(self):
        return self.data

    def ShowData(self):
        for id, value in self.data.items():
            print(f"{id} : {str(value)}")

    def FromDataToFile(self):
        """
        returns a dictionary with data encapsuled in a identificative string
        """
        # print("DataStaticSim::FromDataToFile")
        file_dict = {STATIC_SIM_DATA_STR : self.data}
        return file_dict

    def FromFileToData(self, new_data) -> bool:
        """""
        receives a dictionary and sets data from it
        """""
        ret = False
        if STATIC_SIM_DATA_STR in new_data:
            ret = True
            for id, value in new_data[STATIC_SIM_DATA_STR].items():
                self.SetValue(id, value)

        return ret