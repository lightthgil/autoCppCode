#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/31 16:07
# @Author  : Jiang Bo
# @Site    : 
# @File    : autoCode.py
# @Software: PyCharm
import re

class AutoCode(object) :

    className = "TMsgPtpv3PortDSCfg"

    nameSet = """
    TCmmMsgHdr msghdr;
	Long IfIndex;
	Short CfgIndex;
	Octet Slot;
	Octet Port;
	Boolean PortEna;
	Short DelMech;
	Short DlrqIntv;
	Long P2PmeanPDel;
	Short AnncIntv;
	Short AnncRcptTmo;
	Short SyncIntv;
	Short PdelReqIntv;
	Octet ManualPortState;
	Long SpVlanTPID;
	String SpVlanId;
	Octet SpVlanPri;
	Long CeVlanTPID;
	String CeVlanId;
	Octet CeVlanPri;
	Octet PortType;
	String UcMstIp;
	Octet StepType;
	Short DomainNumber;
	Long SyncAsymmetryDelay;
	Long DlrqAsymmetryDelay;
	Long PdlrqAsymmetryDelay;
	Long PdlrpAsymmetryDelay;
	Long AsymmetryDelay;
	Octet EncapMode;
	Octet DlrqSendMode;
	ULong Pwid;
	ULong PwInlabel;
	ULong PwOutlabel;
	ULong Lspid;
	ULong LspInlabel;
	ULong LspOutlabel;
	Short DelRespTimeOut;
	Short WtrTime;
	Short SyncTimeOut;
	Octet TxFrameType;
	Octet Profile;
	Long NotSlave;
	Long LocalPriority;
	Short Duration;
	Long RESERVE1;
	Long RESERVE2;
	Long RESERVE3;
	Long RESERVE4;
	Long GMClockClass;
	Long GMPriority1;
	Long GMPriority2;
	Long GMScaleLogVar;
	Long GMClockAccuracy;
	Long EnGMClockQuality;
	Long TimeTrace;
	Long EnTimeTrace;
	Long Correction;
	Long EnCorrection;
	Octet PortProtocolMode;
	Boolean PassiveDelReqEn;
	Boolean ReimburseEn;

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

        if(formatLower in ["char*", "string"]):
            outFormat = "%s"
            outValue = value + "? " + value + " : \"NULL\""
        elif(formatLower[-1] == "*"):
            outFormat = "%p"
        elif(value[0] == "*"):
            outFormat = "%p"
            outValue = value[1:]
        elif(formatLower in ["char", "short", "int", "long"]):
            outFormat = "%d"
        elif(formatLower in ["octet", "uchar", "ushort", "uint", "ulong"]):
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
        nameMaxLen = 0
        outString = "void "
        if self.className:
            outString += self.className + "::"
        formateList, valueList = self.getNameList()
        if(len(formateList) > limitNameNum):
            nameSpacing = "\\n"
            nameMaxLen = max(map(lambda i: len(i), valueList))
        outString += "format()\n{\n\tint nameMaxLen = " + str(
            nameMaxLen) + ";\n\n\tif(NULL==name)\n\t{\n\t\treturn;\n\t}\n"
        formate, value = self.getPrintFormatValue(formateList[0], valueList[0])
        outString += "\tname->format(\"%-*s = " + formate + "," + nameSpacing +"\"\t/* "+ valueList[0] + " */\n"
        for formateName, valueName in zip(formateList[1:-1], valueList[1:-1]):
            formate, value = self.getPrintFormatValue(formateName, valueName)
            outString += "\t\t\"%-*s = " + formate +"," + nameSpacing +"\"\t\t\t\t/* "+ valueName + " */\n"
        formate, value = self.getPrintFormatValue(formateList[-1], valueList[-1])
        outString += "\t\t\"%-*s = " + formate +"\",\t\t\t\t/* "+ valueList[-1] + " */\n"
        for formateName, valueName in zip(formateList[0:-1], valueList[0:-1]):
            formate, value = self.getPrintFormatValue(formateName, valueName)
            outString += "\t\tnameMaxLen, \"" + valueName + "\", " + value + ",\n"
        formate, value = self.getPrintFormatValue(formateList[-1], valueList[-1])
        outString += "\t\tnameMaxLen, \"" + valueList[-1] + "\", " + value + ");\n}\n"

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

