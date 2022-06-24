# -*- coding: utf-8 -*-

# @Time : 2021/12/8 18:22

# @Author : John-li
# @id : lijuntong01
# @File : xmind_to_csv_gui.py

import os
import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter import messagebox as tm
import platform
from xmind_to_csv_main import XmindToCsvMain
from pathlib import Path

system = platform.system()

class Window():
    def __init__(self):
        self.root = tkinter.Tk()  # 生成主窗口

        self.root.option_add('*Dialog.msg.width', 30)
        self.root.title("Xmind to csv tool")  # 设置窗口的标题
        self.root.geometry("500x300")  # 设置窗口的大小
        self.root.geometry('+800+350')  # 设置窗口出现的位置
        self.root.configure(bg='WhiteSmoke')
        self.root.resizable(0, 0)  # 将窗口大小设置为不可变
        # 文件的路径
        self.xmind_label = tkinter.Label(self.root, text='Xmind路径：', bg='WhiteSmoke')# 生成一个标签
        self.xmind_label.grid(row=0, column=0)  # 使用grid布局，标签显示在第一行，第一列
        self.path = tkinter.StringVar()  # 生成一个StringVar 对象，来保存下面输入框中的内容
        self.xmind_path = tkinter.Entry(self.root, textvariable=self.path)  # 生成一个文本框，内容保存在上面变量中
        self.xmind_path.configure(highlightbackground='WhiteSmoke')
        self.xmind_path.grid(row=0, column=1)  # 使用grid布局，文本框显示在第一行，第二列
        # （注意：只写方法名，保存方法的位置，不能加上()来调用）例：get_value，不能写成get_value()
        self.floder_select_button = tkinter.Button(self.root, text="路径选择", command=self.select_path)
        self.floder_select_button.configure(highlightbackground='WhiteSmoke')
        self.file_select_button = tkinter.Button(self.root, text="选择文件", command=self.select_file)
        self.file_select_button.configure(highlightbackground='WhiteSmoke')
        self.floder_select_button.grid(row=0, column=2)  # 使用grid布局，按钮显示在第一行，第三列
        self.file_select_button.grid(row=0, column=3)
        # 测试人员
        self.reporter_label = tkinter.Label(self.root, text="报告人员：", bg='WhiteSmoke')
        self.reporter_label.grid(row=1, column=0)
        self.repoter = tkinter.StringVar()
        self.reporter_text = tkinter.Entry(self.root, textvariable=self.repoter)
        self.reporter_text.configure(highlightbackground='WhiteSmoke')
        self.reporter_text.grid(row=1, column=1)

        # 提交按钮
        self.submit_button = tkinter.Button(self.root, text="提交", command=self.submit)  # 设置按钮的文字，调用方法，大小，颜色，显示框架
        self.submit_button.configure(highlightbackground='WhiteSmoke')
        self.submit_button.grid(row=1, column=2)  # 使用grid布局，按钮显示在第一行，第一列

        #日志
        self.log_title = tkinter.Label(self.root, text="日志:", bg='WhiteSmoke')
        self.log_title.grid(row=2, column=0, sticky=tkinter.N)
        self.log_text = tkinter.Text(self.root, width=50, height=15, relief=GROOVE)
        self.log_text.configure(highlightbackground='WhiteSmoke')
        self.log_text.grid(row=2, column=1, sticky=tkinter.SW, columnspan=3)

    def opendir(self, path):
        if system == "Darwin":
            os.system('open ' + path)
        elif system == "Windows":
            os.system('start ' + path)

    def openfile(self, file):
        if system == "Darwin":
            os.system('open ' + file)
        elif system == "Windows":
            os.system('start ' + file)

    def get_value(self):
        """获取文本框中数据"""
        fileBasePath = self.path.get()
        if fileBasePath == '':
            self.log_text.insert(END, '用例路径为空\n')
            tm.showerror(title='提示', message='用例路径为空')
            self.log_text.delete('1.0', END)
            raise

        if system == "Darwin":
            filePath = fileBasePath
        elif system == "Windows":
            filePath = "\\".join(fileBasePath.split("/"))
        else:
            filePath = fileBasePath

        repoterName = self.repoter.get()
        if repoterName == '':
            self.log_text.insert(END, '用户名为空\n')
            if_contiune = tm.askyesno(title='提示', message='报告人为空，是否重新执行？')
            if if_contiune is False:
                return filePath, repoterName
            else:
                self.log_text.delete('1.0', END)
                raise
        return filePath, repoterName


    def submit(self):
        xmind_to_csv_main = XmindToCsvMain()
        filePath, repoterName = self.get_value()
        result = xmind_to_csv_main.create_cases(filePath, repoterName)
        if result is True:
            self.log_text.insert(END, '用例转换成功成功\n')
            if_open = tm.askyesno(title='提示', message='执行成功，是否打开用例文件夹')
            if if_open:
                if Path(filePath).is_dir():
                    self.opendir(filePath)
                else:
                    self.opendir(str(Path(filePath).parent))
            else:
                self.log_text.insert(END, '请自行查阅文件\n')
        else:
            if_pass = tm.askyesno(title='提示', message=str(result[1])+'是否现在检查该文件？')
            if if_pass:
                filePath = result[1]
                self.openfile(filePath)
            else:
                self.log_text.insert(END, str(result))

    def select_path(self):
        """选择xmind文件夹"""
        path_ = askdirectory()
        self.path.set(path_)


    def select_file(self):
        """选择xmind文件"""
        path_ = askopenfilename()
        self.path.set(path_)

    def mainloop(self):
        self.root.mainloop()


# 进入消息循环（必需组件）
if __name__ == '__main__':
    window = Window()
    window.mainloop()
