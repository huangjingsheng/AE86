import re
import os
import xlrd
from colaapi import *
from htmlreport import *
import time
class Case():
    def __init__(self):
        self.methodName = None
        self.desc = None
        self.parame = {}
        self.expectedResults = {}
        self.Result = None

class CaseRunner():
    def __init__(self):
        self.cases = []
        self.calaApi = None
        self.result = None

    def readExcel(self):
        pathExcle = os.path.abspath('case.xlsx')
        data = xlrd.open_workbook(pathExcle)

        #初始化所有接口的Url
        urlTable = data.sheet_by_name("url")
        cola = ColaApi()
        for rownum in range(0, urlTable.nrows):
            cola.url[urlTable.cell(rownum, 0).value] = urlTable.cell(rownum, 1).value
        self.calaApi = cola

        caseTable = data.sheet_by_name("case")
        for rownum in range(1,caseTable.nrows):
            status = caseTable.cell(rownum, 4).value
            if status == 0:
                continue
            elif status == 1:
                c = Case()
                c.methodName = caseTable.cell(rownum, 0).value
                c.desc = caseTable.cell(rownum, 1).value
                c.parame = eval(caseTable.cell(rownum, 2).value)
                c.expectedResults = eval(caseTable.cell(rownum, 3).value)
                self.cases.append(c)
        return

    def run(self):
        result = Result()
        caseId = 1

        for case in self.cases:
            unitResult = UnitResult()
            unitResult.desc = str(caseId)+"." + case.desc

            try:
                f = getattr(self.calaApi,case.methodName)
                rsp = f(case.parame)
                self._assertEqual(case.expectedResults,rsp,unitResult,result,caseId,case.parame)
                unitResult.rep = "请求：" + str(case.parame) + "\n" + "响应：" + str(rsp)
            
            except:
                unitResult.status = "错误"
                unitResult.trClass = "none"
                unitResult.tdClass = "errorCase"
                unitResult.id = "ft1." + str(caseId)
                result.error_count += 1
                unitResult.rep = "请求：" + str(case.parame) + "\n" + "响应：" + "请求时出错"
            caseId += 1
            result.unitResults.append(unitResult)

        result.stopTime = datetime.datetime.now()
        self.result = result

        return

    def _assertEqual(self,expectedResults,rsp,unitResult,result,caseId,parame):
        for key in expectedResults.keys():
            regex = '\"' + key + '\":\".+?\"'
            ls = re.findall(regex, str(rsp))
            if ls:
                jsonStr = '{%s}' % ls[0]
                js = json.loads(jsonStr)
                if expectedResults[key] == js[key]:
                    unitResult.resultCode = True
                else:
                    unitResult.resultCode = False
            else:
                unitResult.resultCode = False

        if unitResult.resultCode:
            unitResult.status = "通过"
            unitResult.trClass = 'hiddenRow'
            unitResult.tdClass = 'none'
            result.success_count += 1
            unitResult.id = "pt1." + str(caseId)
            unitResult.rep = "请求：" + str(parame) + "\n" + "响应：" + str(rsp) + "\n"

        else:
            unitResult.status = "失败"
            unitResult.trClass = 'none'
            unitResult.tdClass = 'failCase'
            unitResult.id = "ft1." + str(caseId)
            unitResult.rep = "请求：" + str(parame) + "\n" + "响应：" + str(rsp)
            result.failure_count += 1
        return

if __name__ == "__main__":
    c = CaseRunner()
    c.readExcel()
    c.run()
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    path = os.getcwd()
    report_path = path + "\\" + "report" + "\\" + "可乐优品接口自动化测试报告" + now + ".html"
    fp = open(report_path, "wb")
    rp = Report(stream=fp, title=u'可乐优品接口自动化测试', description=u'用例执行情况')
    rp.generateReport(c.result)



