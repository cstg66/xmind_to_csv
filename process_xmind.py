# -*- coding: utf-8 -*-
# @Time    : 2023/3/27 13:47
# @Author  : Juntong Li
# @File    : testcase_method
# @DESC    :


from xmindparser import xmind_to_dict
from utils import *

priorities = {
    "priority-1": "高",
    "priority-2": "中",
    "priority-3": "低",
}


class ProgressXmind:

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
        case_priority = priorities[case_priority] if case_priority in priorities.keys() else "中"
        return case_priority, case_flag

    # 处理数据
    def generate_data(self, parents: list, topics: list):
        rows = []
        for topic in topics:
            # 如果子级不为空，那么就不是最后一级，继续向下处理，并将当前级别作为父级传入
            if 'topics' in topic:
                rows.extend(self.generate_data(parents + [topic], topic['topics']))
            else:
                # 初始化
                item = []
                for parent in parents:
                    item.append({"title": parent['title'], "makers": parent['makers'] if 'makers' in parent else ''})
                item.append({"title": topic['title'], "makers": topic['makers'] if 'makers' in topic else ''})
                rows.append(item)
        return rows

    # 数据汇总
    def progress_case(self, topics: list):
        case_total = []
        for topic in topics:
            case = []
            # 用例模块, 本期需求内容, 迭代版本
            case_module_name, feature, version = [i for i in topic.get('title').split('|')]
            data_table = self.generate_data([], topic.get('topics'))
            for data in data_table:
                index = 0
                case_name_index = 0
                for info in data:
                    if info.get('makers') != '':
                        case_name = info.get('title')
                        # 判断是否存在冒烟
                        makers = info.get('makers')
                        check_makers(makers)

                        if len(info.get('makers')) == 2:
                            case_priority, case_flag = info.get('makers')
                        else:
                            case_priority, case_flag = info.get('makers')[0], ''

                        case_name_index = index
                    else:
                        index += 1
                case_priority, case_flag = self.change_makers(case_priority, case_flag)
                # 用例模块标题汇总
                case_module = data[:case_name_index]
                # print(case_module)
                if len(case_module) > 0:
                    case_title = '-'.join([i.get('title') for i in case_module]) + "-" + case_name
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
                    [version, feature, case_module_name, case_title, case_priority, case_flag, case_preset, case_step,
                     case_expect, ''])
            # 汇总为二位数组
            case_total.extend(case)
        return case_total

    def progress_data(self, file: str):
        data_dict = self.get_xmind_dict(file)
        case_target = self.check_topics(data_dict)
        case_data = self.progress_case(case_target)
        return case_data
