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
	char *m_taskName;
	INT m_taskNameLen;
	
	INT m_ctlStartIndex;
	INT m_slvDelayStartIndex;
	INT m_slvSyncStartIndex;
	INT m_tcfSynStartIndex;
	INT m_tcfDelStartIndex;
	INT m_mstSynStartIndex;
	INT m_mstDelStartIndex;
	INT m_mstAnncStartIndex;
	INT m_p2pPdelStartIndex;
	INT m_p2pPrspStartIndex;
	INT m_mntStartIndex;
	INT m_disStartIndex;
	INT m_disnetStartIndex;
	INT m_ucmSynStartIndex;
	INT m_ucmAnnStartIndex;
	INT m_ucmDelStartIndex;
	INT m_ucdStartIndex;
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
            outValue = value + "? " + value + " : \"NULL\""
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
            outFormat = "{%s}"
            outValue = value + ".toString()"

        return outFormat, outValue

    def makeFormat(self):
        limitNameNum = 5
        nameSpacing = " "
        outString = "void "
        if self.className:
            outString += self.className + "::"
        outString += "format()\n{\n\tif(NULL==name)\n\t{\n\t\treturn;\n\t}\n"
        formateList, valueList = self.getNameList()
        if(len(formateList) > limitNameNum):
            nameSpacing = "\\n"
        formate, value = self.getPrintFormatValue(formateList[0], valueList[0])
        outString += "\tname->format(" + "\"" + valueList[0] + " = " + formate + "," + nameSpacing +"\"\n"
        for formateName, valueName in zip(formateList[1:-1], valueList[1:-1]):
            formate, value = self.getPrintFormatValue(formateName, valueName)
            outString += "\t\t\"" + valueName + " = " + formate +"," + nameSpacing +"\"\n"
        formate, value = self.getPrintFormatValue(formateList[-1], valueList[-1])
        outString += "\t\t\"" + valueList[-1] + " = " + formate +"\", \n"
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

