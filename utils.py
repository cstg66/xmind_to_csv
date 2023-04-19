# -*- coding: utf-8 -*-
# @Time    : 2023/3/10 13:52
# @Author  : Juntong Li
# @File    : utils
# @DESC    :

import pandas as pd
from pathlib import Path
from loguru import logger
from Error import *


# 检查文件是否是文件夹
def check_path(file_path: Path):
    if Path.is_dir(file_path):
        pass
    else:
        Path.mkdir(file_path)


# 创建指定文件
def make_current_file(file_path: str, file_type: str):
    if file_path.endswith('.xmind'):
        if "." not in file_type:
            file_type = "." + file_type
        new_file_path = Path(file_path).with_suffix(file_type)
        return new_file_path
    else:
        raise FileNotFoundError


# 创建csv文件
def create_csv_file(csv_path: Path):
    first_row = ["迭代版本", "需求内容", "模块", "标题", "优先级", "标签", "前置条件", "步骤", "期望结果", "测试结果"]
    df = pd.DataFrame([first_row])
    df.to_csv(csv_path, header=False, index=False)


# 写入csv文件
def write_to_csv(csv_path, data: list):
    dfs = pd.DataFrame(data)
    dfs.to_csv(csv_path, mode='a', header=False, index=False, encoding='utf_8_sig')


# 判断maker合法性
def check_makers(makers):
    if len(makers) > 2:
        logger.error(MakerAccountError)
        raise MakerAccountError
    for maker in makers:
        if "priority" not in maker and "flag-red" not in maker:
            logger.error(MakerTypeError(maker))
            raise MakerTypeError(maker)
