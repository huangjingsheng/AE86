from htmlreport import *
import os,time
"""
if __name__ == '__main__':
    r = Result()

    r.error_count = 1
    r.success_count = 1
    r.failure_count = 1
    r.startTime = 2
    r.stopTime = 1

    a = UnitResult()
    a.id = '案例1'
    a.trClass = 'none'
    a.tdClass = 'errorCase'
    a.desc = '点击第一次'
    a.status = '通过'
    a.rep = "{aaaaaa}"

    unitResult2 = UnitResult()
    unitResult2.id = '案例2'
    unitResult2.trClass = 'none'
    unitResult2.tdClass = 'errorCase'
    unitResult2.desc = '点击第一次'
    unitResult2.status = '失败'
    unitResult2.rep = "{aaaaaa}"

    r.unitResults.append(a)
    r.unitResults.append(unitResult2)

    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    path = os.getcwd()
    report_path = path + "\\" + "report" + "\\" + "可乐优品接口自动化测试报告" + now + ".html"
    print(report_path)
    fp = open(report_path, "wb")
    rp = Report(stream=fp,title=u'可乐优品接口自动化测试',description=u'用例执行情况')
    rp.generateReport(r)
"""
