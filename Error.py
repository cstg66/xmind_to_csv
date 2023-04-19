# -*- coding: utf-8 -*-
# @Time    : 2023/3/29 13:36
# @Author  : Juntong Li
# @File    : Error
# @DESC    :

class MakerAccountError(Exception):
    def __init__(self):
        super().__init__("标记数量错误")


class MakerTypeError(Exception):
    def __init__(self, value):
        super().__init__("标记类型错误 %s" % value)


class TitleError(Exception):
    def __init__(self):
        super().__init__("标题错误")
