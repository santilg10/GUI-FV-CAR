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
            data = yaml.safe_load(fd)
        return data