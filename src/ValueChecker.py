from enum import Enum
import re
import string
# https://docs.python.org/es/3/howto/regex.html


class DateFormat(Enum):
    YYYYMMDD = 0
    DDMMYYYY = 1
    MMDDYYYY = 2


class ValueChecker:
    def matchOK(self, match_result, str):
        if match_result is not None and match_result.group() == str:
            return True
        return False

    def isStringFloat(self, str):
        """""
        recibe un string -> si es un float devuelve True
        independientemente de si es negativo
        """""
        return self.matchPattern(str, '^-?[0-9]{1,}([.][0-9]{1,})?')

    def matchPattern(self, str, pattern):
        ret = False
        patron = re.compile(pattern)
        if str is not None:
            match_result = patron.match(str)
            if self.matchOK(match_result, str):
                ret = True
        return ret

    def isStringYear(self, str):
        return self.matchPattern(str, '^[0-9]{4}')

    def isStringMonth(self, str):
        return self.matchPattern(str, '^[0-1]{1}[0-9]{1}')

    def isStringDay(self, str):
        return self.matchPattern(str, '^[0-3]{1}[0-9]{1}')

    def isStringHour(self, str):
        return self.matchPattern(str, '^[0-2]{1}[0-9]{1}')

    def isStringMinute(self, str):
        return self.matchPattern(str, '^[0-5]{1}[0-9]{1}')

    def isStringDateIsoformat(self, str):
        return self.matchPattern(str, '^[0-9]{4}-[0-1]{1}[0-9]{1}-[0-3]{1}[0-9]{1}T[0-2]{1}[0-9]{1}:[0-5]{1}[0-9]:[0-5]{1}[0-9]')

    def isStringDateIsoformat2(self, str):
        ret = False
        if str is not None:
            matches = re.split("-|T|:", str)
            if len(matches) == 6:
                ret = self.isStringYear(matches[0]) and self.isStringMonth(matches[1]) and self.isStringDay(
                    matches[2]) and self.isStringHour(matches[3]) and self.isStringMinute(matches[4]) and self.isStringMinute(matches[5])
        return ret

    def isStringDate(self, str, dateFormat):
        ret = False
        if str is not None:
            matches = re.split("-", str)
            if dateFormat == DateFormat.YYYYMMDD:
                    ret = self.isStringYear(matches[0]) and self.isStringMonth(
                        matches[1]) and self.isStringDay(matches[2])
            if dateFormat == DateFormat.DDMMYYYY:
                    ret = self.isStringYear(matches[2]) and self.isStringMonth(
                        matches[1]) and self.isStringDay(matches[1])
            if dateFormat == DateFormat.MMDDYYYY:
                    ret = self.isStringYear(matches[2]) and self.isStringMonth(
                        matches[0]) and self.isStringDay(matches[2])
        return ret

    def isStringUInt(self, str):
        """""
        returns True if the string passed is unsigned Int
        """""
        return self.matchPattern(str, '^[0-9]*')
    
    def isStringInt(self, str):
        """""
        returns True if the string passed is an Int with/without sign
        """""
        return self.matchPattern(str, '^-?[0-9]*')



    def findValueInList(list, val):
        """
        list : list to find value
        val : value to find in list
        returns first id of the element if found
                None if not found
        """
        ret = None
        for i in range(len(list)):
            if val == list[i]:
                ret = i
                break
        return ret

    def isNumber(self, val):
        return isinstance(val, int)

    def isLastElemNumber(self, val):
        if isinstance(val, str):
            last = self.getLastElem(val)
            print("last")
    
    def getLastElem(self, val):
        if str is not None:
            matches = re.split("", val)
            print(matches)