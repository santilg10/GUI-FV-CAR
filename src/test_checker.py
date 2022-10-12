import datetime
from ValueChecker import DateFormat, ValueChecker

iso1 = "YYYY"
iso2 = "124"
iso3 = "2022-07-31T23:59"
isoCompleto = "1998-07-23T09:03:54"

checker = ValueChecker()

id = 1
print("TEST     isStringFloat")
print("test " + str(id))
id += 1
test = "1234.123"
print(checker.isStringFloat(test))
assert True == checker.isStringFloat(test)
id += 1
print("test " + str(+(+id)))
test = "234"
assert True == checker.isStringFloat(test)
id += 1
print("test " + str(+(+id)))
test = "-8989.23"
assert True == checker.isStringFloat(test)
id += 1
print("test " + str(+(+id)))
test = "655.65sdf"
assert False == checker.isStringFloat(test)
id += 1



print("\n\nTEST     isStringDateIsoformat")
print("test " + str(+(+id)))
test = "YYYY"
assert False == checker.isStringDateIsoformat2(test)
id += 1
print("test " + str(+(+id)))
test = "124"
assert False == checker.isStringDateIsoformat2(test)
id += 1
print("test " + str(+(+id)))
test = "2022-07-31T23:59"
assert False == checker.isStringDateIsoformat2(test)
id += 1
print("test " + str(+(+id)))
test = "1998-07-23T10:03:54"
assert True == checker.isStringDateIsoformat2(test)
id += 1
print("test " + str(+(+id)))
test = "1998-07-23"
assert True == checker.isStringDate(test, DateFormat.YYYYMMDD)
id += 1
print("test " + str(+(+id)))
test = "1998asf"
assert False == checker.isStringUInt(test)
id += 1
print("test " + str(+(+id)))
test = "013"
assert True == checker.isStringUInt(test)
id += 1
print("test " + str(+(+id)))
test = "63.12"
assert False == checker.isStringUInt(test)
id += 1
print("test " + str(+(+id)))
test = "-63"
assert False == checker.isStringUInt(test)
id += 1
print("test " + str(+(+id)))
test = "-63"
assert True == checker.isStringInt(test)
id += 1
print("test " + str(+(+id)))
test = "-6331-"
assert False == checker.isStringInt(test)
id += 1
print("test " + str(+(+id)))
test = 1234
assert True == checker.isNumber(test)
id += 1

print("-------------------------------")
testDate = datetime.datetime.now()
print(testDate.hour)
print(testDate.isoformat())
testDate = datetime.datetime.fromisoformat(isoCompleto)
print(testDate.isoformat())
print(testDate.date().isoformat())
print(testDate.minute)