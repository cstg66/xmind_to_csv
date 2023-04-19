# -*- coding: utf-8 -*-
# @Time    : 2023/3/28 12:10
# @Author  : Juntong Li
# @File    : create_csv
# @DESC    :

from process_xmind import ProgressXmind
from utils import *
import argparse

parser = argparse.ArgumentParser(description='Please enter xmind path.')
parser.add_argument('-F', '--filename', metavar='F', type=str, help='Testcase xmind file path.')

args = parser.parse_args()


def create_csv(xmind_file):
    csv_path = make_current_file(xmind_file, "csv")
    print(csv_path)
    create_csv_file(csv_path)
    case_data = ProgressXmind().progress_data(xmind_file)
    write_to_csv(csv_path, case_data)


if __name__ == '__main__':
    create_csv(args.filename)