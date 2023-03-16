from enum import Enum

class EstadosVistas(Enum):
    CerrarAplicacion = -1
    Init = 0
    VistaSimulaciones = 1
    VistaSimEstatica = 2
    VistaSimDinamica = 3
    VistaResultados = 4