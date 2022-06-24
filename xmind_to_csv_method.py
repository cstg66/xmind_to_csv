# -*- coding: utf-8 -*-

# @Time : 2021/12/8 18:22

# @Author : John-li
# @id : lijuntong01
# @File : xmind_to_csv_method.py

from xmindparser import xmind_to_dict
import pandas as pd
from loguru import logger
from utils import *
from pathlib import Path
import xlsxwriter

prioritys = {
    "priority-1": "高",
    "priority-2": "中",
    "priority-3": "低",
}


class XmindToCsv:
    def check_path(self, csv_dir: Path, excel_dir: Path):
        if Path.is_dir(csv_dir):
            pass
        else:
            Path.mkdir(csv_dir)

        if Path.is_dir(excel_dir):
            pass
        else:
            Path.mkdir(excel_dir)

    def change_file_name_to_csv(self, file_path: str):
        if file_path.endswith('.xmind'):
            csv_file_path_base = Path(file_path).with_suffix('.csv')
            csv_file_parent = csv_file_path_base.parent
            csv_filename = csv_file_path_base.name
            csv_dir = Path.joinpath(csv_file_parent, 'csv')
            excel_dir = Path.joinpath(csv_file_parent, 'excel')
            csv_file_path = Path.joinpath(csv_dir, csv_filename)
            self.check_path(csv_dir, excel_dir)
            return csv_file_path
        else:
            raise FileNotFoundError

    # 获取xmind首层
    def get_xmind_dict(self, file: str):
        data_dict = xmind_to_dict(file_path=file)[0].get('topic')
        return data_dict

    # 检查层级
    def check_topics(self, xmind_dict: dict):
        if xmind_dict.get('topic'):
            return xmind_dict.get('topic')
        else:
            return xmind_dict.get('topics')

    # 标记转换
    def change_makers(self, case_priority, case_flag):
        if case_flag == 'flag-red':
            case_flag = '冒烟测试'
        case_priority = prioritys[case_priority] if case_priority in prioritys.keys() else "中"
        return case_priority, case_flag

    # 数据层级处理
    def generate_data_table(self, parents: list, topics: list):
        rows = []
        for topic in topics:
            # 如果子级不为空，那么就不是最后一级，继续向下处理，并将当前级别作为父级传入
            if 'topics' in topic:
                rows.extend(self.generate_data_table(parents + [topic], topic['topics']))

            else:
                # 初始化
                item = []
                for parent in parents:
                    item.append({"title": parent['title'], "makers": parent['makers'] if 'makers' in parent else ''})
                item.append({"title": topic['title'], "makers": topic['makers'] if 'makers' in topic else ''})
                rows.append(item)
        return rows

    # 数据汇总
    def progress_case(self, topics: list, reporter: str):
        case_total = []
        for topic in topics:
            case = []
            # 用例名称, 故事id, sprint
            case_story_name, story_id, sprint = [i for i in topic.get('title').split('|')]
            data_table = self.generate_data_table([], topic.get('topics'))
            for data in data_table:
                index = 0
                case_name_index = 0
                for info in data:
                    if info.get('makers') != '':
                        case_name = info.get('title')
                        # 判断是否存在冒烟
                        if len(info.get('makers')) == 2:
                            case_priority, case_flag = info.get('makers')
                        else:
                            case_priority, case_flag = info.get('makers')[0], ""
                        case_name_index = index
                    else:
                        index += 1
                case_priority, case_flag = self.change_makers(case_priority, case_flag)
                # 用例模块标题汇总
                case_modle = data[:case_name_index]
                if len(case_modle) > 0:
                    case_title = '-'.join([i.get('title') for i in case_modle]) + "-" + case_name
                else:
                    case_title = case_name
                # 存在预置条件
                if len(data[case_name_index + 1:]) > 2:
                    case_preset, case_step, case_expect = [i.get('title') for i in data[case_name_index + 1:]]
                # 不存在预置条件
                else:
                    case_preset = ''
                    case_step, case_expect = [i.get('title') for i in data[case_name_index + 1:]]
                # 添加用例为一维数组
                case.append(
                    [sprint, story_id, case_story_name, case_title, case_priority, case_flag, case_preset, case_step,
                     case_expect, '', reporter])
        # 汇总为二位数组
        case_total.extend(case)
        return case_total

    def create_csv(self, csv_path):
        first_row = ["Sprint", "需求", "模块", "标题", "优先级", "标签", "测试数据", "步骤", "期望结果", "测试用例集", "报告人"]
        df = pd.DataFrame([first_row])
        df.to_csv(csv_path, header=False, index=False)

    def write_to_csv(self, csv_path, data: list):

        dfs = pd.DataFrame(data)
        dfs.to_csv(csv_path, mode='a', header=False, index=False, encoding='utf_8_sig')

    # 写入excel
    def write_to_excel(self, csv_path):
        excel_path_base = Path(csv_path).with_suffix('.xlsx')
        excel_path_parent = excel_path_base.parent.parent
        excel_filename = excel_path_base.name
        excel_path = Path.joinpath(excel_path_parent, 'excel', excel_filename)
        df = pd.read_csv(csv_path)
        df.to_excel(excel_path, index=False, engine='xlsxwriter')

    # 批量处理用例
    def progress_data(self, file: str, reporter):
        data_dict = self.get_xmind_dict(file)
        case_target = self.check_topics(data_dict)
        case_data = self.progress_case(case_target, reporter)
        csv_path = self.change_file_name_to_csv(file)
        self.create_csv(csv_path)
        case_datas = []
        case_datas.append(case_data)
        return case_datas
