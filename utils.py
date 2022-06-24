# -*- coding: utf-8 -*-

# @Time : 2021/12/8 14:46

# @Author : John-li
# @id : lijuntong01
# @File : utils.py

from pathlib import Path

class TitleError(Exception):
    def __init__(self, leng):
        self.leng = leng
    def __str__(self):
        print("需求名称|需求id|Sprint有误，请检查！")

# 创建导入jira时所需文件
def create_config(path):
    config = '''{"project.key":"XM2111101","jira.field.mappings":"{summary=标题, components=模块, reporter=报告人, priority=优先级, labels=标签}","custom.field.mappings":"{Sprint=Sprint}","dateFormat":"dd\/MMM\/yy h:mm a","delimiter":",","synapse.field.mappings":"{Requirement=需求, ExpectedResult=期望结果, TestData=测试数据, TestSuite=测试用例集, Step=步骤}"}'''
    config_path = Path(path).joinpath('config.txt')
    with open(config_path, 'w') as f:
        f.write(config)