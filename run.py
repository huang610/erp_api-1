#!/srv/pyenv/versions/general/bin/python
# -*- encoding: utf-8 -*-
import os
import pytest
from lib import tools
from common import Base
from config import setting
from pytest_jsonreport.plugin import JSONReport

if __name__ == '__main__':
    tools.makeCase()
    plugin = JSONReport()
    report_result = setting.report_path+os.sep+"result"
    report_html_path = setting.report_path+os.sep+"html"
    pytest.main(["-s","--alluredir",report_result,"--clean-alluredir"], plugins=[plugin])
    summary = plugin.report.get("summary")
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    skipped = summary.get("skipped", 0)
    total = summary.get("total", 0)
    print(f"共{total}条，通过{passed}条，失败{failed}条，跳过{skipped}条")
    Base.allure_report(report_result, report_html_path)
    Base.send_mail(title="接口测试报告结果", content=report_html_path)