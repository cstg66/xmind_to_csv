# testcase_to_notion

1. 准备Xmind编写的测试用例， 可参考demo.xmind ![image](demo.png)
2. 此版本仅可以使用create_csv.py 生成csv文件
>python create_csv.py -F demo.xmind
3. 在Notion中上传创建好的csv文件，即可生成相应的测试用例集合

### 注意事项
1. 测试用例标题层级，必须有优先级标注
2. 用例标题后最多有三个层级(用例标题-->步骤-->预期结果)，超出或缺少会导致报错
3. 部分特殊字符可能会导致转换失败

### TODO
1. 直接在Notion中创建相应的测试用例集合，减少手动上传的时间
2. 更多报错信息及兼容性
3. 更灵活的xmind模板