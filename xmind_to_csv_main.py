# -*- coding: utf-8 -*-

# @Time : 2021/12/8 18:24

# @Author : John-li
# @id : lijuntong01
# @File : xmind_to_csv_main.py

from pathlib import Path
from xmind_to_csv_method import XmindToCsv
from utils import create_config

class XmindToCsvMain:
    def __init__(self):
        self.xmind_to_csv_method = XmindToCsv()

    def write_files(self, case_file_path, reporter):
        case_data = self.xmind_to_csv_method.progress_data(case_file_path, reporter)
        if len(case_data[0]) == 1:
            csv_path = self.xmind_to_csv_method.change_file_name_to_csv(case_file_path)
            self.xmind_to_csv_method.write_to_csv(csv_path, case_data)
            self.xmind_to_csv_method.write_to_excel(csv_path)
        else:
            for case in case_data:
                csv_path = self.xmind_to_csv_method.change_file_name_to_csv(case_file_path)
                self.xmind_to_csv_method.write_to_csv(csv_path, case)
                self.xmind_to_csv_method.write_to_excel(csv_path)

    # 创建文件
    def create_cases(self, case_path, reporter):
        path = Path(case_path)
        # 目录形式转换
        if path.is_dir():
            for case_file in path.rglob("*.xmind"):
                case_file_path = str(case_file)
                self.write_files(case_file_path, reporter)
            create_config(Path(case_path).joinpath('csv'))
            return True
        # 文件形式转换
        else:
            self.write_files(case_path, reporter)
            create_config(Path(case_path).parent)
        return True

if __name__ == '__main__':
    XmindToCsvMain().create_cases(case_path = "demo.xmind", reporter='lijuntong')