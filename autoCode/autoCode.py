#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/31 16:07
# @Author  : Jiang Bo
# @Site    : 
# @File    : autoCode.py
# @Software: PyCharm
import re

class AutoCode(object) :

    className = "CPtpThreadPoolCompany"

    nameSet = """
	static CPtpSupportCompany *m_s_instance;
	CPtpSupport m_ptpFpgaSupport;	/* FPGA处理的报文种类 */
	CPtpSupport m_ptpCpuSupport;	/* CPU协议栈处理的报文种类 */
	CPtpSupport m_ptpFpgaHandle;	/* FPGA收发的报文种类 */
	CPtpSupport m_ptpBcmHandle;		/* BCM收发的报文种类 */
	Boolean m_useOneAnnouceTask;

    """

    def getNameList(self):
        nameSubUnuseKey = re.sub('\/\*[\s\S]*?\*\/|\/\/.*$|static|&', '', self.nameSet)   #去掉单行注释、多行注释、无用关键词
        nameFormatPoint = re.sub('[ \t]+\*', '* ', nameSubUnuseKey) #调整指针符号'*'的位置
        nameList = list(filter(None, re.split("[/\\\\,.\-;:`~|<>\s]+", nameFormatPoint)))
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
        elif(formatLower == "boolean"):
            outFormat = "%s"
            outValue = value + " ? \"True\" : \"False\""
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
        outString += "dump()\n{\n\tprintf(\"%s\\n\", toString());\n}\n"

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

