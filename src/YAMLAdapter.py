import yaml

class YAMLWriter():
    def __init__(self):
        pass

    def writeData(self, file, data):
        """
        file : file descriptor opened on write mode
        data : dictionary containing info to write to file
        """

        with open(file, "w") as fd:
            yaml.dump(data, fd)

class YAMLReader():
    def __init__(self):
        pass

    def readData(self, file):
        """
        file : file descriptor opened on read mode
        returns data read from file
        """

        with open(file, "r") as fd:
            data = yaml.load(fd)
        return data
#YAMLLoadWarning: calling yaml.load() without Loader=... is deprecated, as the default Loader is unsafe. Please read https://msg.pyyaml.org/load for full details.