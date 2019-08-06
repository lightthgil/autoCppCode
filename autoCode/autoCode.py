#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/31 16:07
# @Author  : Jiang Bo
# @Site    : 
# @File    : autoCode.py
# @Software: PyCharm
import re

class AutoCode(object) :

    className = "PtpThreadTask"

    nameSet = """
	SIS_t_TASK task;
	char* name;
	int *func;
	UINT num;
    """

    def getNameList(self):
        nameList = list(filter(None, re.split("[/\\\\,.\-;:`~|<>\s]+", self.nameSet)))
        formateList = nameList[::2]
        valueList = nameList[1::2]

        if(len(formateList) ==  len(valueList) + 1):
            formateList.pop()

        return formateList, valueList

    def getPrintFormatValue(self, format, value):
        outValue = value
        formatLower = format.lower()

        if(formatLower == "char*"):
            outFormat = "%s"
        elif(formatLower[-1] == "*"):
            outFormat = "%p"
        elif(value[0] == "*"):
            outFormat = "%p"
            outValue = value[1:]
        elif(formatLower in ["char", "short", "int", "long"]):
            outFormat = "%d"
        elif(formatLower in ["uchar", "ushort", "uint", "ulong"]):
            outFormat = "%u"
        elif(formatLower == "long64"):
            outFormat = "%lld"
        elif(formatLower == "ulong64"):
            outFormat = "%llu"
        else:
            outFormat = "%s"
            outValue = value + ".toString()"

        return outFormat, outValue

    def makeFormat(self):
        outString = "void "
        if self.className:
            outString += self.className + "::"
        outString += "format()\n{\n"
        formateList, valueList = self.getNameList()
        formate, value = self.getPrintFormatValue(formateList[0], valueList[0])
        outString += "\tname.format(" + "\"" + valueList[0] + " = " + formate + "\",\n"
        for formateName, valueName in zip(formateList[1:], valueList[1:]):
            formate, value = self.getPrintFormatValue(formateName, valueName)
            outString += "\t\t\"" + valueName + " = " + formate +"\",\n"
        for formateName, valueName in zip(formateList[0:-1], valueList[0:-1]):
            formate, value = self.getPrintFormatValue(formateName, valueName)
            outString += "\t\t" + value + ",\n"
        formate, value = self.getPrintFormatValue(formateList[-1], valueList[-1])
        outString += "\t\t" + value + ");\n}\n"

        return outString

    def makeDump(self):
        outString = "void "
        if self.className:
            outString += self.className + "::"
        outString += "dump()\n{\n\tprintf(\"%s\", toString());\n}\n"

        return outString


    def makeCode(self):
        outString = ""
        nameList  = list(filter(None, re.split("[/\\\\,.\-;:`~|<>\s]+", self.nameSet)))
        outString = "    printf(\""
        for name in nameList:
            outString += """
		\"""" + name + """ = %s\\n\""""
        outString += ","
        for name in nameList:
            outString += """
		""" + name + """ ? \"True\" : \"False\","""

        return outString

if __name__ == "__main__" :
    autoCode = AutoCode()
    print(autoCode.makeFormat())
    print(autoCode.makeDump())
    # print(autoCode.makeCode())

