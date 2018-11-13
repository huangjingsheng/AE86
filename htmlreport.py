# -*- coding: utf-8 -*-
__author__ = "天才小兰"
__version__ = "0.0.1"
import sys
from xml.sax import saxutils
import datetime

class Case():
    """每个case"""
    def __init__(self):
        """methodName反射时调用的方法名，parame调用方法时的参数,expectedResults断言用的键和值，unitResult每个case的执行结果"""
        self.methodName = None
        self.desc = None
        self.id = None
        self.parame = {}
        self.expectedResults = {}
        self.unitResult = None

class Result():
    """一个result一个报告，一个result包含多个单元报告，
    startTime执行所有用例的开始时间
    stopTime执行完所有用例的结束时间
    count用例总数
    success_count运行成功数目
    failure_count运行错误数
    error_count脚本出错数目
    trClass如果全部成功passClass，只要有错误或失败都failClass
    unitResults单个case的结果
    """
    def __init__(self):
        self.startTime = self.startTime = datetime.datetime.now()
        self.stopTime = None
        #self.desc = None
        self.count = 0
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.trClass = None
        self.unitResults = []

class UnitResult():
    """
    每个用例的报告
    trClass成功'hiddenRow'，其他'none'
    tdClass成功'none'，失败'failCase'，错误‘errorCase’
    """
    def __init__(self):
        self.id = None
        self.trClass = None
        self.tdClass = None
        self.desc = None
        self.rep = None
        self.status = None
        self.resultCode = True


class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """
    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(s)

    def writelines(self, lines):
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()

stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)


# ----------------------------------------------------------------------
# Template


class Template_mixin(object):
    """
    Define a HTML template for report customerization and generation.

    Overall structure of an HTML report

    HTML
    +------------------------+
    |<html>                  |
    |  <head>                |
    |                        |
    |   STYLESHEET           |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </head>               |
    |                        |
    |  <body>                |
    |                        |
    |   HEADING              |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   REPORT               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   ENDING               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </body>               |
    |</html>                 |
    +------------------------+
    """

    STATUS = {
        0: u'通过',
        1: u'失败',
        2: u'错误',
    }

    DEFAULT_TITLE = 'Unit Test Report'
    DEFAULT_DESCRIPTION = ''

    # ------------------------------------------------------------------------
    # HTML Template

    HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>%(title)s</title>
    <meta name="generator" content="%(generator)s"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>

    <link href="http://cdn.bootcss.com/bootstrap/3.3.0/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.bootcss.com/echarts/3.8.5/echarts.common.min.js"></script>
    <!-- <script type="text/javascript" src="js/echarts.common.min.js"></script> -->

    %(stylesheet)s

</head>
<body>
    <script language="javascript" type="text/javascript"><!--
    output_list = Array();

    /* level - 0:Summary; 1:Failed; 2:All */
    function showCase(level) {
        trs = document.getElementsByTagName("tr");
        for (var i = 0; i < trs.length; i++) {
            tr = trs[i];
            id = tr.id;
            if (id.substr(0,2) == 'ft') {
                if (level < 1) {
                    tr.className = 'hiddenRow';
                }
                else {
                    tr.className = '';
                }
            }
            if (id.substr(0,2) == 'pt') {
                if (level > 1) {
                    tr.className = '';
                }
                else {
                    tr.className = 'hiddenRow';
                }
            }
        }
    }


    function showClassDetail(cid, count) {
        var id_list = Array(count);
        var toHide = 1;
        for (var i = 0; i < count; i++) {
            tid0 = 't' + cid.substr(1) + '.' + (i+1);
            tid = 'f' + tid0;
            tr = document.getElementById(tid);
            if (!tr) {
                tid = 'p' + tid0;
                tr = document.getElementById(tid);
            }
            id_list[i] = tid;
            if (tr.className) {
                toHide = 0;
            }
        }
        for (var i = 0; i < count; i++) {
            tid = id_list[i];
            if (toHide) {
                document.getElementById('div_'+tid).style.display = 'none'
                document.getElementById(tid).className = 'hiddenRow';
            }
            else {
                document.getElementById(tid).className = '';
            }
        }
    }


    function showTestDetail(div_id){
        var details_div = document.getElementById(div_id)
        var displayState = details_div.style.display
        // alert(displayState)
        if (displayState != 'block' ) {
            displayState = 'block'
            details_div.style.display = 'block'
        }
        else {
            details_div.style.display = 'none'
        }
    }


    function html_escape(s) {
        s = s.replace(/&/g,'&amp;');
        s = s.replace(/</g,'&lt;');
        s = s.replace(/>/g,'&gt;');
        return s;
    }

    /* obsoleted by detail in <div>
    function showOutput(id, name) {
        var w = window.open("", //url
                        name,
                        "resizable,scrollbars,status,width=800,height=450");
        d = w.document;
        d.write("<pre>");
        d.write(html_escape(output_list[id]));
        d.write("\n");
        d.write("<a href='javascript:window.close()'>close</a>\n");
        d.write("</pre>\n");
        d.close();
    }
    */
    --></script>

    <div id="div_base">
        %(heading)s
        %(report)s
        %(ending)s
        %(chart_script)s
    </div>
</body>
</html>
"""  # variables: (title, generator, stylesheet, heading, report, ending, chart_script)

    ECHARTS_SCRIPT = """
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('chart'));

        // 指定图表的配置项和数据
        var option = {
            title : {
                text: '测试执行情况',
                x:'center'
            },
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%%)"
            },
            color: ['#95b75d', 'grey', '#b64645'],
            legend: {
                orient: 'vertical',
                left: 'left',
                data: ['通过','失败','错误']
            },
            series : [
                {
                    name: '测试执行情况',
                    type: 'pie',
                    radius : '60%%',
                    center: ['50%%', '60%%'],
                    data:[
                        {value:%(Pass)s, name:'通过'},
                        {value:%(fail)s, name:'失败'},
                        {value:%(error)s, name:'错误'}
                    ],
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    </script>
    """  # variables: (Pass, fail, error)

    # ------------------------------------------------------------------------
    # Stylesheet
    #
    # alternatively use a <link> for external style sheet, e.g.
    #   <link rel="stylesheet" href="$url" type="text/css">

    STYLESHEET_TMPL = """
<style type="text/css" media="screen">
    body        { font-family: Microsoft YaHei,Consolas,arial,sans-serif; font-size: 80%; }
    table       { font-size: 100%; }
    pre         { white-space: pre-wrap;word-wrap: break-word; }

    /* -- heading ---------------------------------------------------------------------- */
    h1 {
        font-size: 16pt;
        color: gray;
    }
    .heading {
        margin-top: 0ex;
        margin-bottom: 1ex;
    }

    .heading .attribute {
        margin-top: 1ex;
        margin-bottom: 0;
    }

    .heading .description {
        margin-top: 2ex;
        margin-bottom: 3ex;
    }

    /* -- css div popup ------------------------------------------------------------------------ */
    a.popup_link {
    }

    a.popup_link:hover {
        color: red;
    }

    .popup_window {
        display: none;
        position: relative;
        left: 0px;
        top: 0px;
        /*border: solid #627173 1px; */
        padding: 10px;
        /*background-color: #E6E6D6; */
        font-family: "Lucida Console", "Courier New", Courier, monospace;
        text-align: left;
        font-size: 8pt;
        /* width: 500px;*/
    }

    }
    /* -- report ------------------------------------------------------------------------ */
    #show_detail_line {
        margin-top: 3ex;
        margin-bottom: 1ex;
    }
    #result_table {
        width: 99%;
    }
    #header_row {
        font-weight: bold;
        color: #303641;
        background-color: #ebebeb;
    }
    #total_row  { font-weight: bold; }
    .passClass  { background-color: #bdedbc; }
    .failClass  { background-color: #ffefa4; }
    .errorClass { background-color: #ffc9c9; }
    .passCase   { color: #6c6; }
    .failCase   { color: #FF6600; font-weight: bold; }
    .errorCase  { color: #c00; font-weight: bold; }
    .hiddenRow  { display: none; }
    .testcase   { margin-left: 2em; }


    /* -- ending ---------------------------------------------------------------------- */
    #ending {
    }

    #div_base {
                position:absolute;
                top:0%;
                left:5%;
                right:5%;
                width: auto;
                height: auto;
                margin: -15px 0 0 0;
    }
</style>
"""

    # ------------------------------------------------------------------------
    # Heading
    #

    HEADING_TMPL = """
    <div class='page-header'>
        <h1>%(title)s</h1>
    %(parameters)s
    </div>
    <div style="float: left;width:50%%;"><p class='description'>%(description)s</p></div>
    <div id="chart" style="width:50%%;height:400px;float:left;"></div>
"""  # variables: (title, parameters, description)

    HEADING_ATTRIBUTE_TMPL = """<p class='attribute'><strong>%(name)s:</strong> %(value)s</p>
"""  # variables: (name, value)

    # ------------------------------------------------------------------------
    # Report
    #

    REPORT_TMPL = u"""
    <div class="btn-group btn-group-sm">
        <button class="btn btn-default" onclick='javascript:showCase(0)'>总结</button>
        <button class="btn btn-default" onclick='javascript:showCase(1)'>失败</button>
        <button class="btn btn-default" onclick='javascript:showCase(2)'>全部</button>
    </div>
    <p></p>
    <table id='result_table' class="table table-bordered">
        <colgroup>
            <col align='left' />
            <col align='right' />
            <col align='right' />
            <col align='right' />
            <col align='right' />
            <col align='right' />
        </colgroup>
        <tr id='header_row'>
            <td>用例描述</td>
            <td>总数</td>
            <td>通过</td>
            <td>失败</td>
            <td>错误</td>
            <td>查看</td>
        </tr>
        %(test_list)s
        <tr id='total_row'>
            <td>总计</td>
            <td>%(count)s</td>
            <td>%(Pass)s</td>
            <td>%(fail)s</td>
            <td>%(error)s</td>
            <td>&nbsp;</td>
        </tr>
    </table>
"""  # variables: (test_list, count, Pass, fail, error)

    REPORT_CLASS_TMPL = u"""
    <tr class='%(style)s'>
        <td>合计</td>
        <td>%(count)s</td>
        <td>%(Pass)s</td>
        <td>%(fail)s</td>
        <td>%(error)s</td>
        <td><a href="javascript:showClassDetail('c1',%(count)s)">详情</a></td>
    </tr>
"""  # variables: (style, desc, count, Pass, fail, error, cid)

    REPORT_TEST_WITH_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'>

    <!--css div popup start-->
    <a class="popup_link" onfocus='this.blur();' href="javascript:showTestDetail('div_%(tid)s')" >
        %(status)s</a>

    <div id='div_%(tid)s' class="popup_window">
        <pre>%(script)s</pre>
    </div>
    <!--css div popup end-->

    </td>
</tr>
"""  # variables: (tid, Class, style, desc, status)

    REPORT_TEST_NO_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'>%(status)s</td>
</tr>
"""  # variables: (tid, Class, style, desc, status)

    REPORT_TEST_OUTPUT_TMPL = r"""%(id)s: %(output)s"""  # variables: (id, output)

    # ------------------------------------------------------------------------
    # ENDING
    #

    ENDING_TMPL = """<div id='ending'>&nbsp;</div>"""

    # -------------------- The end of the Template class -------------------






class Report(Template_mixin):

    def __init__(self, stream=sys.stdout, verbosity=1, title=None, description=None):
        self.stream = stream
        self.verbosity = verbosity
        if title is None:
            self.title = self.DEFAULT_TITLE
        else:
            self.title = title
        if description is None:
            self.description = self.DEFAULT_DESCRIPTION
        else:
            self.description = description

        #self.startTime = datetime.datetime.now()

    def generateReport(self,result):
        generator = 'HTMLTestRunner %s' % __version__
        stylesheet = self.STYLESHEET_TMPL
        heading = self._getReportAttributes(result)
        report =self._generate_report(result)
        ending = self.ENDING_TMPL
        chart = self._generate_chart(result)

        output = self.HTML_TMPL % dict(
            title = saxutils.escape(self.title),
            generator = generator,
            stylesheet = stylesheet,
            heading = heading,
            report = report,
            ending = ending,
            chart_script = chart
        )
        self.stream.write(output.encode('utf8'))

    def _generate_chart(self, result):
        chart = self.ECHARTS_SCRIPT % dict(
            Pass=str(result.success_count),
            fail=str(result.failure_count),
            error=str(result.error_count),
        )
        return chart

    def _generate_report(self,result):
        rows = []
        row = self.REPORT_CLASS_TMPL % dict(
            style=result.trClass,
            count=result.count,
            Pass=result.success_count,
            fail=result.failure_count,
            error=result.error_count,
        )
        rows.append(row)
        list = result.unitResults
        for unitResult in list:
            row = self.REPORT_TEST_WITH_OUTPUT_TMPL % dict(
                tid= str(unitResult.id),
                Class = unitResult.trClass,
                style = unitResult.tdClass,
                desc = unitResult.desc,
                status = unitResult.status,
                script = unitResult.rep
            )
            rows.append(row)
        report = self.REPORT_TMPL % dict(
            test_list = ''.join(rows),
            count = str(result.count),
            Pass = str(result.success_count),
            fail = str(result.failure_count),
            error = str(result.error_count),
        )
        return report



    def _getReportAttributes(self, result):
        startTime = str(result.startTime)[:19]
        duration = str(result.stopTime - result.startTime)
        status = []
        if result.success_count: status.append(u'通过 %s' % result.success_count)
        if result.failure_count: status.append(u'失败 %s' % result.failure_count)
        if result.error_count:   status.append(u'错误 %s' % result.error_count  )
        if status:
            status = ' '.join(status)
        else:
            status = 'none'

        list = [
            (u'开始时间', startTime),
            (u'运行时长', duration),
            (u'状态', status),
        ]
        a_lines = []
        for name, value in list:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                name = saxutils.escape(name),
                value = saxutils.escape(value),
            )
            a_lines.append(line)

        heading = self.HEADING_TMPL % dict(
            title = saxutils.escape(self.title),
            parameters = ''.join(a_lines),
            description = saxutils.escape(self.description),
        )
        return heading
